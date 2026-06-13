import requests
from bs4 import BeautifulSoup
import pandas as pd

def analyze_url(url):
    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""

        meta_description = ""

        desc_tag = soup.find(
            "meta",
            attrs={"name": "description"}
        )

        if desc_tag:
            meta_description = desc_tag.get(
                "content",
                ""
            ).strip()

        return {
            "URL": url,
            "Title": title,
            "Title Length": len(title),
            "Meta Description": meta_description,
            "Description Length": len(meta_description),
            "Title Status":
                "Good"
                if 30 <= len(title) <= 60
                else "Needs Optimization",
            "Description Status":
                "Good"
                if 120 <= len(meta_description) <= 160
                else "Needs Optimization"
        }

    except Exception as e:
        return {
            "URL": url,
            "Error": str(e)
        }


def main():

    with open(
        "sample_urls.txt",
        "r",
        encoding="utf-8"
    ) as file:

        urls = [
            line.strip()
            for line in file
            if line.strip()
        ]

    results = []

    for url in urls:
        print(f"Checking {url}")
        results.append(analyze_url(url))

    df = pd.DataFrame(results)

    df.to_csv(
        "seo_report.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\nSEO Report Saved:")
    print("seo_report.csv")


if __name__ == "__main__":
    main()
