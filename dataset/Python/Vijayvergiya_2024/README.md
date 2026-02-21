
# Vijayvergiya et al. (2024) - Python Best Practices (Google AutoCommenter)

## Overview
Python samples focusing on unit testing and maintainability idioms, extracted from the **AutoCommenter** study at Google.

## Research Focus
Testing AI's ability to identify "weak assertions" in Python tests and suggest more robust alternatives that verify error messages.

## Mapping & Ground Truth
| Global ID | Original Reference | Category | AI Recommendation (Ground Truth) |
| :--- | :--- | :--- | :--- |
| **29** | Figure 1 | Unit Testing / Maintainability | Use `self.assertRaisesRegex` instead of `self.assertRaises` to ensure the correct error message is triggered. |

## Usage for AI Evaluation
Evaluate if the AI captures Python-specific testing patterns and "Clean Code" principles for test suites.
