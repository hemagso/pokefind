import csv

with open("../data/pokemon.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    fields = next(reader)
    for data in reader:
        data_dict = dict(zip(fields, data))
        print(data_dict["pokedex_number"], data_dict["name"])

