from app.ingest.rss_ingest import fetch_recent_articles


def main(days_back: int = 3, max_preview: int = 10) -> None:
    articles = fetch_recent_articles(days_back=days_back)

    print(f"Fetched {len(articles)} recent funding-related articles.\n")

    for article in articles[:max_preview]:
        print(article)


if __name__ == "__main__":
    main()
