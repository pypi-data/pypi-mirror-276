# HiFi Solves Human WGS workflow runner

As part of [the HiFi Solves Consortium](https://hifisolves.org/collections), organizations will run their sequencing data through [PacBio's Human Whole Genome Sequencing (WGS) pipeline](https://github.com/PacificBiosciences/HiFi-human-WGS-WDL).

This package handles uploading all required raw data to the organization's cloud, configures the required workflow metadata, and triggering a run of the HumanWGS workflow. Output files are automatically ingested into Publisher and made available on [hifisolves.org](https://hifisolves.org/collections).

## Package information

- HumanWGS pipeline version: [`v1.1.0`](https://github.com/PacificBiosciences/HiFi-human-WGS-WDL/releases/tag/v1.1.0)

### Requirements

- python3.9+
- An engine registered on Workbench
- Credentials for the relevant backend (supported backends: AWS)

## Installation

`python3 -m pip install hifi-solves-run-humanwgs`

## Tests

`python3 -m unittest discover -b -s tests`

# Script usage

## Arguemnts

```bash
usage: run-humanwgs [-h] [-v] -s SAMPLE_INFO -b {AWS,GCP,AZURE} -r REGION -o ORGANIZATION [-e ENGINE] [-f]

Upload genomics data and run PacBio's official Human WGS pipeline

options:
  -h, --help            show this help message and exit
  -v, --version         Program version
  -s SAMPLE_INFO, --sample-info SAMPLE_INFO
                        Path to sample info CSV or TSV. This file should have columns [family_id, sample_id, movie_bams, phenotypes, father_id, mother_id, sex]. See
                        documentation for more information on the format of this file.
  -b {AWS,GCP,AZURE}, --backend {AWS,GCP,AZURE}
                        Backend where infrastructure is set up
  -r REGION, --region REGION
                        Region where infrastructure is set up
  -o ORGANIZATION, --organization ORGANIZATION
                        Organization identifier; used to infer bucket names
  -e ENGINE, --engine ENGINE
                        Engine to use to run the workflow. Defaults to the default engine set in Workbench.
  -f, --force-rerun     Force rerun samples that have previously been run
```

## Sample info file

The sample info file defines the set of samples that will be run through the workflow. The workflow can either be run on individual samples or on families (typically trios, where sequencing data exists for the mother, father, and child). One sample ID file per cohort / workflow run should be generated; the workflow will be run on all samples within a single sample_info.csv file.

This information is organized into a CSV file with the following columns:

| Column name              | Description                                                                                                                                                                                                                                                                                                                                     |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `family_id`              | Unique identifier for this family / cohort. If you are running a single sample through the workflow, this can be set to the same value as `sample_id`. Note that only one family_id should be set across all samples/rows; if you want to run more than one cohort, their information should be written into separate smaple information files. |
| `sample_id`              | Sample identifier                                                                                                                                                                                                                                                                                                                               |
| `movie_bams`<sup>†</sup> | Local path to a movie BAM file associated with this sample                                                                                                                                                                                                                                                                                      |
| `phenotypes`<sup>†</sup> | [Human Phenotype Ontology (HPO) phenotypes](https://hpo.jax.org/app/) associated with the cohort. If no particular phenotypes are desired, the root HPO term, "HP:0000001", can be used. Any sample with a phenotype set is assumed to be affected for that phenotype.                                                                          |
| `father_id`              | sample_id of the father. This field can be left blank if the sample's father is not included in the run.                                                                                                                                                                                                                                        |
| `mother_id`              | sample_id of the mother. This field can be left blank if the sample's mother is not included in the run.                                                                                                                                                                                                                                        |
| `sex`                    | Set to either "MALE" or "FEMALE"                                                                                                                                                                                                                                                                                                                |

† There can be more than one movie bam or phenotype for a sample. If this is the case, a new row should be generated for each additional movie_bam and/or phenotype; `family_id` and `sample_id` must be set for these fields, but information from other fields need not be repeated.

### Example sample info file

#### Singleton

Here we have a single sample, HG005, with two associated movie bams found at the local paths `bams/HG005_1.hifi_reads.bam` and `bams/HG005_2.hifi_reads.bam`. This sample does not have any phenotypes associated with it, so the phenotypes field is left blank; the root HPO term, "HP:0000001", will be set automatically. The sample is being run alone so `father_id` and `mother_id` are left blank. Sex information only needs to be included once and can be omitted for futher rows associated with the same `sample_id`.

```csv
family_id,sample_id,movie_bams,phenotypes,father_id,mother_id,sex
HG005,HG005,bams/HG005_1.hifi_reads.bam,,,,MALE
HG005,HG005,bams/HG005_2.hifi_reads.bam,,,,
```

#### Trio

Here we have a trio of samples: a child (HG005), father (HG006), and mother (HG007). The mother and father samples have several associated `movie_bams`, so there are multiple rows for each. The child has only a single movie bam but two phenotypes, so there are two rows for the child, one for each unique phenotype.

```csv
family_id,sample_id,movie_bams,phenotypes,father_id,mother_id,sex
hg005-trio,HG005,bams/HG005_1.hifi_reads.bam,HP:0001250,HG006,HG007,MALE
hg005-trio,HG005,,HP:0001263,,,
hg005-trio,HG006,bams/HG006_1.hifi_reads.bam,,,,MALE
hg005-trio,HG006,bams/HG006_2.hifi_reads.bam,,,,
hg005-trio,HG007,bams/HG007_1.hifi_reads.bam,,,,FEMALE
hg005-trio,HG007,bams/HG007_2.hifi_reads.bam,,,,
hg005-trio,HG007,bams/HG007_3.hifi_reads.bam,,,,
```

## Example run command - AWS

```bash
# AWS credentials
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""

AWS_REGION=""
# Used for naming upload and output buckets
ORGANIZATION=""

run-humanwgs \
    --sample-info sample_info.csv \
    --backend aws \
    --region "${REGION}" \
    --organization "${ORGANIZATION}"
```
