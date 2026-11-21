# Dataset and snippet provenance

This directory contains numbered source-code snippets in Java, C++, and Python. Filenames follow the pattern `<id>_<language>.<extension>`, for example `1_java.java`, `1_cpp.cpp`, and `1_py.py`. Corresponding records in [`../results/Results.json`](../results/Results.json) use the filename stem as the JSON key (for example, `1_java`).

The `metadata` object in each results record includes provenance fields such as `origin` and `external_reference_url`. The examples below are an orientation guide based on the metadata currently visible in the results file; this is **not a complete snippet inventory**.

| Dataset file(s) | Provenance recorded in results metadata |
| --- | --- |
| `1_java.java` | Origin: `Cui_2024`; reference: Figure 3(a). |
| `2_java.java` | Origin: `Cui_2024`; reference: Figure 3(b). |
| `3_java.java` | Origin: `Cui_2024`; reference: Figure 3(c). |
| `1_cpp.cpp`, `1_py.py` | Marked as translations from `1_java` in the metadata. |
| `2_cpp.cpp`, `2_py.py` | Marked as translations from `2_java` in the metadata. |
| `3_cpp.cpp`, `3_py.py` | Marked as translations from `3_java` in the metadata. |

For provenance details beyond these examples, match a snippet’s filename stem to its key in `results/Results.json`. The `external_reference_url` field may contain a figure/listing citation or a note about translation rather than a clickable web URL. These entries document what the study metadata records; they do not independently verify the original source or its reuse terms. Before reusing or redistributing any snippet, check the original source and applicable license or permission. A citation or provenance entry alone does not grant reuse rights.
