"""
Personal research tool: find Reddit discussions about transitioning from
database administration into platform engineering.

Read-only. No posting, voting, or messaging.
Results are written to a local Markdown file for manual reading and are
not redistributed, published, or used to train any model.
"""

import os
import time
import datetime as dt

import praw

# --- Configuration -----------------------------------------------------------

SUBREDDITS = [
    "devops",
    "sre",
    "platform_engineering",
    "ExperiencedDevs",
    "sysadmin",
]

QUERIES = [
    "dba to platform engineer",
    "database administrator career change",
    "platform engineer interview experience",
    "dba to devops",
    "platform engineering skills required",
]

POSTS_PER_QUERY = 15      # keep the request volume low
COMMENTS_PER_POST = 10    # top-level comments only
SLEEP_BETWEEN_CALLS = 2   # be gentle, stay well under rate limits
OUTPUT_FILE = "results.md"


# --- Reddit client -----------------------------------------------------------

def get_client() -> praw.Reddit:
    """Credentials come from environment variables, never hardcoded."""
    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ.get(
            "REDDIT_USER_AGENT",
            "script:career-research:v1.0 (personal, non-commercial)",
        ),
    )


# --- Collection --------------------------------------------------------------

def search_subreddit(reddit, subreddit_name, query):
    """Search one subreddit for one query and return simplified results."""
    results = []
    subreddit = reddit.subreddit(subreddit_name)

    for post in subreddit.search(query, sort="relevance", limit=POSTS_PER_QUERY):
        post.comments.replace_more(limit=0)  # skip "load more" expansion
        comments = [
            c.body.strip()
            for c in post.comments[:COMMENTS_PER_POST]
            if getattr(c, "body", None)
        ]

        results.append(
            {
                "subreddit": subreddit_name,
                "title": post.title,
                "url": f"https://reddit.com{post.permalink}",
                "score": post.score,
                "created": dt.datetime.fromtimestamp(post.created_utc).date(),
                "selftext": (post.selftext or "").strip(),
                "comments": comments,
            }
        )
        time.sleep(SLEEP_BETWEEN_CALLS)

    return results


# --- Output ------------------------------------------------------------------

def write_markdown(all_results, path=OUTPUT_FILE):
    """Write everything to one Markdown file so it can be read in an editor."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Reddit research notes\n\n")
        f.write(f"Collected on {dt.date.today().isoformat()}\n\n")

        for item in all_results:
            f.write(f"## {item['title']}\n\n")
            f.write(
                f"r/{item['subreddit']} · {item['score']} points · "
                f"{item['created']}\n\n"
            )
            f.write(f"<{item['url']}>\n\n")

            if item["selftext"]:
                f.write(item["selftext"][:2000] + "\n\n")

            if item["comments"]:
                f.write("### Comments\n\n")
                for comment in item["comments"]:
                    f.write(f"- {comment[:1000]}\n\n")

            f.write("---\n\n")


# --- Main --------------------------------------------------------------------

def main():
    reddit = get_client()
    seen_urls = set()
    all_results = []

    for subreddit_name in SUBREDDITS:
        for query in QUERIES:
            print(f"Searching r/{subreddit_name}: {query!r}")
            try:
                for item in search_subreddit(reddit, subreddit_name, query):
                    if item["url"] not in seen_urls:
                        seen_urls.add(item["url"])
                        all_results.append(item)
            except Exception as exc:
                print(f"  skipped ({exc})")
            time.sleep(SLEEP_BETWEEN_CALLS)

    write_markdown(all_results)
    print(f"\n{len(all_results)} threads written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
