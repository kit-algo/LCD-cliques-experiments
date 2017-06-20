#!/bin/bash

fb_graph_path="~/graphs/facebook100/"

directories="output_lfr-dj-uw output_lfr-ol-uw output_lfr-weighted output_fb-dorm output_fb-dorm-year"

for d in $directories
do
	mkdir $d
done

./gen_lfr.py output_lfr-dj-uw/
./gen_ol_lfr.py output_lfr-ol-uw/
./gen_weighted_lfr.py output_lfr-weighted/
./convert_fb.py $fb_graph_path output_fb-dorm/ dorm
./convert_fb.py $fb_graph_path output_fb-dorm-year/ dorm year

for d in $directories
do
	echo executing $d
	./execute_algorithms.py $d
done

for d in $directories
do
	echo evaluating $d
	./evaluate_communities.py $d
done

mkdir plots_fb-dorm
./plot.py output_fb-dorm/ plots_fb-dorm/

mkdir plots_fb-dorm-year
./plot.py output_fb-dorm-year/ plots_fb-dorm-year/

mkdir plots_lfr-dj-uw
./plot_lfr.py output_lfr-dj-uw/ plots_lfr-dj-uw/ '$\mu$'

mkdir plots_lfr-ol-uw
./plot_lfr.py output_lfr-ol-uw/ plots_lfr-ol-uw/ '$O_m$'

mkdir plots_lfr-weighted
./plot_lfr.py output_lfr-weighted/ plots_lfr-weighted/ '$\mu_w$'

./time_table.py output_fb-dorm/ fb_times.tex
./time_table.py output_lfr-ol-uw/ lfr-ol-uw_times.tex
