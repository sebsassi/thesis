import json
import argparse

import matplotlib.pyplot as plt
import numpy as np

from dd_limits import DDLimits

def experiment(string: str):
    name, year, interaction = string.split(":")
    return (name, int(year), interaction)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("experiments", type=experiment, nargs="*", help="experiment in format <name>:<year>:<interaction>")
    args = parser.parse_args()

    limits = DDLimits()
    limits.export_data_and_bibtex_citations(*args.experiments)
