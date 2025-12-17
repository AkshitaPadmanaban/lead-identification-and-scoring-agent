import pandas as pd
from config.domain_config import TARGET_KEYWORDS

def identify_leads(data: pd.DataFrame) -> pd.DataFrame:
    def keyword_match(text):
        return sum(kw.lower() in text.lower() for kw in TARGET_KEYWORDS)

    data["keyword_matches"] = data["research_summary"].apply(keyword_match)
    return data[data["keyword_matches"] > 0]
