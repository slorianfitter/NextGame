import pandas as pd

image_and_description_data = pd.read_csv("../data/second_additional_info.csv")


image_and_description_data_angepasst = image_and_description_data.drop(labels="detailed_description", axis=1)

# Teilen der Daten, weil zu groß fürs speichern im repo
# detailed description kann ganz ignoriert werden. SInd teilweise romane. juckt nicht.

# Speichern der Daten


image_and_description_data_angepasst.to_csv("../data/image_and_description_data.csv", index=False)

print("Drop erfolgreich abgeschlossen!!!")