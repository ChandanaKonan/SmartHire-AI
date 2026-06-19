import json
from sentence_transformers import SentenceTransformer

# ====================================
# Load Candidates
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

    return text

# ====================================
# Load Model
# ====================================

print("Loading model...")

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ====================================
# Test First Candidate
# ====================================

candidate_text = build_candidate_text(
    candidates[0]
)

embedding = model.encode(
    candidate_text
)

print(
    "Embedding Shape:",
    len(embedding)
)

print(
    "Candidate ID:",
    candidates[0].get(
        "candidate_id",
        "Unknown"
    )
)

print(
    "Text Length:",
    len(candidate_text)
)