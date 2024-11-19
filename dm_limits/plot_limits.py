import json
import argparse

import matplotlib.pyplot as plt
import numpy as np
import cycler

from dd_limits import DDLimits

class LimitPlot:
    def __init__(self, title):
        self.fig, self.ax = plt.subplots()
        self.ax.set_title(title)
        colors = [plt.get_cmap("tab10")(i) for i in range(10)]
        cyc = cycler.cycler(color=colors)*cycler.cycler(linestyle=["-", ":", "--", "-."])
        self.ax.set_prop_cycle(cyc)
    
    def add_experiment(self, values, label):
        self.ax.loglog(values[:,0], values[:,1], label=label)
        self.ax.legend()

def experiment(string: str):
    name, year, interaction = string.split(":")
    return (name, int(year), interaction)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("experiments", type=experiment, nargs="*", help="experiment in format <name>:<year>:<interaction>")
    args = parser.parse_args()

    limit_plots = {
        "SI": LimitPlot("SI"),
        "SDp": LimitPlot("SDp"),
        "SDn": LimitPlot("SDn")
    }
    
    limits = DDLimits()
    for exp in args.experiments:
        try:
            values, label, year = limits.find_data(exp[2], exp[0], exp[1])
        except RuntimeError:
            print(f"Warning: no data found for {exp}")
        interaction = exp[2]
        limit_plots[interaction].add_experiment(values, f"{label} {year}")
    
    plt.show()
