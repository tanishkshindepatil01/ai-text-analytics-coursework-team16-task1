BioBERT: A Pre-trained Biomedical Language Representation Model

BioBERT (Bidirectional Encoder Representations from Transformers for Biomedical Text Mining) is a domain-specific language representation model pre-trained on large-scale biomedical corpora.

This repository contains information, resources, and (if applicable) code related to the research paper: BioBERT: a pre-trained biomedical language representation model for biomedical text mining (Lee et al., 2020).

Overview

While deep learning has boosted the development of effective biomedical text mining models, directly applying general-domain NLP advancements (like standard BERT) to biomedical text often yields unsatisfactory results due to a word distribution shift.

BioBERT addresses this by initializing with weights from the original BERT model (pre-trained on English Wikipedia and BooksCorpus) and continuing the pre-training process on massive biomedical domain corpora.

Pre-training Corpora

PubMed Abstracts: 4.5 Billion words

PMC Full-text articles: 13.5 Billion words

Key Results & Performance

With almost the same architecture across tasks, BioBERT largely outperforms standard BERT and previous state-of-the-art (SOTA) models in a variety of biomedical text mining tasks:

Biomedical Named Entity Recognition (NER): 0.62% F1 score improvement over previous SOTA.

Biomedical Relation Extraction (RE): 2.80% F1 score improvement over previous SOTA.

Biomedical Question Answering (QA): 12.24% Mean Reciprocal Rank (MRR) improvement over previous SOTA.

Official Repositories

The original authors have made the pre-trained weights and fine-tuning source code freely available:

Pre-trained Weights: naver/biobert-pretrained

Fine-tuning Source Code: dmis-lab/biobert

Evaluated Datasets

BioBERT was rigorously evaluated on several standard biomedical datasets:

NER: NCBI Disease, 2010 i2b2/VA, BC5CDR, BC4CHEMD, BC2GM, JNLPBA, LINNAEUS, Species-800

Relation Extraction: GAD (Gene-disease), EU-ADR (Gene-disease), CHEMPROT (Protein-chemical)

Question Answering: BioASQ 4b, 5b, and 6b (factoid)

Citation

If you use BioBERT in your research or project, please cite the original paper:

@article{lee2020biobert,
  title={BioBERT: a pre-trained biomedical language representation model for biomedical text mining},
  author={Lee, Jinhyuk and Yoon, Wonjin and Kim, Sungdong and Kim, Donghyeon and Kim, Sunkyu and So, Chan Ho and Kang, Jaewoo},
  journal={Bioinformatics},
  volume={36},
  number={4},
  pages={1234--1240},
  year={2020},
  publisher={Oxford University Press}
}


License

The original article is an Open Access article distributed under the terms of the Creative Commons Attribution License.
