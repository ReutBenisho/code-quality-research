
# NIST SARD Samples (C++)

## Overview
This folder contains C++ code samples derived from the **NIST Software Assurance Reference Dataset (SARD)**, specifically targeting **CWE-476: NULL Pointer Dereference**. These samples are designed to test an AI's ability to track data flow through C++ references and identify safety checks.

## Methodology
Following the practices described by **Çetin et al. (2024)**, the original SARD templates (specifically from Data Flow Variant 33) have been refined for this research:
1. **Stripping Templates:** All boilerplate metadata headers and preprocessor directives (e.g., `#ifndef OMITBAD`) were removed to prevent the AI from "guessing" the answer based on labels.
2. **Variable Obfuscation:** Variable names and function identifiers were renamed to neutral terms to ensure the model evaluates the underlying logical flow rather than descriptive identifiers.
3. **Logic Isolation:** The snippets were distilled to their core logic to fit within LLM context windows while maintaining the exact vulnerability mechanism verified by NIST.

## Mapping & Ground Truth Table

| Global ID | SARD Reference | CWE | Category | Ground Truth | Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **31** | Derived from CWE476_..._33 | CWE-476 | Null Pointer | **Vulnerable** | Dereference of a NULL pointer through a C++ reference. |
| **32** | Derived from CWE476_..._33 | CWE-476 | Null Pointer | **Patched (Safe)** | Explicit NULL check before dereference (Defensive coding). |

## Usage for AI Evaluation
These samples provide a balanced test case: 
- **Sample 31** tests for **False Negatives** (can the AI find the bug?).
- **Sample 32** tests for **False Positives** (does the AI incorrectly flag a secured code?). 

When prompting Gemini or other LLMs, use the "clean" code versions provided in the files to maintain the integrity of the experiment.
