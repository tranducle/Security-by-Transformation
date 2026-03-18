Below is an **exhaustive-in-practice technical catalogue** of dataset preprocessing techniques used **before (and within) model training pipelines** across **tabular, text, image, audio, time-series, and graph** data. For each technique/group, I include **what it does, when to use it, what data it fits, how to apply, and key pitfalls**.

Two global rules first:

* **Split first, then fit transforms on the training split only** to avoid leakage (fit → transform). Use pipeline abstractions to enforce this. ([scikit-learn][1])
* Treat preprocessing as **typed transforms**: *validation → cleaning → transform/encode → (optional) selection → (optional) augmentation → batching*.

---

## 0) Dataset profiling, schema, and anomaly detection (all data types)

### 0.1 Profiling (descriptive stats)

**What:** quantify missingness, ranges, cardinality, class balance, outlier rates, drift indicators.
**When:** always, before cleaning/feature design.
**Data:** all.
**How:** compute stats per feature (min/max/quantiles), missingness %, unique counts, label histograms.

### 0.2 Schema inference + validation

**What:** enforce expected types/domains/constraints (e.g., category sets, numeric ranges).
**When:** multiple sources, production pipelines, regulated settings.
**Data:** mostly tabular/logs, but also metadata for images/audio.
**How:** define schema then validate each batch against it; surface anomalies. TensorFlow Data Validation (TFDV) detects anomalies by comparing statistics to schema and reports mismatches. ([TensorFlow][2])

### 0.3 Drift & skew checks (train vs serving / train vs new batch)

**What:** detect distribution change (drift) and training/serving mismatch (skew).
**When:** ongoing training/monitoring; domain shift risk.
**How:** compare statistics for datasets using drift/skew comparators in schema (TFDV). ([TensorFlow][3])

---

## 1) Ingestion, parsing, integration, and alignment (all data types)

### 1.1 Parsing/decoding & canonicalization

**What:** decode encodings, parse formats, normalize line endings, parse timestamps.
**When:** heterogeneous sources, scraped text, logs, CSVs with mixed types.
**How:** robust parsers; strict type casting; reject malformed rows or quarantine.

### 1.2 Unit normalization & semantic harmonization

**What:** convert units (ms↔s), normalize currency, unify label taxonomies.
**When:** multiple producers (teams/devices), historical dataset merges.
**How:** explicit conversion tables; canonical mapping dictionaries.

### 1.3 Entity resolution / record linkage

**What:** deduplicate across sources (same real-world entity).
**When:** customer/user datasets, CRM merges, multi-log ingestion.
**How:** exact match keys + fuzzy matching (names/emails), learned linkage models.

### 1.4 Time alignment (time-series/logs)

**What:** timezone normalization, clock drift correction, resampling to fixed interval.
**When:** IoT, telemetry, logs, finance.
**How:** convert all timestamps to a single timeline, then resample/interpolate as needed; keep original time offsets as features when relevant.

---

## 2) Data cleaning & quality repair (all data types)

### 2.1 Deduplication

**What:** remove exact duplicates or near-duplicates.
**When:** web crawls, logs, image datasets (near-identical frames), speech corpora.
**How:**

* Tabular: hash full rows or key subsets.
* Text: MinHash / similarity thresholds.
* Image: perceptual hashing; embedding similarity.
  **Pitfall:** dedup **after** splitting can leak; prefer dedup **before** splitting if duplicates cross splits.

### 2.2 Missing data handling (tabular/time-series)

**What:** drop, impute, or model missingness.
**When:** tabular is almost always.
**How:** `SimpleImputer` (mean/median/most_frequent/constant) is standard. ([scikit-learn][4])
**Pitfalls:** impute using **train-only fit**; consider adding missingness indicator features for informative missingness.

### 2.3 Outlier handling (tabular/time-series)

**What:** identify and handle extreme/invalid values.
**When:** sensor glitches, financial spikes, manual entry errors.
**How:** IQR/MAD rules; domain thresholds; winsorization/clipping; robust models.
**Pitfall:** removing rare but real events can destroy anomaly detection.

### 2.4 Consistency checks and repair

**What:** fix inconsistent categories/strings (“US” vs “USA”), whitespace, casing.
**When:** human-entered fields, merged sources.
**How:** mapping tables; regex cleanup; canonicalization.

### 2.5 Label cleaning (supervised learning)

**What:** resolve contradictory labels, remove ambiguous items, handle label noise.
**When:** crowdsourced labels, weak supervision, class overlap.
**How:** adjudication rules, consensus, “gold” validation set, noise-robust filtering.
**Pitfall:** automated relabeling can introduce bias—log every change.

---

## 3) Numeric transformation & scaling (tabular/time-series/embeddings)

These are “must know” because many estimators assume roughly standardized inputs.

### 3.1 Standardization (z-score)

**What:** remove mean, scale to unit variance.
**When:** linear models, SVMs, neural nets, PCA.
**How:** `StandardScaler`. ([scikit-learn][5])
**Pitfall:** do not fit on full data; fit on train only.

### 3.2 Min–max / max-abs / robust scaling

**What:** scale into a bounded range; robust scaling uses medians/IQR.
**When:** features have different units; robust scaling when heavy outliers.
**How:** `MinMaxScaler`, `MaxAbsScaler`, `RobustScaler` (sklearn preprocessing suite). ([scikit-learn][6])

### 3.3 Normalization (vector normalization)

**What:** scale each sample vector to unit norm (L1/L2).
**When:** cosine similarity models, some text/embedding pipelines.
**How:** `Normalizer` in sklearn preprocessing. ([scikit-learn][6])

### 3.4 Power and distribution transforms

**What:** reduce skew / stabilize variance (log, Box–Cox, Yeo–Johnson, quantile transforms).
**When:** heavy-tailed numeric features.
**How:** apply after outlier treatment; validate impact using residual skewness.

### 3.5 Discretization / binning

**What:** map continuous values to bins.
**When:** monotonic models, interpretable rules, noisy sensors.
**How:** fixed-width bins, quantile bins; keep bin edges from training only.

---

## 4) Categorical encoding (tabular/logs)

### 4.1 One-hot encoding

**What:** convert categories into binary indicators.
**When:** nominal categories with manageable cardinality.
**How:** `OneHotEncoder` (strings/ints → sparse/dense). ([scikit-learn][7])
**Pitfall:** high cardinality explodes dimensionality.

### 4.2 Ordinal encoding

**What:** map ordered categories to integers.
**When:** true order exists (low/medium/high).
**Pitfall:** do **not** use ordinal encoding for nominal categories unless your model can handle it safely.

### 4.3 Hashing trick

**What:** map categories to fixed-size hash buckets.
**When:** very high cardinality (URLs, tokens, IDs).
**Pitfall:** collisions; choose bucket size carefully.

### 4.4 Target / mean encoding (leakage-sensitive)

**What:** encode category by target statistics.
**When:** high-cardinality categories with strong predictive signal.
**How:** compute on training folds only (CV target encoding).
**Pitfall:** extremely leakage-prone without fold-based computation.

### 4.5 Rare-category grouping & unknown handling

**What:** merge infrequent categories; define behavior for unseen categories.
**When:** production inference where new categories appear.
**How:** threshold-based grouping; `handle_unknown` strategies.

---

## 5) Feature engineering (structured/tabular/time-series/logs)

### 5.1 Derived numeric features

**What:** ratios, differences, interactions, log rates, per-capita metrics.
**When:** domain relationships matter.
**How:** deterministic transforms; document formulas.

### 5.2 Polynomial and interaction expansion

**What:** generate polynomial features & interactions.
**When:** linear models need nonlinearity.
**How:** `PolynomialFeatures`.
**Pitfall:** dimensionality blow-up.

### 5.3 Aggregations and group statistics

**What:** groupby aggregates (mean/count/std by user/device/time bucket).
**When:** logs, transactional data, cybersecurity telemetry.
**Pitfall:** time leakage—aggregate only using past data for forecasting.

### 5.4 Window features (time-series)

**What:** rolling mean/std/min/max, lags, EWMA.
**When:** forecasting, anomaly detection.
**How:** choose window sizes based on sampling rate and seasonality.

### 5.5 Resampling & interpolation (time-series)

**What:** align irregular samples to a grid; fill gaps.
**When:** sensor dropouts, mixed sampling.
**How:** forward fill, linear/spline interpolation; keep “gap length” as feature.

---

## 6) Feature selection & dimensionality reduction

### 6.1 Variance thresholding

**What:** remove near-constant features.
**When:** wide sparse datasets, one-hot outputs.
**How:** `VarianceThreshold`. ([Librosa][8])

### 6.2 Univariate selection

**What:** rank by statistical test score and keep top-k.
**When:** very wide tabular/text features.
**How:** `SelectKBest`. ([Librosa][9])

### 6.3 Mutual information selection

**What:** select features with high mutual information with target.
**When:** nonlinear dependencies.
**How:** `mutual_info_classif`/regression in sklearn. ([Librosa][10])

### 6.4 Wrapper/embedded selection

**What:** RFE, L1/Lasso, tree-based importances.
**When:** need compact models; interpretability.
**Pitfall:** selection must be inside CV to avoid optimistic bias.

### 6.5 PCA/SVD and related

**What:** reduce dimensionality while preserving variance.
**When:** correlated numeric features; text SVD for LSA.
**How:** `PCA` (fit on train only). ([scikit-learn][11])

---

## 7) Dataset splitting, sampling design, and leakage control

### 7.1 Stratified splits (classification)

**What:** preserve class proportions.
**How:** `StratifiedShuffleSplit`. ([scikit-learn][12])

### 7.2 Time-aware splits (forecasting)

**What:** prevent “training on the future.”
**How:** `TimeSeriesSplit` explicitly addresses time-ordered data. ([scikit-learn][11])

### 7.3 Group-aware splits (identity leakage)

**What:** split by user/device/patient so groups don’t cross splits.
**When:** personalization, medical, device telemetry.

### 7.4 Pipelines to prevent leakage

**What:** chain preprocessing and model in a single estimator so fitting occurs correctly.
**How:** sklearn `Pipeline` fits transformers sequentially then final estimator. ([scikit-learn][1])

---

## 8) Class imbalance handling (supervised classification)

### 8.1 Oversampling: SMOTE and variants

**What:** synthesize minority samples in feature space.
**How:** `SMOTE`, `BorderlineSMOTE`. ([Imbalanced Learn][13])
**When:** imbalanced tabular; be cautious with one-hot and complex manifolds.

### 8.2 Undersampling: Tomek links / cleaning

**What:** remove ambiguous majority samples near decision boundary.
**How:** `TomekLinks`. ([Imbalanced Learn][14])

### 8.3 Hybrid: SMOTE + Tomek

**What:** oversample then clean overlaps.
**How:** `SMOTETomek`. ([Imbalanced Learn][15])

---

## 9) Text preprocessing (NLP, LLM fine-tuning, classical ML)

### 9.1 Text normalization

**What:** Unicode normalization, lowercasing, punctuation/whitespace cleanup.
**When:** almost always; be careful with case-sensitive tasks (NER).

### 9.2 Tokenization pipeline (modern)

**What:** normalization + pre-tokenization + subword tokenization.
Hugging Face describes normalization and pre-tokenization as explicit steps before subtoken splitting. ([Hugging Face][16])

**How (practical):**

* Choose tokenizer type: **BPE**, **WordPiece**, **Unigram** (SentencePiece-style). ([Hugging Face][17])
* Train or reuse pretrained tokenizer; lock vocabulary for training.

### 9.3 Stopword handling (classical NLP)

**What:** remove high-frequency non-informative words.
**When:** bag-of-words/TF-IDF; not typical for transformer tokenization.
**How:** ensure stopword list matches vectorizer tokenization rules. ([scikit-learn][18])

### 9.4 Stemming / lemmatization (classical NLP)

**What:** reduce inflected forms to stems/lemmas.
**How:** NLTK provides stemmers and WordNet lemmatizer. ([NLTK][19])
**When:** classical ML on sparse text; less common with modern subword tokenization.
**Pitfall:** can harm meaning/NER.

### 9.5 Vectorization / representation

**TF-IDF / n-grams**
**What:** convert documents into sparse numeric matrices with tokenization + n-grams.
**How:** `TfidfVectorizer` exposes preprocessing/tokenization/ngram controls. ([scikit-learn][20])
**When:** strong baseline for text classification, retrieval.

---

## 10) Image preprocessing & augmentation (vision)

### 10.1 Deterministic preprocessing (applied to train/val/test)

* **Resize / center crop / pad** to fixed input size.
* **Normalize** (per-channel mean/std) consistent with pretrained backbones.
* **Color space conversion** (RGB↔BGR, grayscale) depending on model.
  Use TorchVision transforms for common image operations (crop/resize/etc.). ([PyTorch Documentation][21])

### 10.2 Contrast enhancement (classical CV / medical imaging)

* **Histogram equalization** (global) and **CLAHE** (adaptive, contrast-limited). ([OpenCV Docs][22])
  **When:** low-contrast images; be careful—can introduce artifacts.

### 10.3 Stochastic augmentation (train only)

**Geometric/photometric augmentations:** random crop, flips, color jitter, random resized crop, etc. ([PyTorch Documentation][21])
**Automated policies:** RandAugment. ([arXiv][23])
**Mixed-sample methods:** Mixup and CutMix (mix images and labels proportionally). ([arXiv][24])
**When:** limited data, overfitting, robustness needs.
**Pitfall:** apply only to training split; monitor label noise effects.

---

## 11) Audio preprocessing & augmentation (speech/audio)

### 11.1 Deterministic preprocessing

* resample to common sampling rate, trim/pad to fixed length, loudness normalization.
* feature extraction: **mel spectrogram**, **MFCC**, RMS, spectral centroid/bandwidth, etc. ([Librosa][25])

### 11.2 Augmentation

* additive noise, reverberation, time shift, time stretch, pitch shift (task-dependent).
* **SpecAugment**: time/frequency masking on filterbank-like features. ([arXiv][26])
  **When:** speech recognition and robust audio modeling.

---

## 12) Graph data preprocessing (GNNs)

**Core techniques:**

* **Node/edge deduplication**, remove self-loops (or add them intentionally), handle multi-edges.
* **Graph normalization:** normalize adjacency / degrees; feature normalization (standardize node features).
* **Subgraph sampling:** neighbor sampling, random walk sampling for large graphs.
* **Negative sampling:** for link prediction.
  **When:** any GNN pipeline; the exact normalization/sampling depends on model (GCN/GraphSAGE/GAT).

---

## 13) Privacy, security, governance, and reproducibility (all data types)

### 13.1 De-identification / pseudonymization

**What:** remove or transform PII/PHI; hash identifiers; tokenization/redaction.
**When:** regulated data; multi-tenant enterprise datasets.
**How:** deterministic hashing with salt; reversible token vault for join keys; redact free-text PII.

### 13.2 Dataset versioning & lineage

**What:** immutable dataset snapshots, transform logs, provenance.
**When:** any serious training pipeline; required for audits and reproducibility.

---

## 14) Input pipeline performance (practical, but “preprocessing” in production)

**What:** shuffling, batching, caching, prefetch, parallel mapping.
**When:** large-scale training; GPU underutilization.
**How:** framework input pipelines; keep deterministic seeds when you need reproducibility.

---

# How to apply “all techniques” correctly: an ordering template

1. **Ingest + canonicalize + dedup** (ideally before splitting if duplicates cross splits)
2. **Split** (stratified/time/group-aware as appropriate) ([scikit-learn][12])
3. **Fit-on-train transforms**: impute → encode → scale (inside a Pipeline) ([scikit-learn][1])
4. **Optional**: feature selection / PCA (inside CV) ([scikit-learn][27])
5. **Train-only augmentation** (vision/audio/text augmentation) ([PyTorch Documentation][21])
6. **Batching and throughput tuning**

---

If you tell me your **exact data modalities** (e.g., *tabular + network logs*, or *images + labels*, or *LLM fine-tuning text*) and your **task** (classification/detection/forecasting), I can produce a **single end-to-end preprocessing blueprint** with:

* which techniques are **mandatory vs optional**,
* the **exact order**,
* and concrete library calls (sklearn/TFX/TorchVision/HF/librosa) known to be leakage-safe.

[1]: https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html?utm_source=chatgpt.com "Pipeline"
[2]: https://www.tensorflow.org/tfx/data_validation/anomalies?utm_source=chatgpt.com "TensorFlow Data Validation Anomalies Reference | TFX"
[3]: https://www.tensorflow.org/tfx/tutorials/data_validation/tfdv_basic?utm_source=chatgpt.com "TensorFlow Data Validation | TFX"
[4]: https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html?utm_source=chatgpt.com "SimpleImputer — scikit-learn 1.8.0 documentation"
[5]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html?utm_source=chatgpt.com "StandardScaler — scikit-learn 1.8.0 documentation"
[6]: https://scikit-learn.org/stable/modules/preprocessing.html?utm_source=chatgpt.com "7.3. Preprocessing data"
[7]: https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html?utm_source=chatgpt.com "OneHotEncoder — scikit-learn 1.8.0 documentation"
[8]: https://librosa.org/doc-playground/main/generated/librosa.feature.mfcc.html?utm_source=chatgpt.com "librosa.feature.mfcc — librosa 0.9.1 documentation"
[9]: https://librosa.org/doc/0.11.0/feature.html?utm_source=chatgpt.com "Feature extraction — librosa 0.11.0 documentation"
[10]: https://librosa.org/doc/main/generated/librosa.feature.mfcc.html?utm_source=chatgpt.com "librosa.feature.mfcc — librosa 0.11.0 documentation"
[11]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html?utm_source=chatgpt.com "TimeSeriesSplit — scikit-learn 1.8.0 documentation"
[12]: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html?utm_source=chatgpt.com "StratifiedShuffleSplit — scikit-learn 1.8.0 documentation"
[13]: https://imbalanced-learn.org/stable/references/generated/imblearn.over_sampling.SMOTE.html?utm_source=chatgpt.com "SMOTE — Version 0.14.1"
[14]: https://imbalanced-learn.org/stable/references/generated/imblearn.under_sampling.TomekLinks.html?utm_source=chatgpt.com "TomekLinks — Version 0.14.1"
[15]: https://imbalanced-learn.org/stable/references/generated/imblearn.combine.SMOTETomek.html?utm_source=chatgpt.com "SMOTETomek — Version 0.14.1"
[16]: https://huggingface.co/learn/llm-course/en/chapter6/4?utm_source=chatgpt.com "Normalization and pre-tokenization"
[17]: https://huggingface.co/learn/llm-course/en/chapter6/6?utm_source=chatgpt.com "WordPiece tokenization - Hugging Face LLM Course"
[18]: https://scikit-learn.org/stable/modules/feature_extraction.html?utm_source=chatgpt.com "7.2. Feature extraction"
[19]: https://www.nltk.org/api/nltk.stem.html?utm_source=chatgpt.com "NLTK :: nltk.stem package"
[20]: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html?utm_source=chatgpt.com "TfidfVectorizer — scikit-learn 1.8.0 documentation"
[21]: https://docs.pytorch.org/vision/stable/transforms.html?utm_source=chatgpt.com "Transforming images, videos, boxes and more"
[22]: https://docs.opencv.org/4.x/d5/daf/tutorial_py_histogram_equalization.html?utm_source=chatgpt.com "2: Histogram Equalization"
[23]: https://arxiv.org/abs/1909.13719?utm_source=chatgpt.com "RandAugment: Practical automated data augmentation with a reduced search space"
[24]: https://arxiv.org/pdf/1710.09412?utm_source=chatgpt.com "mixup: BEYOND EMPIRICAL RISK MINIMIZATION"
[25]: https://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html?utm_source=chatgpt.com "librosa.feature.melspectrogram"
[26]: https://arxiv.org/abs/1904.08779?utm_source=chatgpt.com "SpecAugment: A Simple Data Augmentation Method for Automatic Speech Recognition"
[27]: https://scikit-learn.org/stable/modules/cross_validation.html?utm_source=chatgpt.com "3.1. Cross-validation: evaluating estimator performance"
