import os
import requests
import matplotlib.pyplot as plt

# --- Settings ---
GITHUB_USER = os.getenv("GITHUB_USER")  # 'mikemartinez99'
OUTPUT_FILE = "dist/top_languages.svg"
MAX_LANGS = 10  # show top 10 languages

# --- Fetch repos ---
repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
repos = requests.get(repos_url).json()

# --- Aggregate languages ---
language_totals = {}
for repo in repos:
    langs_url = repo["languages_url"]
    langs = requests.get(langs_url).json()
    for lang, bytes_count in langs.items():
        language_totals[lang] = language_totals.get(lang, 0) + bytes_count

# --- Keep top languages ---
top_languages = dict(sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[:MAX_LANGS])

# --- Barplot ---
langs = list(top_languages.keys())
sizes = list(top_languages.values())

plt.figure(figsize=(8, 5))
bars = plt.barh(langs[::-1], [s/1000 for s in sizes[::-1]], color="#4c72b0")  # horizontal bars
plt.xlabel("Bytes (x1000)")
plt.title(f"Top Languages for {GITHUB_USER}")
plt.tight_layout()
plt.savefig(OUTPUT_FILE, format="svg")
print(f"SVG saved to {OUTPUT_FILE}")
