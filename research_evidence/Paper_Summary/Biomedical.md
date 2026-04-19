Summary: Biomedical Question Answering: A Survey of Approaches and Challenges

Authors: Qiao Jin, Zheng Yuan, et al. (Tsinghua University, Alibaba Group, Indiana University)
Published: ACM Computing Surveys, Vol. 55, No. 2, January 2022.

1. Executive Summary

This paper provides a systematic survey of the Biomedical Question Answering (BQA) landscape over the last two decades. It categorizes the field into four primary content types, identifies five major methodological approaches, and outlines critical challenges preventing BQA from reaching maturity for real-world clinical use.

2. Content Types in BQA

The authors categorize BQA based on the intended user and the nature of the information:

Type

Target User

Focus

Scientific

Researchers/Professionals

Latest findings from scientific literature (e.g., PubMed).

Clinical

Healthcare Professionals

Decision-making, diagnosis, and treatment based on EMRs.

Consumer Health

General Public

Non-expert health advice and self-diagnosis.

Examination

Students/Examinees

Answering multi-choice questions from medical licensure exams.

3. Five Major Methodological Approaches

The survey classifies BQA systems into five distinct strategies:

Classic Approach: Pipeline-based systems (Question $\rightarrow$ Document $\rightarrow$ Answer processing) relying heavily on rule-based models and manual feature engineering (e.g., IBM Watson-style).

Information Retrieval (IR): Focusing on finding relevant documents or snippets within massive corpora like PubMed.

Machine Reading Comprehension (MRC): The most active area, where models extract or generate answers from a specific context. Modern systems use Pre-trained Language Models (PLMs) like BioBERT or PubMedBERT.

Knowledge Base (KB): Translating natural language into structured queries (e.g., SPARQL) to retrieve facts from databases like UMLS, MeSH, or DrugBank.

Question Entailment (QE): A "nearest-neighbor" approach that identifies if a new question is semantically equivalent to a previously answered question (FAQ retrieval).

4. Key Datasets Highlighted

BioASQ: The cornerstone annual challenge for scientific BQA.

emrQA: A large-scale dataset derived from Electronic Medical Records.

PubMedQA: Focuses on yes/no/maybe answers based on PubMed abstracts.

VQA-Rad / VQA-Med: Datasets for Visual Question Answering (interpreting medical images).

5. Major Challenges and Future Directions

Despite rapid progress, the paper identifies several "bottlenecks":

Data Scarcity: Annotating biomedical data requires high-cost expert labor. While automatic "cloze-style" (fill-in-the-blank) generation helps, it lacks the complexity of real-world reasoning.

Reasoning Complexity: Most current datasets focus on "single-hop" retrieval. Future systems need to master multi-hop reasoning (connecting multiple pieces of evidence) and numeric reasoning (interpreting clinical stats).

Domain Knowledge Utilization: There is a disconnect between raw text models and structured Knowledge Bases. The authors suggest "fusing" these approaches.

Explainability: In medicine, a "Yes/No" is insufficient. Systems must provide the underlying evidence or "reasoning path" to be trusted by clinicians.

Evaluation Metrics: Standard NLP metrics (like BLEU or ROUGE) don't account for medical synonyms (e.g., "renal" vs. "kidney").

Fairness and Bias: Models trained on historical data may inherit racial or gender biases, which is a critical safety concern in healthcare.

6. Conclusion

The paper concludes that while deep learning and PLMs have significantly boosted performance on benchmarks, the "real-life" utility of BQA remains limited. The path forward involves moving toward multi-modal (text + image), explainable, and knowledge-infused systems that can handle the nuanced reasoning required in medical practice.
