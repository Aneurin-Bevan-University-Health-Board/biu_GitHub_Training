# Exercise: Build Something with GitHub Copilot in a Codespace

**Used in:** [Session 8: GitHub Codespaces and Copilot Hands-On](../../08_Session_8_Codespaces_and_Copilot_Exercise.md)
**Time:** 25 minutes (working alone or in pairs)
**You need:** a GitHub account with Copilot access, and permission to open a Codespace on this repository

> ⚠️ **SYNTHETIC DATA ONLY.** The dataset in this exercise is completely made up. A Codespace runs in
> GitHub's cloud, **outside** the Secure Data Environment (SDE). Never upload real patient data, extracts,
> NHS numbers, or credentials to a Codespace, a repository, or a Copilot prompt.

---

## The scenario

An outpatient service manager asks: *"Which clinics and patient groups have the highest DNA
(did not attend) rates, and is it changing through the year?"*

You have a small synthetic dataset. Use **GitHub Copilot** to help you turn it into something useful.
**You choose the track:**

| Track | What you build | Good for |
|-------|---------------|----------|
| **A. Analysis** | A Python script that checks the data, calculates DNA rates and saves a chart | People who want to prepare analysis code |
| **B. UI** | A small Streamlit app with filters, headline numbers and charts | People who want to build something others can click through |

Both tracks use the same file: `Training/exercises/codespaces-copilot/data/synthetic_outpatient_appointments.csv`.

## The data

| Column | Meaning |
|--------|---------|
| `appointment_id` | Synthetic ID (`SYN-00001` ...), not linked to any real person |
| `appointment_date` | Date of the appointment (2025, weekdays only) |
| `speciality` | Cardiology, Diabetes, Dermatology, Ophthalmology, Orthopaedics, Respiratory |
| `clinic_site` | Site A, Site B or Site C |
| `age_band` | 16-24, 25-39, 40-59, 60-74, 75+ |
| `appointment_type` | New or Follow-up |
| `wait_days` | Days waited for the appointment |
| `attendance_status` | Attended, DNA or Cancelled |

**Metric definition (use this exactly):** `DNA rate = DNA ÷ (Attended + DNA)`. Cancelled appointments are **excluded**.

---

## Steps

### 1. Open a Codespace on your own branch (4 minutes)

You are carrying on with **your own area** from the earlier sessions.

1. On the repository page, switch to your branch `training/<your-folder>`, then select **Code → Codespaces → Create codespace on training/<your-folder>**.
2. Wait for the environment to build. Python, pandas, matplotlib and Streamlit are installed for you.
3. Open the terminal (`` Ctrl+` ``) and create your working folder:

   ```bash
   mkdir -p participants/<your-folder>/dna-analysis
   ```

   All of your files go in this folder. Do **not** edit anything under `Training/`. Your own `.gitignore` (Session 3) keeps CSV files and `outputs/` out of Git.

### 2. Get to know the data (2 minutes)

Open `Training/exercises/codespaces-copilot/data/synthetic_outpatient_appointments.csv` (read it, do not change it). Open **Copilot Chat** and ask it to explain the columns.
Compare its answer with the table above. Does it match?

### 3. Build your track with Copilot (12 minutes)

Create a new file in `participants/<your-folder>/dna-analysis/` (for example `my_analysis.py` or `my_app.py`) and have it read the data file from the path above. Don't paste a full spec;
work in small steps and **read every suggestion before you accept it**.

**Track A: Analysis ideas to try (in Copilot Chat or as comments)**

1. *"Write a function that loads the CSV with pandas and checks for duplicate IDs, missing values and unexpected attendance_status values."*
2. *"Add a function that calculates DNA rate, excluding cancelled appointments."*
3. *"Show DNA rate by speciality and by age band."*
4. *"Plot DNA rate by month and save the chart to an `outputs/` folder."*

**Track B: UI ideas to try**

1. *"Create a Streamlit app that loads the CSV and shows the number of appointments and the DNA rate."*
2. *"Add sidebar filters for speciality and clinic site."*
3. *"Add a bar chart of DNA rate by speciality and a line chart by month."*
4. *"Handle the case where the filters return no rows."*

Run it:

```bash
python my_analysis.py            # Track A
streamlit run my_app.py          # Track B (open the forwarded port when prompted)
```

**Stuck?** Try `/explain` on an error, `/fix` on a broken block, or ask Copilot to explain what a line does.

### 4. Review what Copilot gave you (4 minutes)

Copilot can be confidently wrong. Check:

- [ ] Does the DNA rate **exclude cancelled** appointments, as defined above?
- [ ] Do totals look sensible? (There are 3,000 appointments in the file.)
- [ ] Are there any invented column names or library functions? Does the code actually run?
- [ ] Any hard-coded file paths, secrets, or code that sends data somewhere?
- [ ] Could you explain every line to a colleague? If not, ask Copilot to explain it, or simplify it.
- [ ] Are chart titles and labels clear and in UK English?

### 5. Save your work the GitHub way (3 minutes)

```bash
git add participants/<your-folder>/dna-analysis
git commit -m "Add DNA analysis using synthetic data"
git push
```

Your pull request from Session 3 updates automatically. Refresh it, add a short description (what you built, what you changed from Copilot's first
attempt), and ask a neighbour to review it.

### 6. Stop your Codespace

Use **Codespaces: Stop Current Codespace** from the Command Palette (`Ctrl+Shift+P`), or stop it from
[github.com/codespaces](https://github.com/codespaces). Stopped Codespaces don't use compute time.

---

## Share back (in the session)

| Item | Your answer |
|------|-------------|
| Track chosen | A or B |
| One thing Copilot did well | |
| One thing Copilot got wrong or you had to fix | |
| Would you use this at work? For what? | |

## Stretch tasks

- Ask Copilot to write `pytest` tests for your DNA-rate function (including an empty-data case).
- Open `.github/copilot-instructions.md`. How did these shared instructions change Copilot's answers (UK English, the DNA definition)? Try editing them.
- Add a README section to your branch describing how to run your code.
- Track A: add a chart of DNA rate by `age_band`. Track B: add an `age_band` filter.

---

## For instructors

- Reference solutions are in [`instructor/`](instructor/): `solution_analysis.py`, `solution_app.py`, and `test_solution.py`. Use them to check participants' output; don't share them up front.
- Regenerate the dataset with `python generate_synthetic_data.py` (fixed seed: everyone gets the same file).
- Patterns planted in the synthetic data: DNA rates are highest in **Diabetes** and **Dermatology** and in the **16-24** age band; **Cardiology** and the **60-74** band are lowest. The monthly trend is deliberately noisy (only a small winter uplift), so it's a good prompt to discuss not over-interpreting small-number variation.
- **No Copilot seat or Codespaces permission?** Run it as a pair exercise on one person's screen, or demo it from the instructor's Codespace.
- Confirm before the session: Codespaces enabled for the organisation, Copilot seats assigned, and who pays for Codespaces usage.
