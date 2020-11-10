
## Version 0.6 (May 6, 2020)
* added hmm_db/genome_lengths.tsv
* publication release

genome_db
|
|-checkv_circular.tsv
  metadata for 76,262 circular viral contigs
|-checkv_genbank.tsv
  metadata for 24,834 genbank genomes
|-checkv_clusters.tsv
  information for 52,142 non-redundant genomes
  these are clustered at 95% ANI over 85% the length of both genomes
  clustering performed using a greedy centroid-based algorithm
  the cluster representatives are used by CheckV for mapping
|-checkv_reps.faa
  proteins for 52,142 representative genomes
|-checkv_reps.fna
  genomic sequences for 52,142 representative genomes
  terminal repeat trimmed for circular viral contigs
|-checkv_reps.tsv
  basic info on 52,142 representative genomes
|-checkv_error.tsv
  lookup table used to report error and assign confidence levels to CheckV completeness estimates

hmm_db
|
|-checkv_hmms.tsv
  metadata for 15,959 CheckV HMMs
|-checkv_hmms
  directory of HMMs
  each file contains 200 HMMs
  HMMs split into multiple files for improved parallelization
|-genome_lengths.tsv
  genome length statistics for each HMM
