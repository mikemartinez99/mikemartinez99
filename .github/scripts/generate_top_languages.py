import os
import requests
import matplotlib.pyplot as plt

# --- Settings ---
GITHUB_USER = os.getenv("GITHUB_USER")  # e.g., 'mikemartinez99'
OUTPUT_FILE = "dist/top_languages.svg"

# --- Get repos ---
repos_url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
repos = requests.get(repos_url).json()

language_totals = {}

for repo in repos:
    langs_url = repo['languages_url']
    langs = requests.get(langs_url).json()
    for lang, bytes_count in langs.items():
        language_totals[lang] = language_totals.get(lang, 0) + bytes_count

# --- Sort and take top 10 ---
top_languages = dict(sorted(language_totals.items(), key=lambda x: x[1], reverse=True)[:10])

# --- Plot circular bar plot ---
langs = list(top_languages.keys())
sizes = list(top_languages.values())

fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
theta = [i / len(langs) * 2 * 3.14159 for i in range(len(langs))]

bars = ax.bar(theta, sizes, width=0.4, bottom=0, alpha=0.7)

# Add labels
for bar, lang, angle in zip(bars, langs, theta):
    rotation = angle * 180 / 3.14159
    ax.text(angle, bar.get_height() + max(sizes)*0.05, lang, rotation=rotation, ha='center', va='bottom', fontsize=10)

ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0, max(sizes)*1.2)
fig.tight_layout()
plt.savefig(OUTPUT_FILE, format='svg')
print(f"SVG saved to {OUTPUT_FILE}")
