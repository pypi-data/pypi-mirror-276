#!/bin/bash
#SBATCH --job-name=rfmix_simu
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=jbenja13@jh.edu
#SBATCH --partition=shared,bluejay
#SBATCH --nodes=1
#SBATCH --array=11,21
#SBATCH --cpus-per-task=1
#SBATCH --mem=50gb
#SBATCH --output=rfmix_output.log
#SBATCH --time=72:00:00

echo "**** Job starts ****"
date

echo "**** JHPCE info ****"
echo "User: ${USER}"
echo "Job id: ${SLURM_JOBID}"
echo "Job name: ${SLURM_JOB_NAME}"
echo "Node name: ${SLURM_NODENAME}"
echo "Hostname: ${HOSTNAME}"
echo "Task id: ${SLURM_ARRAY_TASK_ID}"

## List current modules for reproducibility

module list

## Edit with your job command

echo "**** Run RFMix ****"
SOFTWARE="/dcs05/lieber/hanlab/jbenjami/opt/rfmix"
REF="../../../inputs/vcf_ref/_m"

echo "Chromosome: 21"

$SOFTWARE/rfmix \
    -f ../../_m/simulated_admixed.vcf.gz \
    -r $REF/1kGP_high_coverage_Illumina.chr21.filtered.SNV_INDEL_SV_phased_panel.snpsOnly.eur.afr.vcf.gz \
    -m $REF/samples_id2 \
    -g $REF/genetic_map38 \
    -o chr21 \
    --chromosome=chr21

echo "**** Job ends ****"
date
