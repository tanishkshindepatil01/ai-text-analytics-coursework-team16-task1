# Medical Question Answering on PubMedQA: Analysing Text Representations and Classifier Design

## Group Information

**Module:** EMATM0067 – Introduction to AI and Text Analytics  
**University:** University of Bristol  
**Group:** Group 16  
**Coursework Task:** Task 01 – Biomedical Question Answering on PubMedQA  
**Repository Name:** ai-text-analytics-coursework-team16-task1  

---

## Group Members

| Name | University Email |
|---|---|
| Tanishk Nanasaheb Shinde | ac25643@bristol.ac.uk |
| Abdullah Alahmari | dl25357@bristol.ac.uk |
| Peidong Wang | hz25950@bristol.ac.uk |
| Zhengjie Xue | jw25233@bristol.ac.uk |
| Abhigyan Kashyap | wm25342@bristol.ac.uk |

---

## Project Overview

This repository contains the complete Group 16 coursework submission for **EMATM0067 – Introduction to AI and Text Analytics** at the University of Bristol. The project focuses on **biomedical question answering using the PubMedQA dataset**, where the aim is to classify whether scientific evidence supports a biomedical research question with a final answer of **yes**, **no**, or **maybe**.

Biomedical question answering is an important Natural Language Processing task because medical and scientific literature is expanding rapidly. Clinicians, researchers, and healthcare professionals cannot manually read every relevant biomedical paper, so automated systems that can interpret scientific evidence and support evidence-based decision making are increasingly valuable. However, this task is difficult because biomedical language is technical, context-dependent, and often uncertain.

In this project, we investigate the **expert-annotated PubMedQA subset**, which contains **1,000 labelled examples**. Each example includes a biomedical research question, context paragraphs from PubMed abstracts, a long-form answer, and a final label. The label distribution is imbalanced: the **yes** class is the largest, the **no** class is smaller, and the **maybe** class represents only around **11%** of the dataset. This makes the task especially challenging because the model must not only identify positive or negative evidence, but also recognise when the evidence is inconclusive.

The central research question of this project is:

> **Is PubMedQA performance mainly limited by the text representation used by the model, the classifier design, or the intrinsic difficulty of predicting the minority maybe class?**

To answer this, the project is organised around two main experimental axes:

1. **Axis 1 – Text Representation**  
   This axis studies how different input compositions and text representations affect model performance.

2. **Axis 2 – Classifier Design**  
   This axis studies how different classifiers, training strategies, and minority-class interventions affect overall performance and maybe-class recovery.

---

## Repository Structure

```text
ai-text-analytics-coursework-team16-task1/
│
├── Root_Level_Files/
│   ├── Group_Report/
│   │   └── EMATM0067_Task01_Team16_Report_.pdf
│   │
│   └── Individual_Reflection/
│
├── code/
│   ├── EMATM0067_Task01_Group16_PubMedQA_Pipeline.ipynb
│   ├── Predictions/
│   └── Visualization/
│
├── latex_source/
│   ├── Figures/
│   ├── acl.sty
│   ├── acl_latex.tex
│   ├── acl_lualatex.tex
│   ├── acl_natbib.bst
│   ├── anthology.bib.txt
│   └── custom.bib
│
├── research_evidence/
│   ├── AI & TA Research paper/
│   └── Paper_Summary/
│
└── README.md
```

---

## Folder Descriptions

### `Root_Level_Files/`

This folder contains final submission-level documents.

#### `Group_Report/`

This folder contains the final group report PDF:

```text
EMATM0067_Task01_Team16_Report_.pdf
```

The report presents the full project, including the abstract, introduction, related work, dataset description, methodology, experiments, results, discussion, limitations, future work, and conclusion.

#### `Individual_Reflection/`

This folder is reserved for individual reflection documents required as part of the coursework submission.

---

### `code/`

This folder contains the main experimental notebook and generated outputs.

#### Main Notebook

```text
EMATM0067_Task01_Group16_PubMedQA_Pipeline.ipynb
```

This notebook contains the full experimental pipeline, including:

- data loading
- preprocessing
- label encoding
- text input construction
- 500/500 train-test split creation
- 10-fold stratified cross-validation setup
- baseline TF-IDF + Logistic Regression
- BioBERT embeddings + Logistic Regression
- BioBERT fine-tuning
- PubMedBERT fine-tuning
- hyperparameter-tuned BioBERT
- LoRA PubMedBERT
- zero-shot BART-MNLI
- focal loss experiments
- threshold tuning
- ordinal-aware loss
- hierarchical classification
- quality-predictor analysis
- confusion matrix analysis
- cross-model error overlap
- visualisation generation
- prediction export

#### `Predictions/`

This folder stores model prediction outputs generated during the experiments.

#### `Visualization/`

This folder stores figures and visual outputs used in the report, including:

- label distribution charts
- Axis 1 performance comparison
- Axis 2 performance comparison
- per-class F1 plots
- confusion matrices
- Random Forest feature-importance plots
- model ranking figures

---

### `latex_source/`

This folder contains the LaTeX source files used to prepare the final group report.

It includes:

- ACL-style template files
- bibliography files
- custom references
- report source files
- figures used in the paper

This folder allows the final paper to be reproduced or edited through LaTeX or Overleaf.

---

### `research_evidence/`

This folder contains background research material used to support the report.

It includes:

- paper summaries
- literature notes
- CRAAP evaluations
- methodology sketches
- research gap analysis
- notes on biomedical NLP and PubMedQA-related literature

These files support the academic foundation of the coursework and demonstrate wider engagement with related research.

---

## Dataset

The project uses the **expert-annotated PubMedQA subset**, which contains **1,000 biomedical question-answering examples**.

Each example includes:

- a biomedical research question
- PubMed abstract context paragraphs
- a long-form answer
- a final label: `yes`, `no`, or `maybe`

The dataset is highly imbalanced:

| Label | Count | Percentage |
|---|---:|---:|
| yes | 552 | 55.2% |
| no | 338 | 33.8% |
| maybe | 110 | 11.0% |

The **maybe** class is the most difficult part of the task because it represents uncertain, insufficient, or inconclusive scientific evidence.

---

## Evaluation Setup

The project follows the **Jin et al. (2019) 500/500 evaluation structure**.

| Split | Total | Yes | No | Maybe |
|---|---:|---:|---:|---:|
| CV set | 500 | 276 | 169 | 55 |
| Test set | 500 | 276 | 169 | 55 |
| Full dataset | 1,000 | 552 | 338 | 110 |

The 500-sample CV set is used for internal validation and model selection.  
The 500-sample held-out test set is used for final evaluation.

Classical models use **10-fold stratified cross-validation**.  
Transformer models use a held-out validation fold due to computational constraints.

The primary evaluation metric is **macro-F1**, because the dataset is imbalanced and accuracy alone can hide poor minority-class performance.

Additional metrics include:

- accuracy
- per-class F1
- confusion matrix analysis
- McNemar’s significance test
- cross-model error overlap
- cluster-based error analysis
- quality-predictor analysis

---

## Axis 1: Text Representation

Axis 1 investigates how input composition and representation quality affect model performance.

The project compares three main input settings:

- **Q:** question only
- **Q+Ctx:** question plus PubMed abstract context
- **Q+Ctx+Ans:** question plus context plus long-form answer

It also compares different text representation methods:

- TF-IDF n-grams
- BioBERT sentence embeddings
- fine-tuned BioBERT
- fine-tuned PubMedBERT

### Axis 1 Configurations

| Label | Configuration |
|---|---|
| A1a | Question only with TF-IDF + Logistic Regression |
| A1b | Question + Context with TF-IDF + Logistic Regression |
| A1c | Question + Context + Answer with TF-IDF + Logistic Regression |
| A1d | BioBERT embeddings + Logistic Regression |
| A1e | BioBERT fine-tuning with Question + Context |
| A1f | BioBERT fine-tuning with Question + Context + Answer |
| A1g | PubMedBERT fine-tuning with Question + Context + Answer |

### Axis 1 Summary

The Axis 1 experiments show that adding more text does not automatically improve sparse TF-IDF models. TF-IDF models remain close to the same performance range because biomedical vocabulary is large and sparse, and useful discourse-level cues are diluted.

However, transformer models benefit strongly from richer input. BioBERT and PubMedBERT can use contextual information and long-answer cues more effectively than TF-IDF.

The strongest Axis 1 model is:

```text
A1g – PubMedBERT fine-tuned on Question + Context + Answer
```

---

## Axis 2: Classifier Design

Axis 2 investigates whether classifier choice, calibration, resampling, thresholding, or specialised training objectives can improve performance, especially for the minority **maybe** class.

### Axis 2 Configurations

| Label | Configuration |
|---|---|
| A2a | Tuned Logistic Regression |
| A2b | Calibrated SVM with threshold tuning |
| A2c | Multinomial Naive Bayes |
| A2d | SMOTE + Logistic Regression |
| A2e | Soft-voting ensemble |
| A2g | Hyperparameter-tuned BioBERT |
| A2i | LoRA PubMedBERT |
| A2j | Zero-shot BART-MNLI |
| M1 | BioBERT Q+Ctx+Ans with threshold tuning |
| M2 | PubMedBERT with focal loss |
| M3 | PubMedBERT focal loss with threshold tuning |
| M4 | PubMedBERT with ordinal-aware loss |
| M5 | Hierarchical classifier |

### Axis 2 Summary

The Axis 2 experiments show that classical classifier changes alone do not solve the PubMedQA problem. Logistic Regression, SVM, Naive Bayes, SMOTE, and voting ensembles all remain limited when using sparse TF-IDF features.

The best-performing models are PubMedBERT-based transformer models. However, even these models struggle to recover the **maybe** class.

Focal loss improves maybe-class F1, but slightly reduces overall macro-F1. This shows a trade-off between overall balanced performance and minority-class recovery.

---

## Main Results

The strongest overall model is:

```text
A1g – PubMedBERT fine-tuned on Question + Context + Answer
```

| Metric | Score |
|---|---:|
| Accuracy | 75.4% |
| Macro-F1 | 0.604 |
| F1-no | 0.797 |
| F1-maybe | 0.192 |
| F1-yes | 0.822 |

The best **maybe-class F1** is achieved by:

```text
M2 – PubMedBERT with Focal Loss
```

| Metric | Score |
|---|---:|
| Accuracy | 72.8% |
| Macro-F1 | 0.591 |
| F1-no | 0.694 |
| F1-maybe | 0.237 |
| F1-yes | 0.842 |

This shows that the best overall model is not the same as the best minority-class model.

---

## Key Findings

### 1. TF-IDF Models Plateau

Sparse TF-IDF models remain around **0.34–0.37 macro-F1**, regardless of input composition. This suggests that bag-of-words representations struggle to capture biomedical reasoning and uncertainty.

### 2. Long Answers Help Transformers More Than TF-IDF

Adding the long-form answer does not significantly improve TF-IDF models, but it strongly improves transformer models. This suggests that transformers can use discourse-level answer cues more effectively.

### 3. PubMedBERT Is the Best Overall Backbone

PubMedBERT fine-tuned on Q+Ctx+Ans achieves the strongest overall result, with **0.604 macro-F1** and **75.4% accuracy**.

### 4. The Maybe Class Remains the Main Bottleneck

Even the best model struggles with the **maybe** class. The project shows that uncertainty detection is much harder than predicting clear yes/no evidence.

### 5. Focal Loss Improves Maybe Recovery

PubMedBERT with focal loss improves maybe F1 from **0.192** to **0.237**, but overall macro-F1 decreases slightly from **0.604** to **0.591**.

### 6. Zero-Shot BART-MNLI Performs Poorly

Zero-shot BART-MNLI performs poorly on this task, showing that off-the-shelf NLI transfer does not work well for specialised biomedical QA without fine-tuning.

### 7. Overall Performance and Minority Recovery Trade Off

No single model wins on every metric. A1g is best for macro-F1, M2 is best for maybe F1, and M3 gives the highest accuracy but suppresses the maybe class.

---

## Error Analysis Overview

The error analysis shows that many errors are not simple keyword mistakes. The model often struggles with evidence sufficiency.

The most important error types include:

- **yes → no:** the model reverses positive evidence
- **no → yes:** the model reverses negative evidence
- **maybe → yes:** uncertain evidence is forced into a positive answer
- **maybe → no:** uncertain evidence is forced into a negative answer

The strongest model still forces many true maybe examples into yes or no predictions. This supports the conclusion that PubMedQA requires reasoning about whether the evidence is sufficient, not only whether it is positive or negative.

---

## Why This Project Matters

This project is important because medical question answering systems should not only maximise headline accuracy. In biomedical and clinical settings, the type of error matters.

For example, confusing **yes** and **no** can reverse the meaning of evidence. Similarly, converting an uncertain **maybe** answer into a confident **yes** or **no** answer can be risky because it hides uncertainty.

Therefore, this project argues that biomedical QA evaluation should consider:

- macro-F1
- per-class F1
- minority-class recovery
- confusion matrices
- yes/no reversal errors
- maybe-class suppression
- model calibration
- statistical significance
- cross-model error overlap
- human review for low-confidence predictions

---

## How to Run the Notebook

Open the main notebook:

```text
code/EMATM0067_Task01_Group16_PubMedQA_Pipeline.ipynb
```

Recommended environment:

- Google Colab or Jupyter Notebook
- Python 3.10+
- GPU recommended for transformer fine-tuning

Main Python libraries used:

```text
numpy
pandas
scikit-learn
matplotlib
seaborn
torch
transformers
sentence-transformers
imbalanced-learn
peft
```

Install required packages using:

```bash
pip install numpy pandas scikit-learn matplotlib seaborn torch transformers sentence-transformers imbalanced-learn peft
```

Then run the notebook cells sequentially.

Some transformer experiments require a GPU and may take longer to run on CPU.

---

## Reproducibility Notes

The project uses fixed random seeds where possible to support reproducibility.

However, transformer results may vary slightly depending on:

- GPU availability
- PyTorch version
- random seed behaviour
- batch size
- early stopping
- HuggingFace model loading
- Colab runtime state

Classical models are generally easier to reproduce because they use scikit-learn pipelines and stratified cross-validation.

---

## Final Report

The final group report is located at:

```text
Root_Level_Files/Group_Report/EMATM0067_Task01_Team16_Report_.pdf
```

The report contains:

- abstract
- introduction
- related work
- dataset description
- methods
- Axis 1 experiments
- Axis 2 experiments
- results
- error analysis
- discussion
- limitations
- future work
- conclusion
- references

---

## LaTeX Source

The LaTeX source used to generate the report is available in:

```text
latex_source/
```

This includes the ACL formatting files, bibliography files, and figures used in the final paper.

---

## Research Evidence

The supporting research notes are available in:

```text
research_evidence/
```

This folder contains background reading and supporting evidence for the report, including paper summaries and methodological notes.

---

