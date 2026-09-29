#!/usr/bin/env bash
# Share a local preview of this site with a reviewer through a temporary Cloudflare quick tunnel.
#
#   ./share-preview.sh          (run from anywhere; Ctrl+C stops sharing)
#
# Prints a public https://<random>.trycloudflare.com link. Anyone with the link
# can see the site while this script runs; nothing stays online after Ctrl+C.
# Needs: hugo, and cloudflared (install once with: brew install cloudflared).
set -euo pipefail

PORT="${PORT:-1314}"   # 1314 so it doesn't clash with your usual `hugo server` on 1313
cd "$(dirname "$0")"

command -v hugo >/dev/null || { echo "hugo not found."; exit 1; }
command -v cloudflared >/dev/null || { echo "cloudflared not found. Install it once with:  brew install cloudflared"; exit 1; }

LOG="$(mktemp "${TMPDIR:-/tmp}/cf-tunnel.XXXXXX")"
cleanup() { [[ -n "${CF_PID:-}" ]] && kill "$CF_PID" 2>/dev/null || true; rm -f "$LOG"; }
trap cleanup EXIT INT TERM

echo "Starting Cloudflare tunnel..."
cloudflared tunnel --no-autoupdate --url "http://localhost:${PORT}" >"$LOG" 2>&1 &
CF_PID=$!

URL=""
for _ in $(seq 1 60); do
  URL="$(grep -Eo 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG" | head -1 || true)"
  [[ -n "$URL" ]] && break
  kill -0 "$CF_PID" 2>/dev/null || { echo "cloudflared exited:"; cat "$LOG"; exit 1; }
  sleep 1
done
[[ -n "$URL" ]] || { echo "No tunnel URL after 60 s:"; cat "$LOG"; exit 1; }

echo
echo "============================================================"
echo "  Share this link:  $URL"
echo "  (give it ~10 s to come up; Ctrl+C here stops sharing)"
echo "============================================================"
echo

# baseURL = the tunnel URL so every link and asset resolves for the reviewer.
# (not `exec`, so the trap still stops cloudflared when you press Ctrl+C)
hugo server --port "$PORT" --bind 127.0.0.1 \
  --baseURL "$URL" --appendPort=false --disableLiveReload
