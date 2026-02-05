
import os, time
from collections import defaultdict, deque
from flask import request, jsonify

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

API_KEY = os.getenv("API_KEY", "")
RATE_LIMIT = int(os.getenv("RATELIMIT") or 80)
WINDOW = 60
_buckets = defaultdict(deque)

def _bucket_id():
    k = request.headers.get("X-API-Key")
    return k if k else f"ip:{request.remote_addr or 'unknown'}"

def init_auth(app):
    @app.before_request
    def _enforce():
        if not request.path.startswith("/api/"):
            return
        if API_KEY:
            if request.headers.get("X-API-Key") != API_KEY:
                return jsonify({"ok": False, "error": "unauthorized", "message": "Invalid API key"}), 401
        now = time.time()
        b = _bucket_id()
        dq = _buckets[b]
        while dq and now - dq[0] >= WINDOW:
            dq.popleft()
        if len(dq) >= RATE_LIMIT:
            retry_after = int(WINDOW - (now - dq[0]))
            resp = jsonify({"ok": False, "error": "rate_limited", "message": "You are rate limited", "retry_after": retry_after, "remaining": 0})
            resp.status_code = 429
            resp.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
            resp.headers["X-RateLimit-Remaining"] = "0"
            resp.headers["Retry-After"] = str(retry_after)
            return resp
        dq.append(now)
        request._remaining = RATE_LIMIT - len(dq)

    @app.after_request
    def _headers(resp):
        if request.path.startswith("/api/"):
            resp.headers["X-RateLimit-Limit"] = str(RATE_LIMIT)
            rem = getattr(request, "_remaining", None)
            if rem is not None:
                resp.headers["X-RateLimit-Remaining"] = str(max(0, rem))
        return resp

def get_api_key():
    return API_KEY
