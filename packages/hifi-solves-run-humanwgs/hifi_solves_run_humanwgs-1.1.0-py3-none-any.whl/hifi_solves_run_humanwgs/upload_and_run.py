#!/usr/bin/env python3

from argparse import ArgumentParser

import importlib
import pkg_resources
import os
import pandas as pd
from pathlib import Path
import re
import subprocess
import json
import hashlib
from .constants import (
    WORKBENCH_URL,
    WORKFLOW_NAME,
    WORKFLOW_VERSION,
    AWS_CONTAINER_REGISTRY_ACCOUNT,
)

from importlib.metadata import version


def parse_args():
    """
    Parse command-line arguments

    Returns:
        args (argparse.Namespace): Parsed command-line arguments
    """
    parser = ArgumentParser(
        description="Upload genomics data and run PacBio's official Human WGS pipeline"
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {version('hifi_solves_run_humanwgs')}; HumanWGS workflow {WORKFLOW_VERSION}",
        help="Program version",
    )

    parser.add_argument(
        "-s",
        "--sample-info",
        required=True,
        type=str,
        help="Path to sample info CSV or TSV. This file should have columns [family_id, sample_id, movie_bams, phenotypes, father_id, mother_id, sex]. See documentation for more information on the format of this file.",
    )

    parser.add_argument(
        "-b",
        "--backend",
        required=True,
        type=str.upper,
        help="Backend where infrastructure is set up",
        choices=["AWS", "GCP", "AZURE"],
    )

    parser.add_argument(
        "-r",
        "--region",
        required=True,
        type=str,
        help="Region where infrastructure is set up",
    )

    parser.add_argument(
        "-o",
        "--organization",
        required=True,
        type=str,
        help="Organization identifier; used to infer bucket names",
    )

    parser.add_argument(
        "-e",
        "--engine",
        required=False,
        type=str,
        help="Engine to use to run the workflow. Defaults to the default engine set in Workbench.",
    )

    parser.add_argument(
        "-f",
        "--force-rerun",
        required=False,
        default=False,
        action="store_true",
        help="Force rerun samples that have previously been run",
    )

    args = parser.parse_args()
    return args


def import_backend_module(backend):
    """
    Import backend-specific functions

    Args:
        backend (str): Backend where infrastructure is set up ["AWS", "GCP", "AZURE"]

    Returns:
        (module): Module containing backend-specific functions
    """
    try:
        backend_module = importlib.import_module(
            f".backends.{backend.lower()}", package="hifi_solves_run_humanwgs"
        )
    except:
        raise ImportError(f"Module backends.{backend.lower()} not found.")

    return backend_module


def _confirm_unqiue_values(sample_info, columns):
    """
    Confirm that there is exactly one unique value for each family_id/sample_id combination for a set of columns in the DataFrame

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information
        columns (List[str]): Set of columns to check

    Raises:
        ValueError: If there is more than one unique value for any combination of family_id, sample_id
    """
    sample_info = sample_info.set_index(["family_id", "sample_id"])
    for column in columns:
        unique_values = sample_info.groupby(["family_id", "sample_id"])[
            column
        ].nunique()
        if (unique_values > 1).any():
            problematic_samples = sample_info[
                sample_info.index.isin(unique_values[unique_values > 1].index)
            ]
            raise ValueError(
                f"There should be exactly one unique value of {column} for each combination of family_id, sample_id\n{problematic_samples}"
            )


def _standardize_sex(sample_info):
    """
    Standardize the representation of sex in the sample_info DataFrame

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        sample_info (pd.DataFrame): DataFrame containing sample information with sex standardized
    """
    sex_mapping = {
        "MALE": "MALE",
        "M": "MALE",
        "1": "MALE",
        "FEMALE": "FEMALE",
        "F": "FEMALE",
        "2": "FEMALE",
        "None": None,
        "UNKNOWN": None,
        "0": None,
        "-1": None,
        "Null": None,
    }

    def map_sex(value):
        if pd.isna(value):
            return None
        elif str(value).upper() in sex_mapping:
            return sex_mapping[str(value).upper()]
        else:
            raise KeyError(
                f"Invalid sex '{value}'; should be one of ['MALE', 'FEMALE', None (empty value)]"
            )

    sample_info["sex"] = sample_info["sex"].map(map_sex)

    return sample_info


def _extract_phenotypes(sample_info):
    """
    Confirm that phenotypes are set properly and return the set of unique phenotypes. Set the phenotype to the root HPO term if the proband can be determined.
    Set the affected column based on the value of phenotypes.

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        phenotypes (pd.Series): Series containing phenotypes
        sample_info (pd.DataFrame): DataFrame containing sample information with phenotypes set
    """
    root_phenotypes = ["HP:0000001"]
    # Set phenotype to the root HPO term if it has not been defined
    if sample_info["phenotypes"].isnull().all():
        # If there is a single sample, set the phenotype to the root HPO term
        if len(sample_info) == 1:
            sample_info["phenotypes"] = root_phenotypes

        # If there are several samples but one is a proband, set the phenotype to the root HPO term
        elif (
            len(
                sample_info[
                    sample_info["mother_id"].notnull()
                    | sample_info["father_id"].notnull()
                ]
            )
            == 1
        ):
            proband_index = sample_info[
                sample_info["mother_id"].notnull() | sample_info["father_id"].notnull()
            ].index[0]
            sample_info.at[proband_index, "phenotypes"] = root_phenotypes

        # Otherwise, raise an error and ask the user to fill this out more clearly
        else:
            raise ValueError(
                "Must define at least one phenotype for the proband.  If no particular phenotypes are desired, the root HPO term, 'HP:0000001', can be used."
            )

    # Confirm that all phenotypes match the HPO regex
    hpo_regex = re.compile(r"^HP:[0-9]{7}$")
    invalid_phenotypes = set(
        filter(
            lambda phenotype: not hpo_regex.match(phenotype),
            sample_info["phenotypes"].explode().dropna().unique(),
        )
    )
    if len(invalid_phenotypes) > 0:
        raise ValueError(
            f"Invalid HPO term(s) found: {invalid_phenotypes}\nHPO terms should be of the form HP:xxxxxxx, where x is a digit 0-9. See [the Human Phenotype Ontology](https://hpo.jax.org/app/) for more information."
        )

    # Confirm that there is exactly one possible set of phenotypes across all samples
    unique_phenotype_sets = (
        sample_info["phenotypes"]
        .apply(lambda x: tuple(x) if x is not None else None)
        .dropna()
        .unique()
    )
    if len(unique_phenotype_sets) > 1:
        raise ValueError(
            f"There should be exactly one unique set of phenotypes across all samples; found {unique_phenotype_sets}"
        )

    phenotypes = list(unique_phenotype_sets[0])

    # Set the affected column based on the value of phenotypes
    sample_info["affected"] = sample_info["phenotypes"].apply(
        lambda x: True if x == phenotypes else False
    )

    sample_info = sample_info.drop("phenotypes", axis=1)

    return phenotypes, sample_info


def validate_format_sample_info(sample_info):
    """
    Validate that sample_info contains the required information and reformat it

    Args:
        sample_info (pd.DataFrame): DataFrame containing sample information

    Returns:
        formatted_sample_info (pd.DataFrame): Reformatted and validated sample information
        phenotypes (List[str]): List of phenotypes associated with this cohort
    """
    required_columns = ["family_id", "sample_id", "movie_bams"]
    optional_columns = ["phenotypes", "father_id", "mother_id", "sex"]

    # Confirm all the required columns are present
    missing_required_columns = set(required_columns) - set(sample_info.columns)
    if missing_required_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_required_columns))}"
        )
    for col in optional_columns:
        if col not in sample_info.columns:
            sample_info[col] = None

    # Confirm that there is exactly one family ID in this file
    if sample_info["family_id"].nunique() != 1:
        raise ValueError(
            f"There should be exactly one unique value of family_id in the sample_info file; found {list(sample_info['family_id'].unique())}\nTo run multiple families, make separate family info files"
        )

    sample_info = _standardize_sex(sample_info)

    # Confirm that there is exactly one unique value of mother_id, father_id, sex for each combination of family_id, sample_id
    _confirm_unqiue_values(sample_info, ["mother_id", "father_id", "sex"])

    # Gather movie_bams, phenotypes for each family_id-sample_id combination
    sample_info = (
        sample_info.groupby(["family_id", "sample_id"])
        .agg(
            {
                "movie_bams": lambda x: (
                    (sorted(list(set(x.dropna())))) if x.notnull().any() else None
                ),
                "phenotypes": lambda x: (
                    sorted(list(set(x.dropna()))) if x.notnull().any() else None
                ),
                "father_id": "first",
                "mother_id": "first",
                "sex": "first",
            }
        )
        .reset_index()
    )

    phenotypes, sample_info = _extract_phenotypes(sample_info)

    # Confirm that there are no null values in any required column
    na_values = sample_info[required_columns].isna().any()
    if na_values.any():
        missing_value_columns = na_values[na_values].index.tolist()
        raise ValueError(
            f"Missing values found in required columns: {', '.join(missing_value_columns)}"
        )

    # Confirm that there are no duplicate movie bams across different samples
    movie_bams = sample_info["movie_bams"].explode().dropna()
    if len(movie_bams) != len(set(movie_bams)):
        seen_bams = set()
        duplicate_bams = set()
        for movie_bam in movie_bams:
            if movie_bam in seen_bams:
                duplicate_bams.add(movie_bam)
            else:
                seen_bams.add(movie_bam)
        raise ValueError(f"Duplicate movie bams found: {', '.join(duplicate_bams)}")

    return sample_info, phenotypes


def _check_file_exists_locally(file_path):
    """
    Check if a file exists locally

    Args:
        file_path (str): Path to file

    Returns:
        file_exists (bool): True if file exists at path; False if it does not
    """
    return Path(file_path).exists()


def upload_files(sample_info, backend_module, raw_data_bucket, path_prefix=None):
    """
    Check whether files exist in the raw_data_bucket; if not, upload them

    Args:
        sample_info (pd.DataFrame): Sample information
        backend_module (module): Module containing backend-specific functions
        raw_data_bucket (str): Bucket where workflow input files will be uploaded
        path_prefix (str): Path within the bucket to upload files to

    Returns:
        formatted_sample_info (pd.DataFrame): Sample information with movie bams paths
            translated to their remote equivalent
    """
    print("Checking whether files exist in the target bucket")
    file_info = {}
    for sample_id, file_path in sample_info["movie_bams"].explode().items():
        exists_locally = _check_file_exists_locally(file_path)
        exists_at_remote, remote_path = backend_module.check_file_exists(
            raw_data_bucket, path_prefix, file_path, sample_id, "bam"
        )
        file_info[file_path] = {
            "exists_locally": exists_locally,
            "exists_at_remote": exists_at_remote,
            "remote_path": remote_path,
        }

    # Error if any files do not exist locally or at remote
    files_not_found = [
        k
        for k, v in file_info.items()
        if not v["exists_locally"] and not v["exists_at_remote"]
    ]
    if len(files_not_found) > 0:
        raise FileNotFoundError(
            f"Files {files_not_found} not found locally or in raw data bucket [{raw_data_bucket}]. Check paths?"
        )

    # Upload files that are local only to remote
    files_to_upload = {
        k: v["remote_path"]
        for k, v in file_info.items()
        if v["exists_locally"] and not v["exists_at_remote"]
    }
    backend_module.upload_files(raw_data_bucket, files_to_upload)

    sample_info["movie_bams"] = sample_info["movie_bams"].apply(
        lambda x: [
            f"s3://{raw_data_bucket}/{file_info[movie_bam]['remote_path']}"
            for movie_bam in x
        ]
    )
    return sample_info


def _register_workflow():
    """
    Register a workflow in Workbench

    Returns:
        workflow_id (str): Workflow ID for the registered workflow
    """
    package_path = pkg_resources.resource_filename("upload_and_run", "")
    entrypoint_path = os.path.join(package_path, "workflows", "hifisolves_wrapper.wdl")

    # TODO remove alpha; use a zip of the directory?
    workflow_info = subprocess.run(
        [
            "omics",
            "alpha",
            "workbench",
            "workflows",
            "create",
            "--name",
            WORKFLOW_NAME,
            "--version-name",
            WORKFLOW_VERSION,
            entrypoint_path,
        ],
        capture_output=True,
        text=True,
    )
    if workflow_info.returncode == 0:
        try:
            workflow_info_json = json.loads(workflow_info.stdout)
            workflow_id = workflow_info_json["internalId"]
            print("\t✓ Registered workflow")
            return workflow_id
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        raise SystemExit(
            f"Something went wrong when attempting to register the workflow\n{workflow_info.stderr}"
        )


def _register_workflow_version(workflow_id):
    """
    Register a workflow version in Workbench
    """
    package_path = pkg_resources.resource_filename("upload_and_run", "")
    entrypoint_path = os.path.join(package_path, "workflows", "hifisolves_wrapper.wdl")

    # TODO remove alpha
    version_info = subprocess.run(
        [
            "omics",
            "alpha",
            "workbench",
            "workflows",
            "versions",
            "create",
            "--workflow",
            workflow_id,
            "--name",
            WORKFLOW_VERSION,
            entrypoint_path,
        ],
        capture_output=True,
        text=True,
    )

    if version_info.returncode == 0:
        print("\t✓ Registered workflow version")
    else:
        raise SystemExit(
            f"Something went wrong when attempting to register a workflow version\n{version_info.stderr}"
        )


def get_workflow_id(workflow_name, workflow_version):
    """
    Get the workflow ID for the HumanWGS workflow, or register it if it does not exist

    Args:
        workflow_name (str): Name of the workflow
        workflow_version (str): Workflow version

    Returns:
        workflow_id (str): Workflow ID for the HumanWGS wrapper workflow
    """

    # See if the workflow exists
    workflow_list = subprocess.run(
        [
            "omics",
            "workbench",
            "workflows",
            "list",
            "--source",
            "PRIVATE",
            "--search",
            workflow_name,
        ],
        capture_output=True,
        text=True,
    )

    if workflow_list.returncode == 0:
        try:
            workflow_list_json = json.loads(workflow_list.stdout)
            filtered_workflow_list = [
                workflow
                for workflow in workflow_list_json
                if workflow["name"] == workflow_name
            ]
            if len(filtered_workflow_list) == 1:
                workflow_id = filtered_workflow_list[0]["internalId"]
                if filtered_workflow_list[0]["latestVersion"] != workflow_version:
                    print(
                        "\tWorkflow version {workflow_version} not found for workflow {workflow_name}; registering new version"
                    )
                    _register_workflow_version(workflow_id)
                else:
                    print("\t✓ Workflow found in Workbench")
            elif len(filtered_workflow_list) > 1:
                raise SystemExit(
                    f"More than one workflow returned; not sure what to do\n{filtered_workflow_list}"
                )
            else:
                print("\tWorkflow not found in Workbench; registering workflow")
                workflow_id = _register_workflow()
        except json.JSONDecodeError as e:
            raise SystemExit(f"Error parsing JSON: {e}\n{workflow_list.stderr}")
    else:
        raise SystemExit(
            f"Something went wrong when listing workflows\n{workflow_list.stderr}"
        )
    return workflow_id


def trigger_worfklow_run(
    workflow_inputs, workflow_id, workflow_version, engine, rerun=False
):
    """
    Trigger a run of the workflow via Workbench

    Args:
        workflow_inputs (dict): Inputs JSON that will be used to trigger the workflow
        engine (str): Engine ID to run the workflow through; defaults to the default engine configured in Workbench
    """
    identifier = (
        workflow_inputs["HumanWGS_wrapper.cohort"]["cohort_id"]
        + "-"
        + "-".join(
            [
                sample["sample_id"]
                for sample in workflow_inputs["HumanWGS_wrapper.cohort"]["samples"]
            ]
        )
    )
    inputs_hash = hashlib.md5(
        (json.dumps(workflow_inputs, sort_keys=True)).encode("utf-8")
    ).hexdigest()
    tags = {
        "identifier": identifier,
        "inputs_hash": inputs_hash,
        "workflow": workflow_id,
        "workflow_version": workflow_version,
    }

    # Ensure this combination of workflow/version/inputs has not been run successfully before
    run_list = subprocess.run(
        ["omics", "workbench", "runs", "list", "--tags", json.dumps(tags)],
        capture_output=True,
        text=True,
    )
    if run_list.returncode == 0:
        try:
            run_list_json = json.loads(run_list.stdout)
            # TODO see if any of them were actually successful
            if len(run_list_json) > 0:
                if rerun is False:
                    raise SystemExit(
                        f"\tFound {len(run_list_json)} previous runs using this workflow version and these inputs. To force a rerun, rerun this command with the --force-rerun flag."
                    )
                else:
                    print(
                        "Previous runs found for this workflow version and inputs; rerunning anyway."
                    )
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
    else:
        raise SystemExit(
            f"Something went wrong when listing previous runs\n{run_list.stderr}"
        )

    workflow_run_cmd = [
        "omics",
        "workbench",
        "runs",
        "submit",
        "--url",
        f"{workflow_id}/{workflow_version}",
        "--engine-params",
        json.dumps({}),
        "--workflow-params",
        json.dumps(workflow_inputs),
        "--tags",
        json.dumps(tags),
    ]
    if engine is not None:
        workflow_run_cmd.extend(["--engine", engine])

    subprocess.run(workflow_run_cmd)
    print("\t✓ Workflow run submitted")


def main():
    args = parse_args()

    sample_info = pd.read_csv(
        args.sample_info,
        sep=None,
        engine="python",
        dtype={
            "family_id": str,
            "sample_id": str,
            "movie_bams": str,
            "phenotypes": str,
            "father_id": str,
            "mother_id": str,
            "sex": str,
        },
    )
    # Import backend-specific functions
    backend_module = import_backend_module(args.backend)

    print("Formatting sample information")
    formatted_sample_info, phenotypes = validate_format_sample_info(sample_info)
    formatted_sample_info.set_index("sample_id", drop=False, inplace=True)
    print("\t✓ Sample information formatted")

    # Bucket configuration
    organization = args.organization
    raw_data_bucket = f"{organization}-raw-data"
    reference_inputs_bucket = f"{organization}-reference-inputs"
    workflow_file_outputs_bucket = f"{organization}-workflow-file-outputs"
    workflow_tabular_outputs_bucket = f"{organization}-workflow-table-outputs"

    print("Confirming that the raw data bucket exists, and that you have access to it")
    raw_data_bucket, path_prefix = backend_module.validate_bucket(raw_data_bucket)

    formatted_sample_info_with_paths = upload_files(
        formatted_sample_info, backend_module, raw_data_bucket, path_prefix
    )

    container_registry = (
        (f"{AWS_CONTAINER_REGISTRY_ACCOUNT}.dkr.ecr.{args.region}.amazonaws.com")
        if args.backend == "AWS"
        else None
    )
    print("Preparing worfklow inputs")
    workflow_inputs = backend_module.generate_inputs_json(
        formatted_sample_info_with_paths,
        phenotypes,
        reference_inputs_bucket,
        workflow_file_outputs_bucket,
        workflow_tabular_outputs_bucket,
        container_registry,
    )

    print("Configuring workbench")
    subprocess.run(["omics", "use", WORKBENCH_URL])
    print("\t✓ Workbench configured")

    print(
        f"Registering or retrieving the workflow from Workbench ([{WORKFLOW_NAME}:{WORKFLOW_VERSION}])"
    )
    workflow_id = get_workflow_id(WORKFLOW_NAME, WORKFLOW_VERSION)

    # TODO consider uploading inputs JSON somewhere
    print("Triggering workflow run")
    trigger_worfklow_run(
        workflow_inputs, workflow_id, WORKFLOW_VERSION, args.engine, args.force_rerun
    )

    print("Script execution complete")


if __name__ == "__main__":
    main()
