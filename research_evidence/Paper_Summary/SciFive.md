Literature Review: Biomedical Natural Language Processing and the Evolution of Text-to-Text Transformers

1. Introduction

The application of Natural Language Processing (NLP) to the biomedical domain has seen exponential growth over the last decade. With databases like PubMed and PubMed Central (PMC) housing millions of densely technical scientific papers, there is a pressing need for automated systems capable of text mining, document classification, relation extraction, and question answering. Historically, models trained on generalized corpora (such as Wikipedia or the Colossal Clean Crawled Corpus) have struggled with the highly specialized vocabulary of biomedicine. This review explores the trajectory of NLP models in the biomedical sphere, moving from early transformer-based classification models to domain-specific text-to-text generation models, as synthesized in the recent development of SciFive by Phan et al. (2021).

2. The Transformer Era and the Limits of BERT

The introduction of the Transformer architecture by Vaswani et al. (2017) revolutionized NLP by relying entirely on self-attention mechanisms, discarding recurrence and convolutions. This architecture paved the way for BERT (Bidirectional Encoder Representations from Transformers), introduced by Devlin et al. (2018). BERT achieved state-of-the-art (SOTA) results across numerous standard NLP benchmarks.

However, standard BERT models underperform on domain-specific scientific text. To bridge this gap, researchers developed domain-adapted variants such as BioBERT (Lee et al., 2019) and BlueBERT (Peng et al., 2019). These models were pre-trained on large biomedical corpora and achieved impressive results on classification-based tasks like Named Entity Recognition (NER) and Relation Extraction (RE).

Despite these advances, BERT and its biomedical derivatives are not unified transfer learning methods. Because they rely primarily on encoder-only architectures, they are restricted to producing single predictions (or probability distributions over text spans) for a given input. They are not intrinsically designed for sequence-to-sequence text generation tasks, severely limiting their applicability in complex areas like abstractive summarization and generative question answering.

3. The Shift to Unified Text-to-Text Frameworks

To overcome the generative limitations of BERT-style models, Raffel et al. (2019) proposed the Text-to-Text Transfer Transformer (T5). The T5 framework utilizes a full encoder-decoder architecture and reframes all NLP tasks—whether classification, translation, or regression—into a unified text-to-text format.

The T5 model was pre-trained using self-supervision on the Colossal Clean Crawled Corpus (C4) via span-based masked language modeling, where consecutive tokens are dropped and replaced by sentinel tokens, which the model must then generate. This generalized text-to-text approach allowed T5 to achieve SOTA results on a diverse array of generalized NLP tasks, outperforming BERT by natively supporting complex text generation.

4. Domain-Specific Adaptation: The Development of SciFive

While T5 represented a massive leap in generalized NLP, it still faced the "domain gap" when applied to biomedical literature. To address this, Phan et al. (2021) introduced SciFive, a domain-specific adaptation of the T5 model. SciFive leverages the base and large architectures of T5 but is subjected to extensive domain-specific pre-training.

To prevent the overfitting commonly seen when training language models on narrow domains (Ruder, 2017), SciFive's pre-training regimen combines the generalized C4 corpus with domain-specific corpora, specifically PubMed abstracts and full-text articles from PMC. Furthermore, SciFive employs the SentencePiece model (Kudo & Richardson, 2018) for sub-word tokenization. This prevents the need for an impossibly large technical vocabulary by extracting sub-words that capture semantic meaning, a crucial feature when processing complex chemical and biological nomenclature.

5. Performance on Standard Biomedical NLP Tasks

SciFive applies multi-task learning through "teacher forcing," using task-specific prepend tokens (e.g., prepending "ner:" for Named Entity Recognition tasks). This allows the model to leverage attention across various tasks simultaneously.

When evaluated against prior SOTA models like BioBERT and BlueBERT, SciFive demonstrates highly competitive or superior performance across standard classification-style tasks translated into text generation:

Named Entity Recognition (NER): Tested on corpora such as NCBI disease, BC5CDR, and JNLPBA, SciFive successfully generates target sequences by appending special tokens to named entities, achieving SOTA results on multiple datasets.

Relation Extraction (RE) and Inference: On tasks like CHEMPROT and MedNLI (Romanov & Shivade, 2018), SciFive effectively extracts gene-disease relationships and clinical inferences, proving that text-to-text models can seamlessly handle tasks traditionally dominated by standard classifiers.

6. Advancements in Biomedical Question Answering

The most significant contribution of text-to-text models like SciFive lies in Question Answering (QA). Traditional models like BioBERT handle QA by identifying the start and end probabilities of a text span within a provided context. Consequently, they often output fragmented or overly concise snippets.

Because SciFive is a generative model, it synthesizes the context to output complete, scientifically coherent sentences. When tested on the factoid questions of the BioASQ challenges (Tsatsaronis et al., 2015), SciFive vastly outperformed both BioBERT and the base T5 model. Expert assessments of lenient accuracy revealed that SciFive's generative approach provides clearer and more complete answers, showcasing the distinct advantage of sequence-to-sequence architectures in biomedical contexts where nuanced explanation is often required.

7. Conclusion

The evolution of biomedical NLP demonstrates a clear trajectory from generalized encoders to domain-specific, unified text-to-text transformers. While models like BioBERT successfully adapted transformer architectures to the biomedical vocabulary, their classification-bound nature limited their utility in generative tasks. The development of SciFive illustrates that text-to-text models, when adequately pre-trained on large-scale domain corpora like PubMed and PMC, can achieve SOTA performance across standard extraction tasks while unlocking unprecedented capabilities in complex question answering. Future research in this trajectory points naturally toward highly complex, extended generative tasks, including automated medical document summarization and scientific abstract generation.
