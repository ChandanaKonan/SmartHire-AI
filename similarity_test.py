import json

from docx import Document
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ====================================
# Read Job Description
# ====================================

doc = Document(
    "data/job_description.docx"
)

jd = ""

for para in doc.paragraphs:

    jd += para.text + " "

# ====================================
# Read Candidates
# ====================================

candidates = []

with open(
    "data/candidates.jsonl",
    "r",
    encoding="utf-8"
) as f:

    for line in f:

        candidates.append(
            json.loads(line)
        )

print(
    f"Loaded {len(candidates)} candidates"
)

# ====================================
# Test First Candidate
# ====================================

candidate = candidates[0]

profile = candidate.get(
    "profile",
    {}
)

candidate_text = ""

candidate_text += profile.get(
    "headline",
    ""
)

candidate_text += " "

candidate_text += profile.get(
    "summary",
    ""
)

# ====================================
# Load Model
# ====================================

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ====================================
# Generate Embeddings
# ====================================

jd_embedding = model.encode(
    jd,
    convert_to_numpy=True,
    normalize_embeddings=True
)

candidate_embedding = model.encode(
    candidate_text,
    convert_to_numpy=True,
    normalize_embeddings=True
)

# ====================================
# Similarity Score
# ====================================

score = cosine_similarity(
    [jd_embedding],
    [candidate_embedding]
)[0][0]

# ====================================
# Results
# ====================================

print("\nCandidate ID:")
print(
    candidate["candidate_id"]
)

print("\nHeadline:")
print(
    profile.get(
        "headline",
        "N/A"
    )
)

print("\nSimilarity Score:")
print(
    round(score, 4)
)