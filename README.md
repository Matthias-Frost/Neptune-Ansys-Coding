# Ansys Automation

Python scripts that automate **Ansys Fluent** (and later **Static Structural**) using
[PyFluent](https://fluent.docs.pyansys.com/). The goal is to set up, run, and post-process
simulations from code instead of clicking through the GUI, so runs are repeatable and easy to share.

## New to the group? Start here

1. Follow the setup guide: **[docs/SETUP.md](docs/SETUP.md)** (about 30–45 minutes).
2. Open your setup checklist: go to the **Issues** tab → **New issue** → **Setup checklist** →
   put your name in the title → **Submit**. Tick the boxes as you go.
3. When every box is ticked, run `python scripts/check_setup.py --launch`, paste the output
   into your checklist issue, and close it.

Stuck? Comment on your checklist issue with the step number and a screenshot of the error.

## Our standard environment

Everyone uses the same versions so a script that runs on one machine runs on all of them.

| Item | Version |
|---|---|
| OS | Windows 10/11 (64-bit) |
| Ansys | 2023 R1 (`v231`), UCF license |
| Python | 3.10 (64-bit) |
| PyFluent | pinned in [`requirements.txt`](requirements.txt) |
| Editor | VS Code + Python extension |

> **Why not the newest PyFluent?** Current PyFluent releases (0.38 and newer) only support
> Fluent 2024 R2 and later. We're on 2023 R1, so we pin an older PyFluent that matches it.
> **Do not run `pip install --upgrade ansys-fluent-core`** — it will break your setup.

## Repo layout

```
ansys-automation/
├── README.md              ← you are here
├── requirements.txt       ← exact package versions everyone installs
├── docs/
│   ├── SETUP.md           ← install Python, Git, VS Code, and the project
│   └── GIT_BASICS.md      ← pull / commit / push workflow
├── scripts/
│   └── check_setup.py     ← verifies your environment (and optionally launches Fluent)
├── models/                ← one folder per simulation (see models/README.md)
├── .vscode/               ← shared VS Code settings (auto-picks the .venv interpreter)
└── .github/ISSUE_TEMPLATE/
    └── setup-checklist.md ← the onboarding checklist
```

## Ground rules

- **Never commit the `.venv` folder** or large Fluent output files (`.cas.h5`, `.dat.h5`, etc.).
  The `.gitignore` already blocks them; don't force-add them.
- **Pull before you start working** each session. See [docs/GIT_BASICS.md](docs/GIT_BASICS.md).
- If you need a new package, ask the repo lead before adding it to `requirements.txt`.

## For the repo lead: updating the pinned versions

`requirements.txt` should come from a venv where PyFluent is **known to work** with our Fluent.
From that working venv:

```powershell
python -m pip freeze > requirements.txt
```

Commit the result. Anyone already set up then runs `python -m pip install -r requirements.txt`.
