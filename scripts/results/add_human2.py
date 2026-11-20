import csv
import json

def update_json_with_human2(json_path, csv_path, output_path):
    with open(json_path, 'r', encoding="utf-8-sig") as f:
        data = json.load(f)

    with open(csv_path, 'r', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Evaluator'] != 'Human3':
                continue
            raw_name = row['Record'].strip()
            
            key = raw_name
            for ext in ['.cpp', '.java', '.py']:
                if key.endswith(ext):
                    key = key[:-len(ext)]
                    break

            if key in data:
                try:
                    readability = int(row['Readability'])
                    understandability = int(row['Understandability'])
                    maintainability = int(row['Maintainability'])
                except ValueError:
                    readability = float(row['Readability'])
                    understandability = float(row['Understandability'])
                    maintainability = float(row['Maintainability'])

                human3_obj = {
                    "readability_score": readability,
                    "understandability_score": understandability,
                    "maintainability_score": maintainability,
                    "functional_classification": "",
                    "security_classification": "",
                    "cwe_id": "",
                    "reasoning": ""
                }

                new_item = {}
                for k, v in data[key].items():
                    new_item[k] = v
                    if k == "Human2":
                        new_item["Human3"] = human3_obj

                if "Human3" not in new_item:
                    new_item["Human3"] = human3_obj

                data[key] = new_item

            else:
                print(f"Warning: The key '{key}' (from '{raw_name}') was not found in the JSON file.")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Updated JSON file saved to: {output_path}")

json_file = 'Results.json'
csv_file = 'human_scores.csv'
output_file = 'Results.json'

update_json_with_human2(json_file, csv_file, output_file)