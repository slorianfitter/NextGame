import pandas as pd

full_data_0_1 = pd.read_csv("../../data/full_data_v0.1.2.csv")

if len(full_data_0_1) <= 100000:
    n = 50000
else:
    n = len(full_data_0_1)/2

 
full_data_0_1_part1 = full_data_0_1.iloc[0:n]
full_data_0_1_part2 = full_data_0_1.iloc[n:]




# Teilen der Daten, weil zu groß fürs speichern im repo

# Speichern der Daten


full_data_0_1_part1.to_csv("../../data/full_data_0_1_part1.csv", index=False)
full_data_0_1_part2.to_csv("../../data/full_data_0_1_part2.csv", index=False)
print("Teilung abgeschlossen!!!")