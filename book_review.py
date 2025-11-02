"""

GET - https://github.com/Usul-Dev/TIL/tree-commit-info/main/%EB%8F%85%ED%9B%84%EA%B0%90

응답
{
    "제로투원": {
        "oid": "32d232c0f37a82d3e55e018c89e21b87155dc6b6",
        "url": "/Usul-Dev/TIL/commit/32d232c0f37a82d3e55e018c89e21b87155dc6b6",
        "date": "2025-09-13T23:07:51.000+09:00",
        "shortMessageHtmlLink": "<a data-pjax=\"true\" title=\"chore: 2025-09-13 Coding Test\" class=\"Link--secondary\" href=\"/Usul-Dev/TIL/commit/32d232c0f37a82d3e55e018c89e21b87155dc6b6\">chore: 2025-09-13 Coding Test</a>"
    },
    "호의에대하여": {
        "oid": "7116e4fc6dd9dc6ddf61adc80ebab73bde603afc",
        "url": "/Usul-Dev/TIL/commit/7116e4fc6dd9dc6ddf61adc80ebab73bde603afc",
        "date": "2025-10-21T09:21:48.000+09:00",
        "shortMessageHtmlLink": "<a data-pjax=\"true\" title=\"chore: 호의에 대하여 독후감\" class=\"Link--secondary\" href=\"/Usul-Dev/TIL/commit/7116e4fc6dd9dc6ddf61adc80ebab73bde603afc\">chore: 호의에 대하여 독후감</a>"
    }
}


특정 키값을 추출하고 각 값에 맞는 링크로 들어가는 url을 해당 값에 하이퍼링크로 달아줘
- ex. [2025-10-21 호의에대하여](https://github.com/Usul-Dev/TIL/blob/main/%EB%8F%85%ED%9B%84%EA%B0%90/%EC%A0%9C%EB%A1%9C%ED%88%AC%EC%9B%90/%EC%A0%9C%EB%A1%9C%ED%88%AC%EC%9B%90.md)

"""
import os
from datetime import datetime, timezone
import requests
from urllib.parse import quote

OWNER = "Usul-Dev"
REPO = "TIL"
BASE_DIR = "독후감"
API = "https://api.github.com"

def _headers():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "book-review-bot",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def list_dir(path, ref="main"):
    enc = quote(path, safe="/")  # 한글/공백 경로 인코딩
    url = f"{API}/repos/{OWNER}/{REPO}/contents/{enc}"
    resp = requests.get(url, headers=_headers(), params={"ref": ref}, timeout=20)
    resp.raise_for_status()
    return resp.json()  # [{name,type,path,download_url,...}]

def latest_commit_for(path):
    url = f"{API}/repos/{OWNER}/{REPO}/commits"
    resp = requests.get(url, headers=_headers(), params={"path": path, "per_page": 1}, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return data[0] if data else None

def list_md_files_recursive(path):
    items = list_dir(path)
    md_paths = []
    for it in items:
        if it["type"] == "file" and it["name"].lower().endswith(".md"):
            md_paths.append(it["path"])
        elif it["type"] == "dir":
            md_paths.extend(list_md_files_recursive(it["path"]))
    return md_paths

def main(max_items=5):
    md_files = list_md_files_recursive(BASE_DIR)
    rows = []
    for p in md_files:
        c = latest_commit_for(p)
        if not c:
            continue
        iso = c["commit"]["author"]["date"]  # e.g. "2025-10-21T00:12:34Z"
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(timezone.utc)
        title = p.split("/")[-1].rsplit(".", 1)[0]
        url = f"https://github.com/{OWNER}/{REPO}/blob/main/{quote(p)}"
        rows.append({"title": title, "url": url, "date": dt.strftime("%Y-%m-%d"), "dt": dt})
    rows.sort(key=lambda x: x["dt"], reverse=True)
    return rows[:max_items]

if __name__ == "__main__":
    data = main()
    for item in data:
        print(item)
        print("✅"*10)
