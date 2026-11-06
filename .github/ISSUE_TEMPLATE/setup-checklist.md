---
name: Setup checklist
about: Your personal onboarding checklist. Open one, then tick boxes as you finish each step.
title: "Setup checklist: <your name>"
labels: ["onboarding"]
assignees: ""
---

Follow **[docs/SETUP.md](../blob/main/docs/SETUP.md)** and tick each box when its ✅ Check passes.
(Tick boxes right here on the issue page; no editing needed.)

**Assign this issue to yourself** (right sidebar → Assignees) so the group can see who's where.

### Step 0 — Before you start
- [ ] Fluent 2023 R1 opens normally from the Start menu
- [ ] Accepted the GitHub repo invite
- [ ] `echo $env:AWP_ROOT231` prints the v231 folder

### Step 1 — Python 3.10
- [ ] Installed Python 3.10.11 (64-bit)
- [ ] `py -3.10 --version` prints `Python 3.10.11`

### Step 2 — Git
- [ ] Installed Git for Windows
- [ ] Set `user.name` and `user.email`

### Step 3 — VS Code
- [ ] Installed VS Code
- [ ] Installed the Microsoft **Python** extension (Pylance comes with it)

### Step 4 — Clone
- [ ] Cloned the repo to a non-OneDrive folder with no spaces in the path

### Step 5 — Virtual environment
- [ ] Created `.venv` with `py -3.10 -m venv .venv`
- [ ] Activated it; prompt shows `(.venv)`

### Step 6 — Packages
- [ ] Ran `python -m pip install -r requirements.txt`
- [ ] `ansys-fluent-core` version matches `requirements.txt`

### Step 7 — VS Code interpreter
- [ ] Status bar shows **3.10.11 ('.venv')**

### Step 8 — Verify
- [ ] `python scripts/check_setup.py` passes
- [ ] `python scripts/check_setup.py --launch` ends with `ALL CHECKS PASSED`
- [ ] Pasted the output below

### Bonus — Git workflow
- [ ] Read [docs/GIT_BASICS.md](../blob/main/docs/GIT_BASICS.md)

---

**My machine** (optional, helps when debugging):
- CPU / RAM:
- Windows version:

**check_setup.py output:**
```
paste here
```

**Problems I hit / notes for the next person:**

