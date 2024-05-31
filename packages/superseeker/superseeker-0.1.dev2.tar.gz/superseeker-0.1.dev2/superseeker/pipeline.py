# superseeker/pipeline.py
import subprocess
from .data_manipulation import (
    vcf_to_pyclone_input,
    pyclone_to_vcf,
    identify_evolution,
    make_dot_files
)

def run_pipeline(patient, vcf_file, facets_dir='', patient_sex='', restarts=100, clusters=10, cn_neutral=False, cn_override=False, germfilter=True):
    output_dir = f'{patient}'
    
    # Convert VCF to PyClone input
    pyclone_input_file = f'{output_dir}/{patient}.pyclone_input.tsv'
    vcf_to_pyclone_input(patient, vcf_file, facets_dir, pyclone_input_file, patient_sex, cn_neutral, cn_override, germfilter)
    
    # Run PyClone
    clustered_file = f'{output_dir}/{patient}.pyclone.clustered.tsv'
    subprocess.run([
        'pyclone-vi', 'fit', '-i', pyclone_input_file, '-o', f'{output_dir}/{patient}.h5',
        '-d', 'beta-binomial', '-r', str(restarts), '-c', str(clusters)
    ])
    subprocess.run([
        'pyclone-vi', 'write-results-file', '-i', f'{output_dir}/{patient}.h5', '-o', clustered_file
    ])
    
    # Add PyClone clusters to VCF
    clustered_vcf_file = f'{output_dir}/{patient}.somatic.clustered.vcf'
    pyclone_to_vcf(vcf_file, clustered_file, clustered_vcf_file)
    
    # Make graphical representation of clustering
    cluster_lines_pdf = f'{output_dir}/{patient}.cluster_lines.pdf'
    subprocess.run(['Rscript', 'superseeker/plot_clusters.R', patient, clustered_vcf_file, cluster_lines_pdf])
    
    # Run SuperSeeker
    subclones_vcf = f'{output_dir}/{patient}.subclones.vcf'
    subprocess.run(['superseeker', clustered_vcf_file, '>', subclones_vcf])
    
    # Make a visual representation of the trees found
    tmp_graph_files = f'{output_dir}/tmp_graph_files'
    make_dot_files(subclones_vcf, tmp_graph_files)
    subprocess.run(['dot', '-Tpdf', tmp_graph_files, '-o', f'{output_dir}/{patient}.solutions.pdf'])
    
    # Extract SuperSeeker stats
    stats_file = f'{output_dir}/{patient}.stats.txt'
    evolution_file = f'{output_dir}/{patient}.evolution.txt'
    identify_evolution(stats_file, evolution_file)
    
    print("ALL DONE!")
