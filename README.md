Experimental Evaluation of "Local Community Detection based on Small Cliques"
=============================================================================

These are the scripts used for the experimental evaluation of the (open access) paper

Hamann, Michael; Röhrs, Eike; Wagner, Dorothea. 2017. "[Local Community Detection based on Small Cliques](http://www.mdpi.com/1999-4893/10/3/90)." Algorithms 10, no. 3: 90.

To make it possible to reproduce the results presented in our paper we provide all scripts and the full implementation used.

The scripts generate or convert input graphs, execute the algorithms, run the evaluation and generate plots.
The main script to execute everything is `execute_everything.sh`.
Before you execute this, however, you need to ensure a couple of points:

 * NetworKit from https://github.com/kit-algo/LCD-cliques-networkit must be installed such that it can be imported in Python scripts
 * The Facebook graphs from https://archive.org/details/oxford-2005-facebook-matrix must be available in some directory, the path to it can be defined in `execute_everything.sh`.
 * The `binary_networks` and `weighted_networks` LFR implementations from https://sites.google.com/site/andrealancichinetti/files must be compiled and their path entered in `gen_ol_lfr.py` and `gen_weighted_lfr.py`. Note that as of 2017-06-20, the weighted-networks implementation has a bug in the code (which might only exist under certain compilers, but on our systems it definitely is broken) concerning the output of the graph. To fix it, simply apply the patch in `weighted_networks.patch` (e.g. using `patch -p1 < weighted_networks.patch`).
 * The Infomap implementation from http://www.mapequation.org/code.html needs to be installed and the path to it needs to be entered in `execute_algorithms.py`.


Note that the provided scripts generate more graphs and in particular a lot more plots than actually used in the paper.
While the other plots are certainly also interesting, we did not feel they contributed enough value to justify their inclusion in the paper.
The plots actually used in the paper are:

```
plots_lfr-dj-uw/5000-small_F1-Score - seed_plain_avg.pgf
plots_lfr-dj-uw/5000-small_F1-Score - seed_clique_avg.pgf
plots_lfr-dj-uw/5000-big_F1-Score - seed_plain_avg_nolegend.pgf
plots_lfr-dj-uw/5000-big_F1-Score - seed_clique_avg_nolegend.pgf
plots_lfr-dj-uw/5000-big_Conductance_plain_avg.pgf
plots_lfr-dj-uw/5000-big_Conductance_clique_avg.pgf
plots_lfr-dj-uw/5000-big_Size_plain_avg_nolegend.pgf
plots_lfr-dj-uw/5000-big_Size_clique_avg_nolegend.pgf
plots_lfr-dj-uw/5000-big_F1-Score - noseed_plain_avg_nolegend.pgf
plots_lfr-dj-uw/5000-big_F1-Score - noseed_clique_avg_nolegend.pgf
plots_lfr-ol-uw/2000-0.2_F1-Score - seed_plain_avg.pgf
plots_lfr-ol-uw/2000-0.2_F1-Score - seed_clique_avg.pgf
plots_lfr-weighted/5000-big-0.3_F1-Score - seed_plain_avg.pgf
plots_lfr-weighted/5000-big-0.3_F1-Score - seed_clique_avg.pgf
plots_lfr-weighted/5000-big-0.5_F1-Score - seed_plain_avg_nolegend.pgf
plots_lfr-weighted/5000-big-0.5_F1-Score - seed_clique_avg_nolegend.pgf
plots_lfr-weighted/5000-big-0.8_F1-Score - seed_plain_avg_nolegend.pgf
plots_lfr-weighted/5000-big-0.8_F1-Score - seed_clique_avg_nolegend.pgf
plots_fb-dorm/F1-Score - seed_plain_avg.pdf
plots_fb-dorm/F1-Score - seed_clique_avg.pdf
summary.pdf
```

All plots are generated as PGF for direct inclusion into LaTeX and as PDF for direct viewing or inclusion where PGF does not accurately reproduce the PDF (for the plots on the 100 Facebook networks and the summary plot, the labels on the x-axis are unfortunately not properly aligned when using PGF).

Further, the code also generates two tables that are used in our paper:

```
lfr-ol-uw_times.tex
fb_times.tex
```

In case you have any questions concerning these scripts or the paper, feel free to contact [Michael Hamann](michael.hamann@kit.edu) via email or open an issue in this repository.
