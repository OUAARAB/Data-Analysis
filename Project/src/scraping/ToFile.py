import csv
import json


def write_into_a_csv_file(csv_file_path: str, field_names: list, data: list):
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_file_path)
        csv_writer.writeheader()

        for row in data:
            csv_writer.writerow(row)

    print(f"The file at the path '{csv_file_path}' has been created or updated.")


def write_into_a_json_file(json_file_path: str, data: list):
    json.dumps(data)
    with open(json_file_path, "w") as json_file:
        json.dump(data, json_file)

    print(f"The file at the path '{json_file_path}' has been created or updated.")
