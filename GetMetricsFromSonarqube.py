import json
import requests

SONAR_URL = "http://localhost:9000"
AUTH = ("admin", "Admin1234!@#$") 
project_key = "code-quality-research"
file_path = "dataset%2FPython%2FExercises_2022%2F95.py"


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
    
    
def get_file_metrics():
    file_key = f"{project_key}:{file_path}"
    
    metrics_list = "sqale_rating,security_rating,cognitive_complexity,bugs,vulnerabilities"
    url = f"{SONAR_URL}/api/measures/component?component={file_key}&metricKeys={metrics_list}"
 
    try:
        response = requests.get(url, auth=AUTH)
        response.raise_for_status()
        res_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error while calling SonarQube API: {e}")
        return None

    print("Finished calling the WEB API")
    measures = {}
    for m in res_data.get('component', {}).get('measures', []):
        measures[m['metric']] = m.get('value')
    
    issues_url = f"{SONAR_URL}/api/issues/search?components={file_key}&types=VULNERABILITY"
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
        print(f"Warning: couldn't get tags of CWE: {e}")

    readability = calculate_readability_100(measures.get("cognitive_complexity", 0))
    maintainability = calculate_maintainability_100(
        measures.get("sqale_debt_ratio"), 
        measures.get("sqale_rating")
    )
    security_score = rating_to_score_100(measures.get("security_rating", "1.0"))
    
    bugs_count = int(measures.get("bugs", 0))
    vulnerabilities_count = int(measures.get("vulnerabilities", 0))
    
    result_json = {
        "readability_score": readability,
        "understandability_score": readability,  
        "maintainability_score": maintainability,
        "functional_classification": "Code Smell/Bug" if bugs_count > 0 else "Clean",
        "security_classification": str(security_score),  
        "cwe_id": cwe_id,
        "reasoning": (
            f"SonarQube detected Cognitive Complexity={measures.get('cognitive_complexity', 0)}, "
            f"Bugs={bugs_count}, Vulnerabilities={vulnerabilities_count}."
        )[:400]  
    }
    
    print(result_json)
    return result_json
    

get_file_metrics()