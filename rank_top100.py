import json
from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ====================================
# Read Job Description
# ====================================

doc = Document("data/job_description.docx")

jd = ""

for para in doc.paragraphs:
    jd += para.text + " "

print("Loading model...")

# ====================================
# Load Embedding Model
# ====================================

model = SentenceTransformer("all-MiniLM-L6-v2")

jd_embedding = model.encode(
    jd,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# ====================================
# Build Candidate Text
# ====================================

def build_candidate_text(candidate):

    text = ""

    profile = candidate.get("profile", {})

    text += profile.get("headline", "") + " "
    text += profile.get("summary", "") + " "

    # Career History
    for job in candidate.get("career_history", []):

        text += job.get("title", "") + " "
        text += job.get("company", "") + " "
        text += job.get("description", "") + " "

    # Skills
    for skill in candidate.get("skills", []):

        if isinstance(skill, dict):
            text += skill.get("name", "") + " "
        else:
            text += str(skill) + " "

    # Education
    for edu in candidate.get("education", []):

        text += edu.get("degree", "") + " "
        text += edu.get("field_of_study", "") + " "
        text += edu.get("institution", "") + " "

    # Certifications
    for cert in candidate.get("certifications", []):

        text += cert.get("name", "") + " "

    return text


# ====================================
# Behavioral Score
# ====================================

def behavioral_score(signals):

    score = 0.0

    if signals.get("open_to_work_flag", False):
        score += 0.20

    score += signals.get(
        "recruiter_response_rate", 0
    ) * 0.30

    score += signals.get(
        "interview_completion_rate", 0
    ) * 0.30

    github_score = signals.get(
        "github_activity_score", 0
    )

    score += min(
        github_score / 100,
        0.20
    )

    return min(score, 1.0)


# ====================================
# Career Relevance Score
# ====================================

def career_score(text):

    keywords = [
        "retrieval",
        "ranking",
        "recommendation",
        "search",
        "vector",
        "embedding",
        "elasticsearch",
        "bm25",
        "milvus",
        "pinecone",
        "machine learning",
        "nlp"
    ]

    score = 0

    text = text.lower()

    for keyword in keywords:

        if keyword in text:
            score += 1

    return min(score / len(keywords), 1.0)


# ====================================
# Title Relevance Score
# ====================================

def title_relevance_score(candidate):

    profile = candidate.get("profile", {})

    title = profile.get(
        "headline",
        ""
    ).lower()

    title_map = {

        "senior ai engineer": 1.00,
        "ai engineer": 0.95,

        "senior machine learning engineer": 0.95,
        "machine learning engineer": 0.95,
        "ml engineer": 0.95,

        "data scientist": 0.90,
        "nlp engineer": 0.90,
        "search engineer": 0.90,

        "backend engineer": 0.75,
        "software engineer": 0.70,
        "data engineer": 0.70,

        "business analyst": 0.40,

        "project manager": 0.20,
        "operations manager": 0.15,

        "marketing manager": 0.05,
        "hr manager": 0.05,

        "customer support": 0.02,
        "sales executive": 0.02,

        "accountant": 0.01,
        "graphic designer": 0.01,
        "content writer": 0.01,

        "civil engineer": 0.05,
        "mechanical engineer": 0.05
    }

    for role, score in title_map.items():

        if role in title:
            return score

    return 0.20


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
        years / 10,
        1.0
    )


# ====================================
# Reason Generator
# ====================================

def generate_reason(
    similarity,
    behavior,
    career,
    title_score
):

    reasons = []

    if title_score >= 0.90:
        reasons.append(
            "Strong AI/ML engineering background"
        )

    if career >= 0.50:
        reasons.append(
            "Relevant retrieval, ranking or NLP experience"
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

    return ", ".join(reasons)

# ====================================
# Rank Candidates
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

        candidate = json.loads(line)

        text = build_candidate_text(
            candidate
        )

        candidate_embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        similarity = cosine_similarity(
            [jd_embedding],
            [candidate_embedding]
        )[0][0]

        behavior = behavioral_score(
            candidate.get(
                "redrob_signals",
                {}
            )
        )

        career = career_score(
            text
        )

        title_score = title_relevance_score(
            candidate
        )

        experience = experience_score(
            candidate
        )

        final_score = (
            0.35 * similarity +
            0.15 * behavior +
            0.20 * career +
            0.20 * title_score +
            0.10 * experience
        )

        scores.append({

            "candidate_id":
                candidate[
                    "candidate_id"
                ],

            "similarity":
                float(
                    similarity
                ),

            "behavior":
                float(
                    behavior
                ),

            "career":
                float(
                    career
                ),

            "title_score":
                float(
                    title_score
                ),

            "experience":
                float(
                    experience
                ),

            "final_score":
                float(
                    final_score
                )
        })


# ====================================
# Sort Results
# ====================================

scores.sort(
    key=lambda x:
        x["final_score"],
    reverse=True
)


# ====================================
# Display Top 20
# ====================================

print("\n" + "=" * 80)
print("TOP 20 CANDIDATES")
print("=" * 80)

for rank, candidate in enumerate(
    scores[:20],
    start=1
):

    reason = generate_reason(
        candidate["similarity"],
        candidate["behavior"],
        candidate["career"],
        candidate["title_score"]
    )

    print(
        f"\nRank {rank}"
    )

    print(
        f"Candidate ID : {candidate['candidate_id']}"
    )

    print(
        f"Final Score  : {candidate['final_score']:.4f}"
    )

    print(
        f"Similarity   : {candidate['similarity']:.4f}"
    )

    print(
        f"Behavior     : {candidate['behavior']:.4f}"
    )

    print(
        f"Career       : {candidate['career']:.4f}"
    )

    print(
        f"Title Score  : {candidate['title_score']:.4f}"
    )

    print(
        f"Experience   : {candidate['experience']:.4f}"
    )

    print(
        f"Reason       : {reason}"
    )

    print("-" * 80)


# ====================================
# Optional Top 100 Export
# ====================================

with open(
    "top100_debug.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        scores[:100],
        f,
        indent=4
    )

print("\nSaved top100_debug.json successfully.")
print("\nRanking completed.")