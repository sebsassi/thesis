
import numpy as np
import json

def load_limits():
    with open("dm_limits.json", "r") as f:
        return json.load(f)

def make_bibtex_entry(key, entry):
    content = "\n".join(f"    {k} = {{{v}}}," for k, v in entry.items() if k != "type")
    return f"@{entry['type']}{{{key},\n{content}\n}}"

def pretty_print(limit):
    return f"""
experiment: {limit['experiment']}
year: {limit['year']}
exposure: {limit['exposure']['value']} {limit['exposure']['unit']}
target: {limit['target']}
data: {" ".join(d['interaction'] for d in limit['data'])}
    """

class DDLimits:
    def __init__(self):
        self.dm_limits = load_limits()
    
    def find_data(self, interaction, experiment, year=None):
        dd_limits = self.dm_limits["direct detection limits"]
        if year is None:
            try:
                limit = max(filter(lambda l: l["experiment"] == experiment, dd_limits), key=lambda l: l["year"])
            except ValueError:
                raise ValueError(f"No data found for combination experiment = {experiment}")
        else:
            try:
                limit = next(filter(lambda l: l["experiment"] == experiment and l["year"] == year, dd_limits))
            except StopIteration:
                raise ValueError(f"No data found for combination experiment = {experiment} and year = {year}")
        try:
            data = next(filter(lambda d: d["interaction"] == interaction and d["type"] == "upper limit", limit["data"]))
        except StopIteration:
            raise RuntimeError(f"No data found for interaction: {interaction}, experiment: {experiment}, year: {limit['year']}")
        except KeyError:
            raise KeyError(f"No key 'interaction' found for experiment: {experiment}, year: {limit['year']}")
        values = np.array(data["values"])
        return values, limit["label"], limit["year"]
    
    def export_data_and_bibtex_citations(self, *args):
        print(args)
        dd_limits = self.dm_limits["direct detection limits"]
        bibliography = self.dm_limits["bibliography"]
        bibtex_entries = []
        for experiment, year, interaction in args:
            for limit in dd_limits:
                if (limit["experiment"] == experiment and limit["year"] == year):
                    label = limit["label"].replace(" ", "_")
                    for data in limit["data"]:
                        if (data["interaction"] == interaction):
                            info = None if data["info"] is None else data["info"].replace(" ", "_").replace("/", "_")
                            values = np.array(data["values"])
                            if info is None:
                                fname = f"{label}_{year}_{interaction}.dat"
                            else:
                                fname = f"{label}_{year}_{interaction}_{info}.dat"
                            np.savetxt(fname, values)
                            citation_key = data["citation"]
                            try:
                                bibtex_entries.append(make_bibtex_entry(citation_key, bibliography[citation_key]))
                            except KeyError as e:
                                print(f"Warning: no citation for {limit['label']}, {limit['year']}, {data['interaction']}, {data['info']}")
        
        with open("dm_limits_export.bib", "w")as f:
            f.write("\n\n".join(bibtex_entries))
    
    def find_limits_for(self, experiment=None, year=None):
        if experiment is None and year is None: return

        limits = self.dm_limits["direct detection limits"]
        if experiment is not None:
            limits = filter(lambda l: l["experiment"] == experiment, limits)
        if year is not None:
            limits = filter(lambda l: l["year"] == year, limits)
        
        return limits
        