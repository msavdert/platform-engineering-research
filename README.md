# Reddit Career Research

A small personal script that searches a handful of Reddit communities for
discussions about moving from a database administration role into platform
engineering, and writes the results to a local Markdown file so they can be
read in an editor.

## Why this exists

I work as a database administrator and I am planning a move into platform
engineering. Before committing to that path I want to understand what the role
actually involves day to day, which skills employers expect, and what the
interview process looks like — as described by people who have already made
the transition.

Reddit's search interface makes it hard to collect threads across several
subreddits and read them in one place, so this script does that step for me.
Reading and analysis are entirely manual.

## Scope

**Subreddits searched**

- r/devops
- r/sre
- r/platform_engineering
- r/ExperiencedDevs
- r/sysadmin

**API access used**

- Subreddit search (read-only)
- Top-level comment listing on matching posts (read-only)

The script does not post, comment, vote, send messages, or take any write
action. It authenticates as a script application under a single personal
account.

**Request volume**

Roughly 350–400 requests per run, with a 2 second pause between calls. Runs are
occasional, not scheduled. This is far below the documented rate limits.

## Data handling

- Results are written to `results.md` on my own machine.
- `results.md` is git-ignored and is not committed, published, or shared.
- Collected content is deleted once I have finished reading it.
- No data is stored in a database or retained long term.

## What this project does not do

- Not commercial. It is personal research, with no product, service, or
  revenue attached.
- No machine learning or AI model training on Reddit data.
- No redistribution, resale, or licensing of Reddit content.
- No user profiling, no inference of sensitive characteristics, and no attempt
  to identify or de-anonymise anyone. Author names are not collected.
- No scraping outside the API, and no circumvention of rate limits.

## Setup

```bash
pip install -r requirements.txt

export REDDIT_CLIENT_ID="your_client_id"
export REDDIT_CLIENT_SECRET="your_client_secret"
export REDDIT_USER_AGENT="script:career-research:v1.0 (personal, non-commercial)"

python search_reddit.py
```

Credentials are read from environment variables and are never committed.

## Configuration

`SUBREDDITS` and `QUERIES` at the top of `search_reddit.py` control what gets
searched. `POSTS_PER_QUERY` and `COMMENTS_PER_POST` control how much is
retrieved per search.

## Terms

This project is intended to comply with the
[Reddit Data API Terms](https://redditinc.com/policies/data-api-terms) and the
[Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).
