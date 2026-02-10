# Docker (Quickstart) — pass-gen

Minimal, **copy/paste** commands to get the repo, build the image, and run it.

---

## 0) Get the code (pick one)

### Option A — Download ZIP (no Git needed)

1. Open the repo on GitHub
2. Click **Code** → **Download ZIP**
3. Extract it
4. Open a terminal **in the extracted folder**

### Option B — Git clone (recommended)

```bash
git clone https://github.com/KarimBesserSchool/pass-gen.git
cd pass-gen
```

---

## 1) Build

From the folder that contains your `Dockerfile` and `main.py`:

```bash
docker build -t pass-gen .
```

---

## 2) Run (local)

Publish container port **5000** to your PC:

```bash
docker run --rm -p 5000:5000 pass-gen
```

Open:

- `http://localhost:5000`

---

## 3) Run (background)

```bash
docker run -d --name pass-gen -p 5000:5000 pass-gen
```

Logs:

```bash
docker logs -f pass-gen
```

Stop:

```bash
docker stop pass-gen
```

---

## 4) Environment variables

Your Dockerfile sets:

- `STAGE=PROD`
- `PORT=5000`

Override them at runtime like this:

```bash
docker run --rm -p 5000:5000   -e STAGE=PROD   -e PORT=5000   pass-gen
```

---

## 5) Common “works locally but not in Docker” fix

Your Flask server must listen on **0.0.0.0** (not just `127.0.0.1`).

In `main.py`, make sure your run line includes:

```py
app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
```

---

## (Optional) docker-compose

Create `docker-compose.yml`:

```yml
services:
  pass-gen:
    build: .
    ports:
      - "5000:5000"
    environment:
      STAGE: "PROD"
      PORT: "5000"
```

Run:

```bash
docker compose up --build
```

Stop:

```bash
docker compose down
```
