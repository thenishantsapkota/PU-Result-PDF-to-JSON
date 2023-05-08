import io
import json
import os

import pandas as pd
import tabula

directory = "./results"
files = os.listdir(directory)


def convert_to_json(filename):
    try:
        if not os.path.isdir("./json"):
            os.system("mkdir json")

        tables = tabula.read_pdf(
            f"./results/{filename}", pages="all", pandas_options={"dtype": str}
        )

        buf = io.BytesIO()

        df = pd.concat(tables)

        df.columns = [col.replace("\n", "").replace("\r", " ") for col in df.columns]

        df.dropna(how="all", inplace=True)

        df.to_csv(buf, index=False)

        buf.seek(0)
        # Converting to JSON
        csv_df = pd.read_csv(buf)
        csv_df.set_index("Exam Roll No.", inplace=True)

        result = {}
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
        with open(f"./json/{filename.split('.')[0]}.json", "w") as f:
            json.dump(result, f, indent=4)
    except Exception:
        print(f"Unable to convert {filename}")
        pass


for filename in files:
    convert_to_json(filename)
