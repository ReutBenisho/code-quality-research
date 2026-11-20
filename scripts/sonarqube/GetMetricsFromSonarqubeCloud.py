import os
import json
import requests
from urllib.parse import quote

SONAR_URL = "https://sonarcloud.io"
SONARCLOUD_TOKEN = "69bdd4896cbf768edf05e78f3917bb581ad71a52"
ORGANIZATION = "ReutBenisho"
PROJECT_KEY = "ReutBenisho_code-quality-research"
TARGET_DIRECTORIES = [
    {"path": r"dataset"}
]
AUTH = (SONARCLOUD_TOKEN, "")

RESULTS_FILE = "Results.json"

def rating_to_score_100(rating_val):
    mapping = {
        "1.0": 100.0,  # A
        "2.0": 80.0,   # B
        "3.0": 60.0,   # C
        "4.0": 40.0,   # D
        "5.0": 20.0    # E
    }
    return mapping.get(str(rating_val), 100.0)


def calculate_readability_100(cognitive_complexity):
    try:
        complexity = float(cognitive_complexity)
        score = 100.0 - (complexity * 5.0)
        return max(0.0, score)
    except (ValueError, TypeError):
        return 100.0


def calculate_maintainability_100(debt_ratio, rating_val):
    if debt_ratio is not None:
        try:
            return max(0.0, 100.0 - float(debt_ratio))
        except ValueError:
            pass
    return rating_to_score_100(rating_val)

def discover_files():
    found_files = []

    for target in TARGET_DIRECTORIES:
        base_dir = target["path"]

        if not os.path.exists(base_dir):
            print(f"Warning: Directory does not exist locally: {base_dir}")
            continue

        for root, _, files in os.walk(base_dir):
            for file in files:
                full_local_path = os.path.join(root, file)
                normalized_path = full_local_path.replace("\\", "/")
                found_files.append(normalized_path)

    return found_files

def get_file_metrics(file_path):
    encoded_file_path = quote(file_path, safe='')
    file_key = f"{PROJECT_KEY}:{encoded_file_path}"
    
    metrics_list = "sqale_rating,security_rating,cognitive_complexity,bugs,vulnerabilities"
    url = f"{SONAR_URL}/api/measures/component?component={file_key}&metricKeys={metrics_list}&organization={ORGANIZATION}"

    try:
        response = requests.get(url, auth=AUTH)
        response.raise_for_status()
        res_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while calling SonarQube Cloud API for {file_path}: {e}")
        return None

    measures = {}
    for m in res_data.get('component', {}).get('measures', []):
        measures[m['metric']] = m.get('value')
    
    issues_url = f"{SONAR_URL}/api/issues/search?components={file_key}&types=VULNERABILITY&organization={ORGANIZATION}"
    cwe_id = "None"
    
    try:
        issues_res = requests.get(issues_url, auth=AUTH).json()
        for issue in issues_res.get('issues', []):
            for tag in issue.get('tags', []):
                if tag.lower().startswith('cwe'):
                    cwe_id = tag.upper()
                    break
            if cwe_id != "None":
                break
    except Exception as e:
        print(f"Warning: couldn't get tags of CWE for {file_path}: {e}")

    readability = calculate_readability_100(measures.get("cognitive_complexity", 0))
    maintainability = calculate_maintainability_100(
        measures.get("sqale_debt_ratio"), 
        measures.get("sqale_rating")
    )
    security_score = rating_to_score_100(measures.get("security_rating", "1.0"))
    
    bugs_count = int(measures.get("bugs", 0))
    vulnerabilities_count = int(measures.get("vulnerabilities", 0))
    
    return {
        "readability_score": readability,
        "understandability_score": readability,  
        "maintainability_score": maintainability,
        "functional_classification": "Code Smell/Bug" if bugs_count > 0 else "Clean",
        "security_classification": str(security_score),  
        "cwe_id": cwe_id,
        "reasoning": (
            f"SonarQube Cloud detected Cognitive Complexity={measures.get('cognitive_complexity', 0)}, "
            f"Bugs={bugs_count}, Vulnerabilities={vulnerabilities_count}."
        )[:400]  
    }


if __name__ == "__main__":
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: Could not find '{RESULTS_FILE}'. Please ensure the file exists in the directory.")
        exit(1)

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        try:
            results_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error reading {RESULTS_FILE}: {e}")
            exit(1)

    files_to_analyze = discover_files()
    print(f"Found {len(files_to_analyze)} files to process.")

    updated_count = 0
    for path in files_to_analyze:
        file_name = os.path.basename(path)
        entry_key, _ = os.path.splitext(file_name)

        if entry_key not in results_data:
            print(f"[WARNING] Key '{entry_key}' (from file '{file_name}') not found in {RESULTS_FILE}. Skipping...")
            continue

        metrics = get_file_metrics(path)
        if metrics:
            results_data[entry_key]["Sonarqube"] = metrics
            print(f"Updated SonarQube results for: {entry_key}")
            updated_count += 1

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results_data, f, indent=4, ensure_ascii=False)
        
    print(f"\n--- Process finished! Successfully updated {updated_count} entries in {RESULTS_FILE} ---")