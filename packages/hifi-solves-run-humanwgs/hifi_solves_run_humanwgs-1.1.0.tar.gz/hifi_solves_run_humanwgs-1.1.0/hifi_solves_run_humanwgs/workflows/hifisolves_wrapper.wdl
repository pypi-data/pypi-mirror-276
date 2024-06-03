version 1.0

import "HiFi-human-WGS-WDL/workflows/wdl-common/wdl/workflows/backend_configuration/backend_configuration.wdl" as BackendConfiguration
import "HiFi-human-WGS-WDL/workflows/main.wdl" as main

workflow HumanWGS_wrapper {
    input {
        Cohort cohort

        ReferenceData reference
        SlivarData? slivar_data

        String deepvariant_version = "1.5.0"
        DeepVariantModel? deepvariant_model

        Int? pbsv_call_mem_gb
        Int? glnexus_mem_gb

        # Backend configuration
        String backend
        String? zones
        String? aws_spot_queue_arn
        String? aws_on_demand_queue_arn
        String? container_registry
        Boolean preemptible

        # Wrapper workflow inputs
        String workflow_outputs_bucket
        String tabular_outputs_bucket
        String reference_version = 'GRCh38'
    }

    String workflow_name = "HumanWGS"
    String workflow_version = "v1.1.0"

    call BackendConfiguration.backend_configuration {
        input:
            backend = backend,
            zones = zones,
            aws_spot_queue_arn = aws_spot_queue_arn,
            aws_on_demand_queue_arn = aws_on_demand_queue_arn,
            container_registry = container_registry
    }

    RuntimeAttributes default_runtime_attributes = if preemptible then backend_configuration.spot_runtime_attributes else backend_configuration.on_demand_runtime_attributes

    scatter (sample in cohort.samples) {
        String sample_id = sample.sample_id
    }

    call main.humanwgs as humanwgs {
        input:
            cohort = cohort,
            reference = reference,
            slivar_data = slivar_data,
            deepvariant_model = deepvariant_model,
            pbsv_call_mem_gb = pbsv_call_mem_gb,
            glnexus_mem_gb = glnexus_mem_gb,
            run_tertiary_analysis = true,
            deepvariant_version = deepvariant_version,
            backend = backend,
            zones = zones,
            aws_spot_queue_arn = aws_spot_queue_arn,
            aws_on_demand_queue_arn = aws_on_demand_queue_arn,
            container_registry = container_registry,
            preemptible = preemptible
    }

    # Convert VCF, gVCF outputs to ORC files
    scatter (vcf in humanwgs.sample_phased_small_variant_vcfs) {
        call convert_vcf_to_orc as convert_sample_phased_small_variant_vcfs_to_orc {
            input:
                vcf = vcf,
                reference_version = reference_version,
                runtime_attributes = default_runtime_attributes
        }
    }

    scatter (vcf in humanwgs.sample_phased_sv_vcfs) {
        call convert_vcf_to_orc as convert_sample_phased_sv_vcfs_to_orc {
            input:
                vcf = vcf,
                reference_version = reference_version,
                runtime_attributes = default_runtime_attributes
        }
    }

    scatter (vcf in humanwgs.trgt_repeat_vcf) {
        call convert_vcf_to_orc as convert_trgt_repeat_vcfs_to_orc {
            input:
                vcf = vcf,
                reference_version = reference_version,
                runtime_attributes = default_runtime_attributes
        }
    }

    scatter (vcf in humanwgs.hificnv_vcfs) {
        call convert_vcf_to_orc as convert_hificnv_vcfs_to_orc {
            input:
                vcf = vcf,
                reference_version = reference_version,
                runtime_attributes = default_runtime_attributes
        }
    }

    call convert_vcf_to_orc as convert_cohort_analysis_phased_joint_small_variant_vcf_to_orc {
        input:
            vcf = select_first([humanwgs.cohort_small_variant_vcf]),
            reference_version = reference_version,
            runtime_attributes = default_runtime_attributes
    }

    call convert_vcf_to_orc as convert_cohort_analysis_phased_joint_sv_vcf_to_orc {
        input:
            vcf = select_first([humanwgs.cohort_sv_vcf]),
            reference_version = reference_version,
            runtime_attributes = default_runtime_attributes
    }

    call convert_vcf_to_orc as convert_tertiary_analysis_filtered_small_variant_vcf_to_orc {
        input:
            vcf = select_first([humanwgs.filtered_small_variant_vcf]),
            reference_version = reference_version,
            runtime_attributes = default_runtime_attributes
    }

    call convert_vcf_to_orc as convert_tertiary_analysis_compound_het_small_variant_vcf_to_orc {
        input:
            vcf = select_first([humanwgs.compound_het_small_variant_vcf]),
            reference_version = reference_version,
            runtime_attributes = default_runtime_attributes
    }

    call convert_vcf_to_orc as convert_tertiary_analysis_filtered_svpack_vcf_to_orc {
        input:
            vcf = select_first([humanwgs.filtered_svpack_vcf]),
            reference_version = reference_version,
            runtime_attributes = default_runtime_attributes
    }

    scatter (gvcf in humanwgs.small_variant_gvcfs) {
        call convert_gvcf_to_orc {
                input:
                    gvcf = gvcf.data,
                    reference_fasta = reference.fasta.data,
                    runtime_attributes = default_runtime_attributes
        }
    }

    # Gather workflow output files
    ## IndexData
    scatter (small_variant_gvcf in humanwgs.small_variant_gvcfs) {
        File small_variant_gvcf_data = small_variant_gvcf.data
        File small_variant_gvcf_data_index = small_variant_gvcf.data_index
    }

    scatter (sample_phased_small_variant_vcf in humanwgs.sample_phased_small_variant_vcfs) {
        File sample_phased_small_vcf_data = sample_phased_small_variant_vcf.data
        File sample_phased_small_vcf_data_index = sample_phased_small_variant_vcf.data_index
    }

    scatter (sample_phased_sv_vcfs in humanwgs.sample_phased_sv_vcfs) {
        File sample_phased_sv_data = sample_phased_sv_vcfs.data
        File sample_phased_sv_data_index = sample_phased_sv_vcfs.data_index
    }

    scatter (merged_haplotagged_bam in humanwgs.merged_haplotagged_bam) {
        File mhb_data = merged_haplotagged_bam.data
        File mhb_data_index = merged_haplotagged_bam.data_index
    }

    scatter (trgt_spanning_reads in humanwgs.trgt_spanning_reads) {
        File trgt_reads_data = trgt_spanning_reads.data
        File trgt_reads_data_index = trgt_spanning_reads.data_index
    }

    scatter (trgt_repeat_vcf in humanwgs.trgt_repeat_vcf) {
        File trgt_vcf_data = trgt_repeat_vcf.data
        File trgt_vcf_data_index = trgt_repeat_vcf.data_index
    }


    scatter (paraphase_realigned_bam in humanwgs.paraphase_realigned_bams) {
        File prb_data = paraphase_realigned_bam.data
        File prb_data_index = paraphase_realigned_bam.data_index
    }

    scatter (hificnv_vcf in humanwgs.hificnv_vcfs) {
        File hificnv_vcf_data = hificnv_vcf.data
        File hificnv_vcf_data_index = hificnv_vcf.data_index
    }

    ## IndexData?
    if (defined(humanwgs.cohort_sv_vcf)) {
        IndexData phased_joint_sv_vcf_struct = select_first([humanwgs.cohort_sv_vcf])

        File cohort_sv_vcf_data = phased_joint_sv_vcf_struct.data
        File cohort_sv_vcf_data_index = phased_joint_sv_vcf_struct.data_index
    }

    if (defined(humanwgs.cohort_small_variant_vcf)) {
        IndexData phased_joint_small_variant_vcf_struct = select_first([humanwgs.cohort_small_variant_vcf])

        File cohort_small_variant_vcf_data = phased_joint_small_variant_vcf_struct.data
        File cohort_small_variant_vcf_data_index = phased_joint_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.filtered_small_variant_vcf)) {
        IndexData filtered_small_variant_vcf_struct = select_first([humanwgs.filtered_small_variant_vcf])

        File filtered_small_variant_vcf_data = filtered_small_variant_vcf_struct.data
        File filtered_small_variant_vcf_data_index = filtered_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.compound_het_small_variant_vcf)) {
        IndexData compound_het_small_variant_vcf_struct = select_first([humanwgs.compound_het_small_variant_vcf])

        File compound_het_small_variant_vcf_data = compound_het_small_variant_vcf_struct.data
        File compound_het_small_variant_vcf_data_index = compound_het_small_variant_vcf_struct.data_index
    }

    if (defined(humanwgs.filtered_svpack_vcf)) {
        IndexData filtered_svpack_vcf_struct = select_first([humanwgs.filtered_svpack_vcf])

        File filtered_svpack_vcf_data = filtered_svpack_vcf_struct.data
        File filtered_svpack_vcf_data_index = filtered_svpack_vcf_struct.data_index
    }

    # Create array of workflow output names and their corresponding outputs
    # Each workflow_output_name is at the same index as the corresponding array of workflow_output_files
    Array[String] workflow_output_names = [
        # sample_analysis output
        "bam_stats",
        "read_length_summary",
        "read_quality_summary",
        "small_variant_gvcfs",
        "small_variant_vcf_stats",
        "small_variant_roh_out",
        "small_variant_roh_bed",
        "sample_phased_small_variant_vcfs",
        "sample_phased_sv_vcfs",
        "hiphase_stats",
        "hiphase_blocks",
        "hiphase_haplotags",
        "merged_haplotagged_bam",
        "haplotagged_bam_mosdepth_summary",
        "haplotagged_bam_mosdepth_region_bed",
        "trgt_spanning_reads",
        "trgt_repeat_vcf",
        "trgt_dropouts",
        "cpg_pileup_beds",
        "cpg_pileup_bigwigs",
        "paraphase_output_jsons",
        "paraphase_realigned_bams",
        "paraphase_vcfs",
        "hificnv_vcfs",
        "hificnv_copynum_bedgraphs",
        "hificnv_depth_bws",
        "hificnv_maf_bws",

        # cohort_analysis output
        "cohort_sv_vcf",
        "cohort_small_variant_vcf",
        "cohort_hiphase_stats",
        "cohort_hiphase_blocks",

        # tertiary_analysis output
        "filtered_small_variant_vcf",
        "compound_het_small_variant_vcf",
        "filtered_svpack_vcf",
        "filtered_small_variant_tsv",
        "compound_het_small_variant_tsv",
        "filtered_svpack_tsv"
    ]

    Array[Array[File]] workflow_output_files = [
        # sample_analysis output
        flatten(humanwgs.bam_stats),
        flatten(humanwgs.read_length_summary),
        flatten(humanwgs.read_quality_summary),
        flatten([small_variant_gvcf_data, small_variant_gvcf_data_index]),
        humanwgs.small_variant_vcf_stats,
        humanwgs.small_variant_roh_out,
        humanwgs.small_variant_roh_bed,
        flatten([sample_phased_small_vcf_data, sample_phased_small_vcf_data_index]),
        flatten([sample_phased_sv_data, sample_phased_sv_data_index]),
        humanwgs.sample_hiphase_stats,
        humanwgs.sample_hiphase_blocks,
        humanwgs.sample_hiphase_haplotags,
        flatten([mhb_data, mhb_data_index]),
        humanwgs.haplotagged_bam_mosdepth_summary,
        humanwgs.haplotagged_bam_mosdepth_region_bed,
        flatten([trgt_reads_data, trgt_reads_data_index]),
        flatten([trgt_vcf_data, trgt_vcf_data_index]),
        humanwgs.trgt_dropouts,
        flatten(humanwgs.cpg_pileup_beds),
        flatten(humanwgs.cpg_pileup_bigwigs),
        humanwgs.paraphase_output_jsons,
        flatten([prb_data, prb_data_index]),
        flatten(humanwgs.paraphase_vcfs),
        flatten([hificnv_vcf_data, hificnv_vcf_data_index]),
        humanwgs.hificnv_copynum_bedgraphs,
        humanwgs.hificnv_depth_bws,
        humanwgs.hificnv_maf_bws,

        # cohort_analysis output
        select_all([cohort_sv_vcf_data, cohort_sv_vcf_data_index]),
        select_all([cohort_small_variant_vcf_data, cohort_small_variant_vcf_data_index]),
        select_all([humanwgs.cohort_hiphase_stats]),
        select_all([humanwgs.cohort_hiphase_blocks]),

        #tertiary_analysis output
        select_all([filtered_small_variant_vcf_data, filtered_small_variant_vcf_data_index]),
        select_all([compound_het_small_variant_vcf_data, compound_het_small_variant_vcf_data_index]),
        select_all([filtered_svpack_vcf_data, filtered_svpack_vcf_data_index]),
        select_all([humanwgs.filtered_small_variant_tsv]),
        select_all([humanwgs.compound_het_small_variant_tsv]),
        select_all([humanwgs.filtered_svpack_tsv])
    ]

    call create_timestamp_and_identifier {
        input:
            workflow_output_files = workflow_output_files, # !StringCoercion
            cohort_id = cohort.cohort_id,
            sample_ids = sample_id,
            runtime_attributes = default_runtime_attributes
    }

    call organize_outputs_and_write_to_bucket as organize_and_write_workflow_outputs {
        input:
            output_names = workflow_output_names,
            output_files = workflow_output_files, # !StringCoercion
            output_type = "workflow",
            backend = backend,
            identifier = create_timestamp_and_identifier.identifier,
            timestamp = create_timestamp_and_identifier.timestamp,
            workflow_version = workflow_version,
            workflow_name = workflow_name,
            output_bucket = workflow_outputs_bucket,
            runtime_attributes = default_runtime_attributes
    }

    # Same process for tabular outputs; each tabular output is mapped to the corresponding task name
    #   that produced the original (g)VCF file
    Array[String] tabular_output_names = [
        "sample_phased_small_variant_vcfs",
        "sample_phased_sv_vcfs",
        "trgt_repeat_vcf",
        "hificnv_vcfs",
        "cohort_small_variant_vcf",
        "cohort_sv_vcf",
        "filtered_small_variant_vcf",
        "compound_het_small_variant_vcf",
        "filtered_svpack_vcf",
        "small_variant_gvcfs",
        "small_variant_gvcfs"
    ]

    Array[Array[File]] tabular_output_files = [
        flatten(convert_sample_phased_small_variant_vcfs_to_orc.vcf_orc),
        flatten(convert_sample_phased_sv_vcfs_to_orc.vcf_orc),
        flatten(convert_trgt_repeat_vcfs_to_orc.vcf_orc),
        flatten(convert_hificnv_vcfs_to_orc.vcf_orc),
        convert_cohort_analysis_phased_joint_small_variant_vcf_to_orc.vcf_orc,
        convert_cohort_analysis_phased_joint_sv_vcf_to_orc.vcf_orc,
        convert_tertiary_analysis_filtered_small_variant_vcf_to_orc.vcf_orc,
        convert_tertiary_analysis_compound_het_small_variant_vcf_to_orc.vcf_orc,
        convert_tertiary_analysis_filtered_svpack_vcf_to_orc.vcf_orc,
        convert_gvcf_to_orc.gvcf_tsv,
        flatten(convert_gvcf_to_orc.gvcf_orc)
    ]

    call organize_outputs_and_write_to_bucket as organize_and_write_tabular_outputs {
        input:
            output_names = tabular_output_names,
            output_files = tabular_output_files, # !StringCoercion
            output_type = "tabular",
            backend = backend,
            identifier = create_timestamp_and_identifier.identifier,
            timestamp = create_timestamp_and_identifier.timestamp,
            workflow_version = workflow_version,
            workflow_name = workflow_name,
            output_bucket = tabular_outputs_bucket,
            runtime_attributes = default_runtime_attributes
    }

   output {
        # Workflow outputs
        File workflow_output_json = organize_and_write_workflow_outputs.output_json
        File workflow_output_manifest_tsv = organize_and_write_workflow_outputs.output_manifest_tsv

        # Tabular outputs
        File tabular_output_json = organize_and_write_tabular_outputs.output_json
        File tabular_output_manifest_tsv = organize_and_write_tabular_outputs.output_manifest_tsv
    }

    parameter_meta {
        tabular_outputs_bucket: {help: "Path to the bucket where the tabular outputs will be stored"}
        workflow_outputs_bucket: {help: "Path to the bucket where the workflow outputs will be stored"}
        reference_version: {help: "Reference genome version to use for the convert_vcf_to_orc task (either 'GRCh37' or 'GRCh38'); default is 'GRCh38'"}
    }
}

task convert_gvcf_to_orc {
    input {
        File gvcf
        File reference_fasta

        RuntimeAttributes runtime_attributes
    }

    Int disk_size = ceil((size(gvcf, "GB") + size(reference_fasta, "GB")) * 4 + 20)

    String bcftools_tsv = basename(gvcf, ".g.vcf.gz") + ".translated_genotype.tsv"
    String minimal_representation_tsv = basename(gvcf, ".g.vcf.gz") + ".minimized.tsv"
    String output_dir = basename(gvcf, ".g.vcf.gz") + "_ORC_dir"

    command <<<
        set -euo pipefail

        bcftools_join_and_query.sh \
            -i ~{gvcf} \
            -r ~{reference_fasta} \
            -o ~{bcftools_tsv}

        query_to_minimal_representation.py \
            --input-tsv ~{bcftools_tsv} \
            --output-tsv ~{minimal_representation_tsv}

        tsv_to_orc.py \
            --input-tsv ~{minimal_representation_tsv} \
            --output-dir ~{output_dir}
    >>>

    output {
        File gvcf_tsv = "~{minimal_representation_tsv}"
        Array[File] gvcf_orc = glob("~{output_dir}/orc/*.orc")
    }

    runtime {
        docker: "~{runtime_attributes.container_registry}/hifi_solves_tools:1.2.0"
        cpu: 4
        memory: "16 GB"
        disk: disk_size + " GB"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}

task convert_vcf_to_orc {
    input {
        IndexData vcf
        String reference_version

        RuntimeAttributes runtime_attributes
    }

    Int disk_size = ceil((size(vcf.data, "GB") * 4 + 20))

    String processed_vcf = basename (vcf.data, ".vcf.gz") + ".processed.vcf.gz"
    String output_dir = basename (vcf.data, ".vcf.gz") + "_ORC_dir"

    command <<<
        set -euo pipefail

        vcf_to_orc.py \
            --input-vcf ~{vcf.data} \
            --processed-vcf ~{processed_vcf} \
            --reference-genome ~{reference_version} \
            --force-bgz \
            --output-path ~{output_dir}
    >>>

    output {
        Array[File] vcf_orc = glob("~{output_dir}/orc/*.orc")
    }

    runtime {
        docker: "~{runtime_attributes.container_registry}/vcf_to_orc:0.1.0"
        cpu: 4
        memory: "16 GB"
        disk: disk_size + " GB"
        disks: "local-disk " + disk_size + " HDD"
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}

task create_timestamp_and_identifier {
    input {
        Array[Array[String]] workflow_output_files
        String cohort_id
        Array[String] sample_ids

        RuntimeAttributes runtime_attributes
    }

    command <<<
        set -euo pipefail

        date +%s > timestamp.txt

        echo "~{cohort_id}-~{sep='-' sample_ids}" > identifier.txt

        echo -e "Created timestamp, identifier for outputs\n~{sep='\n' flatten(workflow_output_files)}"
    >>>

    output {
        String timestamp = read_string("timestamp.txt")
        String identifier = read_string("identifier.txt")
    }

    runtime {
        docker: "~{runtime_attributes.container_registry}/ubuntu:jammy"
        cpu: 2
        memory: "4 GB"
        disk: "15 GB"
        disks: "local-disk 15 HDD"
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}

task organize_outputs_and_write_to_bucket {
    input {
        Array[String] output_names
        Array[Array[String]] output_files
        String output_type
        String backend
        String identifier
        String timestamp
        String workflow_version
        String workflow_name
        String output_bucket

        RuntimeAttributes runtime_attributes
    }

    command <<<
        set -euo pipefail

        cp ~{write_lines(output_names)} output_names.txt
        cp ~{write_tsv(output_files)} output_files.tsv

        files_to_json.py \
            -n output_names.txt \
            -f output_files.tsv \
            -j ~{identifier}.~{output_type}_outputs.json

        upload_outputs.sh \
            -b ~{backend} \
            -i ~{identifier} \
            -t ~{timestamp} \
            -w ~{workflow_name} \
            -v ~{workflow_version} \
            -o ~{output_bucket} \
            -j ~{identifier}.~{output_type}_outputs.json \
            -m ~{identifier}.~{output_type}_outputs.manifest.tsv
    >>>

    output {
        File output_json = "~{identifier}.~{output_type}_outputs.json"
        File output_manifest_tsv = "~{identifier}.~{output_type}_outputs.manifest.tsv"
    }

    runtime {
        docker: "~{runtime_attributes.container_registry}/hifi_solves_tools:1.2.0"
        cpu: 2
        memory: "4 GB"
        disk: "50 GB"
        disks: "local-disk 50 HDD"
        preemptible: runtime_attributes.preemptible_tries
        maxRetries: runtime_attributes.max_retries
        awsBatchRetryAttempts: runtime_attributes.max_retries
        queueArn: runtime_attributes.queue_arn
        zones: runtime_attributes.zones
    }
}
