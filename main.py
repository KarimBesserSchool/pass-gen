from flask import Flask, render_template, request, jsonify
import re, random, string
from auth import init_auth, get_api_key
import os
from dotenv import load_dotenv

load_dotenv()
stage = os.getenv("STAGE", "DEV")

app = Flask(__name__)
init_auth(app)


@app.get("/")
def home():
    return render_template("prev.html", api_key=get_api_key())

def has_sequence(p: str) -> bool:
    p = p.lower()

    qrow = "qwertyuiop"
    qrow_rev = qrow[::-1]
    digits = "0123456789"
    digits_rev = digits[::-1]

    seqs = set()
    seqs.update(qrow[i:i+3] for i in range(len(qrow) - 2))
    seqs.update(qrow_rev[i:i+3] for i in range(len(qrow_rev) - 2))
    seqs.update(digits[i:i+3] for i in range(len(digits) - 2))
    seqs.update(digits_rev[i:i+3] for i in range(len(digits_rev) - 2))

    for i in range(len(p) - 2):
        tri = p[i:i+3]
        if tri in seqs:
            return True
    return False

def check_pw(p):
    d = {
        "len": len(p) >= 8,
        "lower": re.search(r"[a-z]", p) is not None,
        "upper": re.search(r"[A-Z]", p) is not None,
        "digit": re.search(r"\d", p) is not None,
        "sym": re.search(r"[^\w\s]", p) is not None,
        "seq": not has_sequence(p)
    }
    s = sum(v for k, v in d.items() if k != "seq")
    ok = s >= 4 and d["seq"]
    return {"ok": ok, "score": s, "req": d}

@app.post("/api/check_password")
def api_check():
    j = request.get_json(silent=True) or {}
    p = j.get("password") or request.form.get("password", "")
    return jsonify(check_pw(p))


def gen_pw(n=12):
    pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*()-_=+[]{};:,.?/"]
    base = [random.choice(x) for x in pools]
    rest = [random.choice("".join(pools)) for _ in range(max(0, n - len(base)))]
    x = base + rest
    random.shuffle(x)
    pw = "".join(x)
    return pw if not has_sequence(pw) else gen_pw(n)


@app.get("/api/generate_password")
def api_gen():
    n = request.args.get("n", default=12, type=int)
    n = max(8, min(n, 64))
    pw = gen_pw(n)
    return jsonify({"password": pw})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))

    if stage.upper() == "DEV":
        app.run(host="0.0.0.0", port=port, debug=True)
    else:
        from gevent import pywsgi
        print(f"Gevent production server running on http://127.0.0.1:{port}")
        server = pywsgi.WSGIServer(("0.0.0.0", port), app)
        server.serve_forever()