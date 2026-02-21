
# Cui et al. (2024) - Static Analysis FPs & FNs

## Overview
This folder contains Java code samples extracted from the research by **Cui et al. (2024)** [1]. The study investigates the root causes and input characteristics that lead to **False Positives (FP)** and **False Negatives (FN)** in three major static analyzers: **PMD, SpotBugs, and SonarQube**.

## Dataset Significance
The samples are categorized into three groups:
1. **Historical Issues (01–14):** Real-world bugs or false alarms reported by users and confirmed by the tool developers.
2. **Metamorphic Mutations (15–18):** Semantic-preserving code transformations used to test the consistency of the analyzers.
3. **Proof-of-Concept Weaknesses (19–22):** Specifically crafted examples demonstrating fundamental limitations in analysis modules like data-flow and symbolic execution.

## Mapping & Ground Truth Table

| Global ID | Original Reference | Category / Characteristic | Ground Truth | Tool & Issue ID |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Figure 3(a) | Scope Analysis Limitation | False Positive (FP) | PMD #1738 |
| **02** | Figure 3(b) | Missing Whitelist Cases | False Positive (FP) | SonarJava-3804 |
| **03** | Figure 3(c) | Boolean Logic / Scope | False Positive (FP) | PMD #3284 |
| **04** | Figure 3(d) | Type Resolution | False Positive (FP) | PMD #2976 |
| **05** | Figure 3(e) | Data-flow Analysis (Nested) | False Negative (FN) | PMD #1749 |
| **06** | Figure 3(f) | Symbolic Execution Error | False Positive (FP) | SonarJava-3619 |
| **07** | Figure 5(a) | Annotations (Lombok) | False Positive (FP) | SonarJava-3320 |
| **08** | Figure 5(b) | Standard Libraries | False Positive (FP) | PMD #3148 |
| **09** | Figure 5(c) | Nested Classes | False Positive (FP) | PMD #3468 |
| **10** | Figure 5(d) | Same Identifiers | False Positive (FP) | PMD #1474 |
| **11** | Figure 5(e) | Complex Expressions | False Negative (FN) | PMD #2140 |
| **12** | Figure 5(f) | Initialization/Assignments | False Positive (FP) | PMD #3114 |
| **13** | Figure 5(g) | Lambda Expressions | False Positive (FP) | PMD #1723 |
| **14** | Figure 5(h) | Modifiers (Final) | False Negative (FN) | SpotBugs-1764 |
| **15** | Table 3(a) | Mutation: Nested Class | Semantic Neutral | - |
| **16** | Table 3(b) | Mutation: Lambda | Semantic Neutral | - |
| **17** | Table 3(c) | Mutation: Identifiers | Semantic Neutral | - |
| **18** | Table 3(d) | Mutation: Equivalence | Semantic Neutral | - |
| **19** | Figure 6(a) | PoC: Resource Hoisting | False Positive (FP) | PMD CloseResource |
| **20** | Figure 6(b) | PoC: Global Constant | False Negative (FN) | SonarQube S2589 |
| **21** | Figure 6(c) | PoC: Private Constructor | False Positive (FP) | SonarQube S2384 |
| **22** | Figure 6(d) | PoC: Instance Method | False Negative (FN) | SonarQube S2259
