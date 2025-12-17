def export_to_csv(df, path="outputs/qualified_leads.csv"):
    df.to_csv(path, index=False)
    return path
