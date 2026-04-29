# Invisible Until Invited
## The Rural Pre-Faculty Readiness Matrix — Streamlit App

Companion to *Invisible Until Invited: Rewriting the Pre-Faculty Pipeline in Rural Medical Schools Through Data, Identity, and Academic Socialization* — BNGAP 2026, NYC.

---

## What's in this folder

- `app.py` — the Streamlit application
- `appalachian_medical_schools.csv` — the dataset (20 schools, all metrics)
- `requirements.txt` — Python dependencies
- `README.md` — this file

---

## Deploy to Streamlit Community Cloud (free, public URL)

### Step 1 — Put the files in a GitHub repo

1. Go to **github.com** and sign in.
2. Click the **"+"** in the top-right → **"New repository."**
3. Name it something like `invisible-until-invited-bngap-2026`.
4. Set visibility to **Public** (Streamlit Community Cloud requires public repos on the free tier).
5. Check **"Add a README"** (you can replace it).
6. Click **"Create repository."**
7. On the new repo page, click **"Add file" → "Upload files."**
8. Drag in all four files: `app.py`, `appalachian_medical_schools.csv`, `requirements.txt`, `README.md`.
9. Scroll down and click **"Commit changes."**

### Step 2 — Deploy to Streamlit Community Cloud

1. Go to **share.streamlit.io** and sign in with GitHub.
2. Click **"New app."**
3. Select the repository you just created.
4. Set the branch to `main` and the main file path to `app.py`.
5. Click **"Deploy."**

Streamlit installs the dependencies and builds your app. The first deploy takes 2–4 minutes.

### Step 3 — Get your public URL

Once deployed, your app gets a public URL like `https://invisible-until-invited-bngap-2026.streamlit.app`. Anyone can visit this URL — no Streamlit account, no GitHub access required. Share it with your audience.

---

## Run locally (optional, for testing)

If you want to test the app on your own laptop before deploying:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Updating the dashboard later

When measured score data comes in (replacing the simulated scores):

1. Edit `appalachian_medical_schools.csv` with the new values.
2. Re-derive the `Quadrant` column using the cutoff-50 rule.
3. Commit and push the updated CSV to your GitHub repo.
4. Streamlit Community Cloud auto-redeploys within 1–2 minutes.

---

## Features

- **Filters sidebar** — degree, state, ARC scope, pipeline state (quadrant), institution type, rural mission, distressed-county toggle. Every chart updates reactively.
- **Four KPI cards** — schools selected, matriculants, Invisible Scholars cluster size, distressed-county count.
- **The Matrix** — Identity × Engagement scatter with hover tooltips; quadrant tints, boundary lines, named typology corners.
- **Geographic map** — Albers USA projection, every school hover-driven.
- **Resource gap** — NIH funding totals by pipeline state.
- **Pillar profile** — pick any school, see its five-pillar bar chart.
- **Compare two schools** — side-by-side panel with all metrics.
- **Apply to Your Institution** — workshop self-assessment with sliders, your school placed as a black star on the matrix, tailored interpretation identifying your most actionable pillar.
- **Sortable table** — every school, click any column to sort.

All hover tooltips are formatted with school name, location, quadrant, all five pillar scores, matriculants, NIH funding, faculty count, and ARC status.

---

## License & attribution

Created by Dr. Paris N. Johnson for BNGAP 2026, NYC. Built on the framework introduced in the conference abstract.
