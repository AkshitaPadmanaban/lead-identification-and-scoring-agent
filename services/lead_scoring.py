def score_lead(row):
    score = 0

    if row["role"] in TARGET_ROLES:
        score += 30

    if row["industry"] in TARGET_INDUSTRIES:
        score += 25

    if row["keyword_matches"] >= 2:
        score += 20

    if row["years_experience"] >= 8:
        score += 15

    if row["source"] == "PubMed":
        score += 10

    return score
