import requests
import os
import json

GITHUB_TOKEN = os.getenv("GH_STATS_TOKEN")
USERNAME = "exttreme0001"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_repositories():
    url = f"https://api.github.com/user/repos?per_page=100&type=all"
    response = requests.get(url, headers=HEADERS)
    return response.json() if response.status_code == 200 else []

def get_language_stats(repos):
    lang_stats = {}
    for repo in repos:
        if repo["private"] or not repo["fork"]:
            lang_url = repo["languages_url"]
            lang_data = requests.get(lang_url, headers=HEADERS).json()
            for lang, bytes in lang_data.items():
                lang_stats[lang] = lang_stats.get(lang, 0) + bytes
    return lang_stats

def update_readme(lang_stats):
    sorted_langs = sorted(lang_stats.items(), key=lambda x: x[1], reverse=True)
    top_langs_md = "\n".join([f"- {lang}: {round(size / 1024, 2)} KB" for lang, size in sorted_langs[:10]])

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content.replace("<!-- LANGUAGES_START -->", f"<!-- LANGUAGES_START -->\n{top_langs_md}")

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

repos = get_repositories()
lang_stats = get_language_stats(repos)
update_readme(lang_stats)
