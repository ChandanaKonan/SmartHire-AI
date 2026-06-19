# SmartHire AI

## AI-Powered Candidate Discovery & Ranking System

### Redrob Intelligent Candidate Discovery & Ranking Challenge

SmartHire AI is an AI-powered candidate ranking system designed to identify the most suitable candidates for a job role by combining semantic understanding, retrieval expertise detection, behavioral intelligence, title relevance analysis, and experience evaluation.

Unlike traditional Applicant Tracking Systems (ATS) that rely heavily on keyword matching, SmartHire AI evaluates the complete candidate profile and ranks candidates similarly to how an experienced recruiter would.

---

# Problem Statement

Recruiters often review hundreds of profiles but still miss strong candidates because traditional systems rely on exact keyword matches.

The objective of SmartHire AI is to:

* Understand the Job Description semantically
* Understand the candidate's actual experience
* Detect retrieval, ranking, recommendation, and AI expertise
* Incorporate behavioral hiring signals
* Down-rank keyword-stuffed profiles
* Avoid obvious trap candidates
* Generate a trustworthy Top-100 shortlist

---

# Key Features

## Semantic Candidate Matching

Uses Sentence Transformers to understand candidate profiles and compare them against the job description using semantic similarity rather than keyword matching.

## Behavioral Signal Analysis

Incorporates Redrob behavioral signals such as:

* Open To Work Status
* Recruiter Response Rate
* Interview Completion Rate
* GitHub Activity
* Recruiter Saves
* Search Appearances

These signals help identify candidates who are both qualified and actively available.

## Retrieval & Ranking Experience Detection

Detects experience related to:

* Retrieval Systems
* Search Systems
* Recommendation Engines
* Candidate Matching Systems
* Ranking Infrastructure
* NLP Systems
* Vector Databases

Supported technologies include:

* Pinecone
* FAISS
* Milvus
* Qdrant
* Weaviate
* Elasticsearch
* OpenSearch
* BM25

## Title Relevance Scoring

Rewards candidates whose career trajectory aligns with the target role:

* AI Engineer
* Machine Learning Engineer
* NLP Engineer
* Search Engineer
* Recommendation Engineer
* Data Scientist

Profiles unrelated to AI and retrieval systems are appropriately down-weighted.

## Experience Analysis

Evaluates professional experience using candidate career history.

## Dynamic Candidate Reasoning

Generates human-readable explanations describing why each candidate was selected.

---

# System Architecture

Job Description

↓

Sentence Transformer Embeddings

↓

Semantic Similarity Scoring

↓

Behavioral Signal Analysis

↓

Retrieval & Ranking Experience Detection

↓

Title Relevance Scoring

↓

Experience Scoring

↓

Hybrid Candidate Ranking

↓

Top 100 Candidate Recommendations

---

# Final Scoring Formula

Final Score =

0.30 × Semantic Similarity

* 0.25 × Retrieval Experience Score

* 0.25 × Title Relevance Score

* 0.10 × Behavioral Score

* 0.10 × Experience Score

---

# Trap Candidate Handling

The Redrob dataset contains intentionally misleading profiles.

SmartHire AI reduces the likelihood of selecting these candidates by:

* Penalizing unrelated job titles
* Rewarding retrieval and ranking expertise
* Using semantic similarity instead of keyword counts
* Incorporating recruiter engagement signals
* Considering overall career trajectory

This helps prevent keyword-stuffed profiles from ranking above genuinely qualified candidates.

---

# Technologies Used

* Python
* Streamlit
* Pandas
* NumPy
* Scikit-Learn
* Sentence Transformers
* Plotly
* Python-Docx

---

# Project Structure

SmartHire_AI/

├── app.py

├── generate_submission.py

├── generate_submission_fast.py

├── ranktop100.py

├── requirements.txt

├── README.md

├── submission.csv

└── data/

  ├── job_description.docx

  └── candidates.jsonl

---

# Installation

```bash
pip install -r requirements.txt
```

---

# Generate Candidate Rankings

```bash
python generate_submission_fast.py
```

This generates:

```text
submission.csv
```

containing the Top 100 ranked candidates.

---

# Launch Dashboard

```bash
streamlit run app.py
```

---

# Dashboard Features

* Candidate Search
* Best Candidate Overview
* Score Distribution Visualization
* Top 10 Candidate Analysis
* Candidate Leaderboard
* Top 100 Rankings
* CSV Download Support

---
## Screenshots

### Dashboard
<img width="791" height="741" alt="Screenshot 2026-06-19 175937" src="https://github.com/user-attachments/assets/6fdc9cc7-dd6b-4849-9480-02f5ebcd6d4b" />


### Candidate Rankings
<img width="1530" height="860" alt="Screenshot 2026-06-19 180004" src="https://github.com/user-attachments/assets/6e5f9498-15fa-4093-8818-7c143ece1f6e" />


### Score Distribution
<img width="1746" height="672" alt="Screenshot 2026-06-19 180032" src="https://github.com/user-attachments/assets/028dba4e-4b5a-41d3-a207-e4b015b07c0b" />
<img width="1763" height="683" alt="Screenshot 2026-06-19 180052" src="https://github.com/user-attachments/assets/865c5a66-998d-4382-94f7-de3f9e636a6b" />
<img width="1763" height="683" alt="Screenshot 2026-06-19 180052" src="https://github.com/user-attachments/assets/28eff7fc-ed96-49e9-be54-9b3e49a12338" />
<img width="1787" height="672" alt="Screenshot 2026-06-19 180109" src="https://github.com/user-attachments/assets/3fdf315c-ff46-463d-945b-060d523a2668" />
<img width="1738" height="717" alt="Screenshot 2026-06-19 180126" src="https://github.com/user-attachments/assets/0c0c7846-b6d8-41ba-805b-0c08f95e9765" />
<img width="1723" height="632" alt="Screenshot 2026-06-19 180146" src="https://github.com/user-attachments/assets/8d54822e-9d06-4c45-9c72-c56ebdca52b6" />
<img width="936" height="618" alt="Screenshot 2026-06-19 180200" src="https://github.com/user-attachments/assets/87b9189b-a7d2-480c-be63-bcef116769bf" />


# Future Improvements

* Learning-to-Rank Models
* XGBoost Ranker
* LLM-Based Re-Ranking
* Skill Gap Analysis
* Explainable AI Recommendations
* Multi-Job Ranking Support

---

# Author

Chandana K V

Graguagated Computer Science and Engineering (Data Science) Student

SmartHire AI – Intelligent Candidate Discovery & Ranking System
