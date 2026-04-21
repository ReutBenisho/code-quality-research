
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
| **51** | Derived from [CWE190_..._250319](https://samate.nist.gov/SARD/test-cases/250319/versions/1.0.0) | CWE-190 | Integer Overflow | **Vulnerable** | Incresing short max value, causing overflow. |
| **52** | Derived from [CWE190_..._250319](https://samate.nist.gov/SARD/test-cases/250319/versions/1.0.0) | CWE-190 | Integer Overflow | **Patched (Safe)** | Incresing short value in int type, not causing overflow. |
