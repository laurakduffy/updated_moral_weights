import os
import pandas as pd
from gsheets import Sheets 
import csv

def clean_csv(unclean_csv, clean_csv_name):
    with open(unclean_csv, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        with open(os.path.join('inputs', clean_csv_name), 'w', newline='') as fo:
            writer = csv.writer(fo, delimiter=',')
            for idx, row in enumerate(reader):
                new_row = []
                if idx == 0:
                    writer.writerow(row)
                else:
                    for i, col in enumerate(row):
                        if type(col) == str:
                            new_row.append(col.strip())
                        else:
                            new_row.append(col)
                    writer.writerow(new_row)

def download_csv(url, output_str):
    s = sheets.get(url)
    name = os.path.join('inputs', "Unclean {}.csv".format(output_str))
    s.to_csv(make_filename=name)
    c_name = "{}.csv".format(output_str)
    clean_csv(name, c_name)
    os.remove(os.path.join('inputs', "Unclean {}.csv".format(output_str)))

sheets = Sheets.from_files('~/google_drive_api_secrets.json', '~/google_drive_api_storage.json')

neurons_url = "https://docs.google.com/spreadsheets/d/1JPydsJPzUmkY4l4MPiULJ-BVOsoMVglsJND2EALLoxY/edit#gid=0"
download_csv(neurons_url, "Neuron Count Data")

qualitative_url = "https://docs.google.com/spreadsheets/d/1vWa-dCnPUN24SZ3HzwOYOgWcloL3M7GZSdBcK11PBqI/edit#gid=0"
download_csv(qualitative_url, "Qualitative Data")

