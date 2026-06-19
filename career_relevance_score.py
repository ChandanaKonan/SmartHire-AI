def career_relevance_score(title):
    title = str(title).lower()

    scores = {
        "senior ai engineer": 1.0,
        "ai engineer": 0.95,
        "machine learning engineer": 0.95,
        "ml engineer": 0.95,
        "senior machine learning engineer": 0.95,
        "data scientist": 0.90,
        "nlp engineer": 0.90,
        "search engineer": 0.90,
        "recommendation engineer": 0.90,
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

    for role, score in scores.items():
        if role in title:
            return score

    return 0.20