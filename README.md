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

## folder Structure

reference files/:
Contains supporting reference materials used for the coursework.

classical Axis2 model.ipynb:
The final adjusted Classical Axis 2 code that was integrated into the main group notebook.

individually executable part Axis2.ipynb:
A standalone notebook that extracts the necessary setup from the full group notebook and keeps only the parts required for the Classical Axis 2 comparison. It can be run independently.

Classical_Axis2_Report.ipynb:
An explanatory report describing the code logic, the experiment design, and the interpretation of the results in a clear and beginner-friendly way.

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
