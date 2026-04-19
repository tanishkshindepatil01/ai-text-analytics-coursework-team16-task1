Literature Review: Sequence Tagging for Biomedical Extractive Question Answering

1. Introduction

Extractive Question Answering (EQA) involves identifying the exact span of text within a given passage that answers a specific question. While pre-trained transformer architectures (e.g., BERT, RoBERTa) have propelled general domain EQA to surpass human performance on benchmark datasets like SQuAD, transitioning these advancements to the biomedical domain (BioEQA) presents unique challenges.

Historically, both general and biomedical EQA models have relied on a single-span extraction setting, which attempts to predict a single "start" and "end" position for an answer. While this paradigm suits the general domain, where questions are predominantly "factoid" (requiring a single answer), it is fundamentally constrained when applied to biomedical literature. The paper Sequence tagging for biomedical extractive question answering by Yoon et al. (2022) addresses this limitation by reformulating BioEQA as a multi-span sequence tagging task. This review synthesizes the motivations, methodologies, and empirical findings of this paradigm shift.

2. The Distributional Shift: General vs. Biomedical Questions

A core contribution of the reviewed literature is its empirical investigation into the fundamental differences between general-domain questions and naturally posed biomedical questions.

By analyzing datasets of naturally occurring questions—such as the Natural Questions (NQ) dataset for the general domain, alongside the Clinical Questions Collection (CQC) and PubMed user queries for the biomedical domain—Yoon et al. highlight a critical discrepancy:

General Domain: Questions are overwhelmingly factoid (63.4%), with a small minority (6.9%) being list-type questions (requiring multiple distinct phrases as answers).

Biomedical Domain: The proportion of list-type questions jumps significantly (21.9%), while factoid questions make up a much smaller share (12.5%).

This distributional shift is intuitive: biomedical concepts inherently involve multiplicities. Diseases present with multiple symptoms, signaling pathways involve multiple genes, and conditions are treated with multiple drugs. Furthermore, even factoid biomedical questions often feature valid alternative spans (e.g., synonyms or abbreviations). Consequently, a model restricted to extracting a single answer span is structurally ill-equipped for real-world BioEQA.

3. Traditional Approaches and Their Limitations

Prior state-of-the-art BioEQA models, such as those introduced by Yoon et al. (2019b) and Jeong et al. (2020), adapted general EQA models (like BioBERT) to biomedical tasks. Because these models utilized single-span prediction, they required complex, external post-processing pipelines to handle list-type questions.

These workarounds typically involved:

Thresholding: Applying fixed probability thresholds (optimized on validation sets) to determine how many predicted answer candidates should be accepted.

Rule-Based Detection: Parsing the question string for explicit numbers (e.g., "What two biological processes...") to artificially limit the model's output.

These ad-hoc solutions are brittle. They penalize valid alternative answers during training (treating them as noise) and fail entirely when list-type questions lack explicit numerical indicators—a scenario that comprises over 70% to 85% of list questions in standard BioASQ datasets.

4. BioEQA as Sequence Tagging

To natively solve the multi-span extraction problem, Yoon et al. (2022) propose abandoning the start-end prediction mechanism in favor of a sequence tagging framework (akin to Named Entity Recognition methodologies).

4.1 Methodology

The proposed architecture concatenates the question and passage into a single input sequence, feeding it into a contextualized biomedical language model (e.g., BioBERT, BlueBERT, or PubMedBERT). However, instead of outputting start/end logits, the final layer performs token-level classification using the BIO tagging scheme (Begin, Inside, Outside).

This allows the model to predict any number of answer spans simultaneously in a single forward pass, organically learning the appropriate number of answers from the training data without arbitrary thresholds.

4.2 Sequence Tagging Layers

The authors evaluated several sequence tagging layers applied on top of the transformer representations:

Linear Feed-Forward Layer: A simple linear classifier applied token-by-token.

BiLSTM & BiLSTM-CRF: Traditional sequence tagging architectures that model token dependencies.

Interestingly, the experiments revealed that the simple Linear layer outperformed the complex RNN/CRF layers. The authors hypothesize that RNNs bottleneck the contextual attention flows established by the underlying Transformer model, thereby nullifying the benefits of the BERT-based architecture for reading comprehension tasks.

5. Empirical Findings and System Capabilities

The sequence tagging approach was evaluated on the BioASQ 7b and 8b datasets, specifically targeting list-type questions.

5.1 Performance Improvements

The sequence tagging models demonstrated a commanding improvement over the baseline single-span models. Across various backbone language models (BioBERT, BlueBERT, PubMedBERT), the sequence tagging approach yielded average absolute F1-score improvements of 3.80% on BioASQ 7b and 6.22% on BioASQ 8b. The primary driver of this improvement was a massive boost in Recall, directly resulting from the model's unconstrained ability to predict multiple valid answer spans.

5.2 Universal Modeling capability

An additional advantage of the sequence tagging paradigm is its flexibility. Traditional pipelines require metadata indicating whether a question is "factoid" or "list" to apply the correct post-processing rules. The sequence tagging model requires no such metadata. When trained on an amalgamated dataset of both factoid and list questions, the model naturally learned to output single answers for factoid questions and multiple answers for list questions, maintaining competitive performance across both categories.

6. Conclusion

The transition from single-span start-end prediction to BIO sequence tagging represents a vital maturation in Biomedical Extractive Question Answering. By empirically validating that biomedical queries fundamentally require multi-span extractions, Yoon et al. (2022) successfully align the neural architecture with the domain's ground truth.

The sequence tagging framework eliminates the need for fragile, rule-based post-processing, achieves state-of-the-art results on benchmark datasets, and provides a "universal" modeling approach capable of answering naturally posed clinical questions without prior metadata. This robust, end-to-end extraction methodology is highly recommended as the standard architectural baseline for future BioEQA systems.
