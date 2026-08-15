#!/usr/bin/env -S uv run --script
# Harvest public Reddit threads and comments for the R2 segment questions, into
# a local corpus a delegate can read offline. Authors are never written.
# Last updated: 2026-08-15
#
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
THREADS_PER_QUERY = 10
MIN_BODY_CHARS = 200  # Shorter comments are reactions, not descriptions.


class Reddit:
    def __init__(self, client_id: str, secret: str, user_agent: str) -> None:
        self.ua = user_agent
        self.token = self._authenticate(client_id, secret)

    def _authenticate(self, client_id: str, secret: str) -> str:
        basic = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        req = urllib.request.Request(
            TOKEN_URL,
            data=body,
            headers={"Authorization": f"Basic {basic}", "User-Agent": self.ua},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())["access_token"]

    def get(self, path: str, **params) -> dict | list | None:
        url = f"{API}{path}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {self.token}",
                "User-Agent": self.ua,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                print("  429, sleeping 60s", file=sys.stderr)
                time.sleep(60)
                return None
            print(f"  HTTP {exc.code} on {path}", file=sys.stderr)
            return None
        except Exception as exc:  # noqa: BLE001 - never abort a long harvest
            print(f"  {type(exc).__name__}: {exc}", file=sys.stderr)
            return None
        finally:
            time.sleep(PACE_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
