"""Download chemistry olympiad task PDFs (no solutions) from olympiads.bc-pf.org."""
import os
import re
import urllib.request

BASE = "https://olympiads.bc-pf.org/chemistry"
OUT = "chemistry"
YEARS = range(2020, 2025)  # last 5 available years
STAGES = {"national": "republic", "oblast": "oblast", "region": "region"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def links(url, pattern):
    return sorted(set(re.findall(pattern, get(url).decode("utf-8"))))


def save(url, path):
    if os.path.exists(path):
        return
    try:
        data = get(url)
    except urllib.error.HTTPError as e:
        print(f"SKIP {e.code} {url}")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    print(path)


for stage, folder in STAGES.items():
    for year in YEARS:
        grades = links(f"{BASE}/{stage}/{year}", rf'href="/chemistry/{stage}/{year}/(\d+)"')
        for grade in grades:
            pdfs = links(f"{BASE}/{stage}/{year}/{grade}", r'href="(https://cdn\.bc-pf\.org/[^"]+\.pdf)"')
            for pdf in pdfs:
                name = pdf.rsplit("/", 1)[1]
                if "tasks" in name:
                    save(pdf, f"{OUT}/{folder}/{year}/{grade}/{name}")

sessions = links(f"{BASE}/s/kaz_sbory", r'href="/chemistry/s/kaz_sbory/([^"]+)"')
for session in sessions:
    for pdf in links(f"{BASE}/s/kaz_sbory/{session}", r'href="(https://cdn\.bc-pf\.org/[^"]+\.pdf)"'):
        save(pdf, f"{OUT}/kaz_sbory/{session}/{pdf.rsplit('/', 1)[1]}")
