"""Private progress report; optional allowlisted public snapshot."""
import base64
import datetime as dt
import json
import os
import urllib.request
from collections import Counter
from urllib.error import HTTPError

API = "https://api.github.com"
SOURCE = "GTU-Ultrasonik/Ultrasonik"
DEST = "GTU-Ultrasonik/gtu-ultrasonik.github.io"
MODULES = ("M1", "M2", "M3", "M4", "M5")


def request(path, token, method="GET", payload=None):
    req = urllib.request.Request(
        API + path, method=method,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "Content-Type": "application/json", "User-Agent": "ultrasonik-progress"})
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


def pages(path, token):
    page = 1
    while True:
        batch = request(path + "&per_page=100&page=" + str(page), token)
        yield from batch
        if len(batch) < 100:
            return
        page += 1


def aggregate(issues):
    counts = {m: {"completed": 0, "total": 0} for m in MODULES}
    credits = Counter()
    unassigned = 0
    for issue in issues:
        if "pull_request" in issue or issue.get("state_reason") in ("duplicate", "not_planned"):
            continue
        labels = {x["name"] for x in issue.get("labels", [])}
        selected = labels.intersection(MODULES)
        if not selected:
            continue
        if len(selected) != 1:
            raise ValueError("Each tracked issue must have exactly one module label")
        module = next(iter(selected))
        counts[module]["total"] += 1
        if issue["state"] == "closed":
            if issue.get("state_reason") != "completed":
                raise ValueError("Tracked closed issue has an unknown completion reason")
            counts[module]["completed"] += 1
            assignees = issue.get("assignees", [])
            if not assignees:
                unassigned += 1
            for a in assignees:
                credits[a["login"]] += 1
    return counts, credits, unassigned


def main():
    token = os.environ["GH_TOKEN"]
    counts, credits, unassigned = aggregate(pages("/repos/" + SOURCE + "/issues?state=all", token))
    prs = Counter(p["user"]["login"] for p in pages(
        "/repos/" + SOURCE + "/pulls?state=closed", token)
        if p.get("merged_at") and p.get("user") and p["user"].get("type") == "User")
    total = sum(c["total"] for c in counts.values())
    done = sum(c["completed"] for c in counts.values())
    lines = ["## Task progress (private)", "", f"Completed: {done}/{total}", "",
             "| Module | Completed | Total |", "|---|---:|---:|"]
    lines += [f"| {m} | {c['completed']} | {c['total']} |" for m,c in counts.items()]
    lines += ["", "## Contribution indicators (private)", "",
              "| GitHub account | Completed issue assignments | Merged PRs authored |",
              "|---|---:|---:|"]
    for user in sorted(credits.keys() | prs.keys()):
        lines.append(f"| {user} | {credits[user]} | {prs[user]} |")
    lines += ["", f"Completed issues without an assignee: {unassigned}.",
              "Multiple assignees each receive one assignment credit. These are activity indicators, not grades or effort percentages."]
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    if os.getenv("PUBLISH") != "true":
        print("Private report generated; public publication disabled.")
        return
    publish_token = os.getenv("PAGES_SYNC_TOKEN")
    if not publish_token:
        raise RuntimeError("Publication requested but PAGES_SYNC_TOKEN is missing")
    # Strict allowlist: do not export issue text, identifiers, names, or PR metadata.
    snapshot = {"published": True, "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "modules": counts}
    path = "/repos/" + DEST + "/contents/data/progress.json"
    current = request(path + "?ref=main", publish_token)
    previous = json.loads(base64.b64decode(current["content"]))
    if previous.get("published") is True and previous.get("modules") == counts:
        print("Public counts unchanged; no deployment needed.")
        return
    request(path, publish_token, "PUT", {
        "message": "chore: refresh approved aggregate progress",
        "content": base64.b64encode((json.dumps(snapshot, indent=2) + "\n").encode()).decode(),
        "sha": current["sha"], "branch": "main"})
    print("Approved aggregate snapshot published.")


if __name__ == "__main__":
    main()
