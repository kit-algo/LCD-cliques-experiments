#!/usr/bin/env python3



plt_styles = {
        "GCE M" : ('#e41a1c', '+'),
        "GCE L" : ('#377eb8', 'x'),
        "TwoPhaseL" : ('#ffaa00', '*'),
        "LFMLocal": ('#984ea3', 'p'),
        "LFMLocal1.5": ('#ff5500', 'p'),
        "PRN" : ('#4daf4a', 's'),
        "LTE" : ('#a65628', 'v'),
        "LocalT": ('#a6cee3', '<'),
        "TCE": ('#f781bf', '>'),
        "BFS" :  ('#000000', '1'),
        "Cl" : ('#555555', 'D'),
        "Cl+GCE M" : ('#e41a1c', '+'),
        "Cl+GCE L" : ('#377eb8', 'x'),
        "Cl+TwoPhaseL" : ('#ffaa00', '*'),
        "Cl+LFM": ('#984ea3', 'p'),
        "Cl+LFM1.5": ('#ff5500', 'p'),
        "Cl+PRN" : ('#4daf4a', 's'),
        "Cl+LTE" : ('#a65628', 'v'),
        "Cl+LocalT": ('#a6cee3', '<'),
        "Cl+TCE": ('#f781bf', '>'),
        "Louvain" : ('#55557f', '2'),
        "Infomap" : ('#aaaa00', '3')
}

basic_algorithms = ["GCE M", "GCE L", "TwoPhaseL", "LFMLocal", "PRN", "LTE", "LocalT", "TCE", "BFS", "Cl"]
clique_algorithms = ["Cl+GCE M", "Cl+GCE L", "Cl+TwoPhaseL", "Cl+LFM", "Cl+PRN", "Cl+LTE", "Cl+LocalT", "Cl+TCE", "BFS", "Infomap"]
dashed_algorithms = ['BFS', 'Cl', 'Louvain', 'Infomap']
