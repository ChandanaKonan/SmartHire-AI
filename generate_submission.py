import json
import pandas as pd
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ====================================
# Read Job Description
# ====================================

doc = Document("data/job_description.docx")

jd = " ".join(
    [p.text for p in doc.paragraphs]
)

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

jd_embedding = model.encode(
    jd,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# ====================================
# Build Candidate Text
# ====================================

def build_candidate_text(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    text = ""

    text += profile.get(
        "headline",
        ""
    ) + " "

    text += profile.get(
        "summary",
        ""
    ) + " "

    for job in candidate.get(
        "career_history",
        []
    ):

        text += job.get(
            "title",
            ""
        ) + " "

        text += job.get(
            "company",
            ""
        ) + " "

        text += job.get(
            "description",
            ""
        ) + " "

    for skill in candidate.get(
        "skills",
        []
    ):

        if isinstance(skill, dict):

            text += skill.get(
                "name",
                ""
            ) + " "

        else:

            text += str(skill) + " "

    for edu in candidate.get(
        "education",
        []
    ):

        text += edu.get(
            "degree",
            ""
        ) + " "

        text += edu.get(
            "field_of_study",
            ""
        ) + " "

        text += edu.get(
            "institution",
            ""
        ) + " "

    for cert in candidate.get(
        "certifications",
        []
    ):

        text += cert.get(
            "name",
            ""
        ) + " "

    return text

# ====================================
# Behavioral Score
# ====================================

def behavioral_score(signals):

    score = 0.0

    if signals.get(
        "open_to_work_flag",
        False
    ):
        score += 0.15

    score += (
        signals.get(
            "recruiter_response_rate",
            0
        ) * 0.25
    )

    score += (
        signals.get(
            "interview_completion_rate",
            0
        ) * 0.25
    )

    score += min(
        signals.get(
            "github_activity_score",
            0
        ) / 100,
        0.15
    )

    score += min(
        signals.get(
            "saved_by_recruiters_30d",
            0
        ) / 100,
        0.10
    )

    score += min(
        signals.get(
            "search_appearance_30d",
            0
        ) / 200,
        0.10
    )

    return min(score, 1.0)

# ====================================
# Title Relevance Score
# ====================================

def title_relevance_score(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    title = profile.get(
        "headline",
        ""
    ).lower()

    if not title:

        career = candidate.get(
            "career_history",
            []
        )

        if career:

            title = career[0].get(
                "title",
                ""
            ).lower()

    title_map = {

        "senior ai engineer": 1.00,
        "ai engineer": 0.95,

        "senior machine learning engineer": 0.95,
        "machine learning engineer": 0.95,
        "ml engineer": 0.95,

        "search engineer": 0.95,
        "recommendation engineer": 0.95,

        "nlp engineer": 0.90,
        "data scientist": 0.90,

        "backend engineer": 0.75,
        "software engineer": 0.70,
        "data engineer": 0.70,

        "business analyst": 0.40,

        "project manager": 0.20,
        "operations manager": 0.15,

        "marketing manager": 0.01,
        "hr manager": 0.01,

        "customer support": 0.01,
        "sales executive": 0.01,

        "graphic designer": 0.01,
        "content writer": 0.01,
        "accountant": 0.01,

        "civil engineer": 0.05,
        "mechanical engineer": 0.05
    }

    for role, score in title_map.items():

        if role in title:

            return score

    return 0.20

# ====================================
# Retrieval Score
# ====================================

def retrieval_score(text):

    keywords = [

        "retrieval",
        "ranking",
        "search",
        "recommendation",

        "matching system",
        "candidate matching",
        "recommendation engine",
        "search engine",
        "relevance ranking",
        "marketplace ranking",
        "personalization",
        "retrieval pipeline",

        "embedding",
        "embeddings",

        "vector",
        "vector database",

        "pinecone",
        "milvus",
        "qdrant",
        "weaviate",
        "faiss",

        "elasticsearch",
        "opensearch",
        "bm25",

        "ndcg",
        "mrr",
        "map",

        "sentence transformer",
        "bge",
        "e5",

        "llm",
        "rag",
        "nlp"
    ]

    text = text.lower()

    score = 0

    for keyword in keywords:

        if keyword in text:

            score += 1

    return min(
        score / len(keywords),
        1.0
    )

# ====================================
# Experience Score
# ====================================

def experience_score(candidate):

    years = len(
        candidate.get(
            "career_history",
            []
        )
    )

    return min(
        years / 8,
        1.0
    )

# ====================================
# Dynamic Reasoning
# ====================================

def generate_reason(
    similarity,
    behavior,
    retrieval,
    title_score
):

    reasons = []

    if title_score >= 0.90:

        reasons.append(
            "Strong AI/ML engineering background"
        )

    if retrieval >= 0.40:

        reasons.append(
            "Relevant retrieval, ranking and search experience"
        )

    if behavior >= 0.50:

        reasons.append(
            "Strong recruiter engagement signals"
        )

    if similarity >= 0.60:

        reasons.append(
            "High semantic alignment with JD"
        )

    if not reasons:

        reasons.append(
            "Balanced candidate profile"
        )

    return "; ".join(reasons)
# ====================================
# Ranking
# ====================================

scores = []

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for i, line in enumerate(f):

        if i % 1000 == 0:

            print(
                f"Processed {i} candidates..."
            )

        candidate = json.loads(
            line
        )

        text = build_candidate_text(
            candidate
        )

        emb = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        similarity = cosine_similarity(
            [jd_embedding],
            [emb]
        )[0][0]

        behavior = behavioral_score(
            candidate.get(
                "redrob_signals",
                {}
            )
        )

        retrieval = retrieval_score(
            text
        )

        title_score = (
            title_relevance_score(
                candidate
            )
        )

        experience = experience_score(
            candidate
        )

        # ====================================
        # Final Score
        # ====================================

        final_score = (

            0.30 * similarity +

            0.25 * retrieval +

            0.25 * title_score +

            0.10 * behavior +

            0.10 * experience
        )

        scores.append({

            "candidate_id":
                candidate[
                    "candidate_id"
                ],

            "score":
                float(
                    final_score
                ),

            "similarity":
                float(
                    similarity
                ),

            "behavior":
                float(
                    behavior
                ),

            "retrieval":
                float(
                    retrieval
                ),

            "title_score":
                float(
                    title_score
                ),

            "experience":
                float(
                    experience
                )
        })

# ====================================
# Sort Results
# ====================================

scores.sort(
    key=lambda x:
        x["score"],
    reverse=True
)

# ====================================
# Create Top 100 Submission
# ====================================

rows = []

for rank, cand in enumerate(
    scores[:100],
    start=1
):

    rows.append({

        "candidate_id":
            cand["candidate_id"],

        "rank":
            rank,

        "score":
            round(
                cand["score"],
                4
            ),

        "reasoning":
            generate_reason(
                cand["similarity"],
                cand["behavior"],
                cand["retrieval"],
                cand["title_score"]
            )
    })

# ====================================
# Save Submission
# ====================================

df = pd.DataFrame(
    rows
)

df.to_csv(
    "submission.csv",
    index=False
)

print(
    "\nsubmission.csv created successfully!"
)

print(
    f"\nTotal Ranked Candidates: {len(df)}"
)

print(
    "\nTop 10 Candidates:\n"
)

print(
    df.head(10)
)

print(
    "\nBest Candidate:\n"
)

print(
    df.iloc[0]
)