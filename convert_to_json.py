import io
import json
import os

import pandas as pd
import pdfplumber

directory = "./results"
files = os.listdir(directory)


def convert_to_json(filename):
    json_dir = "./json"
    if not os.path.isdir(json_dir):
        os.makedirs(json_dir)

    try:
        with pdfplumber.open(f"./results/{filename}") as pdf:
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                for table in page_tables:
                    tables.append(table)

        result = {}
        for table in tables:
            buf = io.StringIO()
            df = pd.DataFrame(table[1:], columns=table[0])
            df.columns = [
                col.replace("\n", " ").replace("\r", " ") for col in df.columns
            ]
            df.dropna(how="all", inplace=True)
            df.to_csv(buf, index=False)
            buf.seek(0)

            # Converting to JSON
            csv_df = pd.read_csv(buf, dtype=str)
            csv_df.set_index("Exam Roll No.", inplace=True)

            for roll_no, row in csv_df.iterrows():
                roll_dict = {}
                for col_name, value in row.items():
                    if col_name == "Exam Roll No.":
                        continue
                    snake_case_name = col_name.lower().replace(" ", "_")
                    if pd.isna(value):
                        value = "-"
                    roll_dict[snake_case_name] = value
                result[str(roll_no)] = roll_dict

        with open(f"{json_dir}/{filename.split('.')[0]}.json", "w") as f:
            json.dump(result, f, indent=4)

    except Exception as e:
        print(f"Unable to convert {filename}: {e}")


for filename in files:
    convert_to_json(filename)
