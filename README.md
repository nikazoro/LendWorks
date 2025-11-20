# LendWorks ⚙️💼

A full-stack lending application.

This repo contains:

* **`backend/`** 🐍 – Python API
* **`frontend/`** 🌐 – JavaScript web client

---

## 🚀 Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py                 # replace with actual start file if different
```

---

## 💻 Frontend Setup

```bash
cd frontend
npm install
npm run dev                   # or npm start, depending on your setup
```

Open the URL shown in the terminal (usually **[http://localhost:3000](http://localhost:3000)**).

---

## 🔐 Environment Variables

Backend `.env` example:

```
DATABASE_URL=...
SECRET_KEY=...
```

Frontend `.env` example:

```
API_URL=http://localhost:8000
```

---

## 📁 Project Structure

```
/
├── backend/    🐍
├── frontend/   🌐
└── README.md
```

---

## 🧭 Development Workflow

Run backend and frontend in separate terminals.
Backend typically runs at **[http://localhost:8000](http://localhost:8000)**.
Frontend consumes the backend via your configured `API_URL`.

---

If you want, I can generate a version with cleaner GitHub-style badges (build status, Python version, Node version, etc.) or a more branded header.
