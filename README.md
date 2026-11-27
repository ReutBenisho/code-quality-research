# Evaluating Source Code Quality and Security with Large Language Models vs. Static Analysis

[![License: MIT (original materials only)](https://img.shields.io/badge/License-MIT%20(original%20materials%20only)-yellow.svg)](LICENSE)
![Software Engineering](https://img.shields.io/badge/Domain-Software%20Engineering-blue)
![Code Quality](https://img.shields.io/badge/Topic-Code%20Quality-brightgreen)
![LLM Evaluation](https://img.shields.io/badge/Topic-LLM%20Evaluation-purple)
![Static Analysis](https://img.shields.io/badge/Topic-Static%20Analysis-orange)
![Vulnerability Detection](https://img.shields.io/badge/Topic-Vulnerability%20Detection-red)

**Replication package** for the empirical study *“Evaluating Source Code Quality and Security with Large Language Models vs. Static Analysis: A Comparative Study.”* This repository contains the code corpus, human annotations, model assessments, SonarQube Cloud baseline data, and analysis artifacts used to compare automated assessments with expert ground truth.

## Study at a glance

The study compares four commercial large language model assistants—OpenAI ChatGPT, Anthropic Claude, Google Gemini, and Microsoft GitHub Copilot—with SonarQube Cloud and human assessments. The corpus comprises 300 code snippets across Java, C++, and Python. LLM assessments were obtained in zero-shot, web-based, stateless runs (August 2026, as recorded for the study). Human evaluations provide the reference annotations; SonarQube Cloud serves as a conventional static-analysis baseline.

The repository is intended to make the study materials and analysis traceable and reusable. The precomputed outputs are included so that statistical summaries and figures can be inspected without repeating external model or SonarQube runs.

## Evaluation schema

Each snippet is evaluated along five dimensions:

| Dimension | Scale / labels | Interpretation |
| --- | --- | --- |
| Readability | 0–100 | Ease of reading and following the code. |
| Understandability | 0–100 | Ease of understanding the logic, intent, and complexity. |
| Maintainability | 0–100 | Structure and suitability for future modification. |
| Functional correctness | `Correct`, `Partially Correct`, or `Buggy` | Whether the implementation behaves as intended. |
| Security | `Safe` or `Vulnerable`, with CWE identifier(s) where applicable | Presence and classification of potential security weaknesses using MITRE CWE references. |

For model assessments, the prompt and strict JSON response schema are documented in [`docs/prompt.txt`](docs/prompt.txt). Human annotations are retained separately in the results data. SonarQube reports native measures and classifications; where the analysis maps these onto the study’s scoring fields, those mapped values should be interpreted as a baseline proxy rather than as scores directly equivalent to human or LLM judgments.

## Repository structure

```text
.
├── data/
│   └── annotations/              # Human annotation source files (CSV)
├── dataset/                      # Code snippets; numbered Java, C++, and Python files
├── docs/
│   ├── prompt.txt                # Zero-shot evaluation prompt and JSON schema
│   └── sonarqube-server.md       # Notes for the optional local SonarQube setup
├── notebooks/
│   └── ResultsNotebook.ipynb     # Exploratory results notebook
├── results/
│   ├── Results.json              # Consolidated snippet metadata and evaluator results
│   ├── ResultsSample.json        # Smaller example of the consolidated JSON schema
│   ├── charts/                   # Analysis scripts and generated visualizations
│   └── tables/                   # Exported statistical summaries
├── scripts/
│   ├── results/                  # Human annotation and average-score processing
│   ├── sonarqube/                # SonarQube Cloud/local metric retrieval scripts
│   └── num_of_lines.py           # Dataset line-count utility
├── sonar-project.properties      # SonarQube project configuration
└── sonar-project-server.properties
```

### Data and outputs

- **Code corpus (`dataset/`)** — numbered source files for Java (`*_java.java`), C++ (`*_cpp.cpp`), and Python (`*_py.py`). The current collection includes files through the numbered `100_*` examples. The snippets originate from the study corpus and, where applicable, translated variants; per-snippet provenance is recorded in the `metadata` object in `results/Results.json`.
- **Human annotations (`data/annotations/`)** — source CSVs include `human_scores.csv` and `Grades_for_Human2.csv`. Consolidated snippet results retain evaluator-specific entries (e.g., `Human1`, `Human2`, `Human3`) and a metadata section. Where supplied, human numeric scores can be combined into consolidated reference values; see `scripts/results/` and the notebook for the processing workflow. Do not treat a consolidated value as an independent fourth evaluator.
- **LLM assessments** — the consolidated `results/Results.json` contains the per-snippet responses for ChatGPT, Claude, Gemini, and GitHub Copilot, including the three numeric dimensions, classifications, CWE values, and rationale. These are stored results from the August 2026 web-based stateless runs, not outputs generated by the replication scripts. `results/ResultsSample.json` illustrates the record format.
- **SonarQube baseline** — the consolidated JSON includes SonarQube entries. `scripts/sonarqube/GetMetricsFromSonarqubeCloud.py` retrieves measures and issue/CWE information from SonarQube Cloud; the corresponding local-server script and configuration are provided for an optional local setup. Re-running these integrations requires an accessible project and credentials and may not reproduce the original scan exactly.
- **Analysis artifacts (`results/charts/`, `results/tables/`)** — analysis scripts flatten the nested results, harmonize evaluator labels for comparisons, and generate figures and summary tables. The summary analysis covers quality scores, language variation, vulnerability detection, and functional-defect flags. The statistical measures used across the analyses include MAE and Delta-MAE for numeric score comparisons, Spearman rank correlation for agreement, and Precision, Recall, false-negative rate (FNR), and F1 for classification/detection comparisons. The checked-in `summary_statistics_comprehensive.csv` provides an example of exported aggregate results.

## Getting started and replication

### Requirements

- Python 3.10 or later is recommended.
- Python packages used by the analysis and notebook: `pandas`, `numpy`, `matplotlib`, and `seaborn`. The SonarQube Cloud retrieval script additionally uses `requests`.
- Jupyter Notebook/Lab is needed only to run the notebook.

The repository does not currently define a pinned Python dependency file. Create an isolated environment and install the packages as follows:

```bash
# Clone the repository and enter it
git clone https://github.com/ReutBenisho/code-quality-research.git
cd code-quality-research

# Create and activate a virtual environment
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install pandas numpy matplotlib seaborn requests jupyter
```

### Reproduce the summary figures and table

The summary script expects a file named `Results.json` in its **current working directory**. From the repository root, copy the consolidated input there, then execute the script:

```bash
cp results/Results.json Results.json
python results/charts/1_Summary/analyze_results.py
```

The script writes multiple PNG charts and `summary_statistics.csv` under `output_charts/` relative to the current working directory. On Windows, use `copy results\Results.json Results.json` instead of `cp`. The generated `Results.json` copy and `output_charts/` are local working artifacts; the checked-in source data remains under `results/`.

### Run the results notebook

From the repository root, with the environment activated and the working `Results.json` copy in place:

```bash
jupyter lab notebooks/ResultsNotebook.ipynb
```

Run the notebook cells in order to load and flatten the consolidated data, inspect grouped summaries, and reproduce the notebook’s exploratory plot. The notebook and the standalone summary script are complementary analysis entry points; the precise artifacts produced depend on which is run.

### Inspect or rerun SonarQube collection (optional)

The precomputed baseline is already present in `results/Results.json`; no SonarQube account is required to reproduce the included charts from that file. To collect fresh Cloud data, configure the project as appropriate and provide a token via an environment variable—never commit credentials:

```bash
export SONAR_TOKEN="<your-sonarqube-token>"  # macOS/Linux
python scripts/sonarqube/GetMetricsFromSonarqubeCloud.py
```

The Cloud script reads and updates a `Results.json` file in the current directory and accesses the configured SonarQube project. Run it only on a backup or working copy of the results file, and confirm the project key, organization, and scan state before using it. For local SonarQube usage, consult [`docs/sonarqube-server.md`](docs/sonarqube-server.md) and the server properties file. External scans can change over time due to analyzer versions, rules, project configuration, and service updates, so the checked-in scan is the reproducibility reference for the published analysis.

### Statistical interpretation

Numeric agreement measures (MAE, Delta-MAE, and Spearman correlation) apply to the scored dimensions and should be interpreted alongside the study’s chosen aggregation and reference values. Detection metrics require an explicit positive class and mapping of labels; for example, `Partially Correct` is grouped with functional issue flags in the summary analysis. Report the label mapping and denominator when comparing Precision, Recall, FNR, or F1. CWE strings are multi-label annotations and should not be treated as a single mutually exclusive class without an explicit rule.

## Citation

Please cite the study and this replication package when using these materials. Replace the bracketed fields with the final publication details when available:

```bibtex
@misc{benisho_code_quality_llm_static_analysis,
  title        = {Evaluating Source Code Quality and Security with Large Language Models vs. Static Analysis: A Comparative Study},
  author       = {Benisho, Reut},
  year         = {2026},
  howpublished = {Replication package},
  url          = {https://github.com/ReutBenisho/code-quality-research},
  note         = {Add venue, volume, pages, and DOI when published}
}
```

## License and reuse

The MIT license in [`LICENSE`](LICENSE) applies **only to original project materials owned by the copyright holder**, such as original scripts, documentation, and original analysis code or presentation artifacts. It does not license the repository as a whole. In particular, third-party code snippets and article excerpts, externally sourced datasets, and outputs governed by third-party service terms are excluded unless their respective rights holders have separately granted permission. Check source notices and provenance before reusing those materials. If an item has its own license or notice, that item-specific license or notice governs.

## Acknowledgments and provenance

The corpus draws on prior software-engineering studies and includes source provenance in snippet metadata. The existing project documentation references work by Cui et al. (2024), Simões and Venson (2024), Vijayvergiya et al. (2024), and Buse and Weimer (2010). Please consult the source publications and the per-snippet metadata when reusing or redistributing individual code examples; the repository-level license does not supersede third-party rights that may apply to source material.
