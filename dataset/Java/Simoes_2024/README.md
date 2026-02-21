
# Simões & Venson (2024) - LLMs vs. SonarQube Maintainability

## Overview
This folder contains Java samples extracted from the comparative study by **Simões & Venson (2024)**. The research evaluates the proficiency of LLMs (GPT-3.5 Turbo and GPT-4o) in assessing overall code quality and maintainability compared to **SonarQube's** metrics.

## Research Focus
The study uses the **Maintainability Rating (A–E)** from SonarQube as a baseline and compares it with AI-generated scores (0–100). A key finding of this study is that **GPT-4o tends to be overly optimistic**, often assigning high scores to low-quality code (Sonar Rating E).

## Mapping & Ground Truth Table

| Global ID | Project Source | Original Ref | Category | Sonar Rating | AI Findings (GPT-3.5) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **23** | Quarkus | Listing 1 | Empty Class | B | Score: 50/100 (Penalized for lack of logic) |
| **24** | Quarkus | Listing 2 | Empty Class | B | Score: 50/100 (Penalized for lack of logic) |
| **25** | Quarkus | Listing 5 | Thread Safety | D | Score: 85/100 (Missed complex concurrency risks) |
| **26** | Shattered Pixel Dungeon | Listing 8 | Deep Inheritance | E | Score: 90/100 (Context-blind to project structure) |
| **27** | Shattered Pixel Dungeon | Listing 9 | Magic Numbers | E | Score: 85/100 (Identified magic numbers but missed inheritance depth) |

## Usage for AI Evaluation
These samples test whether the AI evaluates code based on **Readability** (qualitative) or **Repair Cost** (quantitative like SonarQube). Use these to check for "optimism bias" in newer LLM models.
