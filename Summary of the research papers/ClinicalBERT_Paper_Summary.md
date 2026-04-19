# ClinicalBERT Paper Summary

## File Description
This repository/document contains a concise academic summary of the paper:

**ClinicalBERT: Modeling Clinical Notes and Predicting Hospital Readmission**  
Huang, Altosaar, and Ranganath (2020)


## What the Paper Does
The paper introduces **ClinicalBERT**, a version of BERT that is pre-trained on clinical notes instead of general text such as Wikipedia and BookCorpus. The goal is to build better representations of clinical language and use them for healthcare prediction tasks, especially **30-day hospital readmission prediction**. 

## Main Contributions
- Adapts BERT to clinical notes through domain-specific pre-training.
- Shows better clinical language modeling performance than standard BERT.
- Demonstrates stronger medical concept similarity representations than Word2Vec and FastText.
- Improves hospital readmission prediction using both discharge summaries and early admission notes.
- Provides some interpretability through attention visualization. 

## Key Results
### Clinical language modeling
- ClinicalBERT masked language modeling accuracy: **0.857**
- Standard BERT masked language modeling accuracy: **0.495** 

### Clinical concept similarity
- ClinicalBERT Pearson correlation: **0.670**
- Word2Vec: **0.553**
- FastText: **0.487** 

### Readmission prediction using discharge summaries
- ClinicalBERT achieves the best overall results among compared baselines:
  - **AUROC: 0.714**
  - **AUPRC: 0.701**
  - **RP80: 0.242** 

## Why It Matters
Clinical notes contain rich information about patient condition, symptoms, and care history, but they are difficult to model using traditional NLP methods. ClinicalBERT shows that transformer-based models trained on domain-specific text can improve predictive performance in healthcare and support clinically useful early-warning systems. 

## Limitations
- Trained and evaluated mainly on **MIMIC-III**, from one hospital system.
- May need retraining on local institutional data before practical deployment.
- Long-note aggregation remains challenging. 

## Suggested Use
This summary is useful for:
- literature review writing
- project background sections
- biomedical NLP coursework
- understanding why domain-specific BERT variants matter in healthcare
