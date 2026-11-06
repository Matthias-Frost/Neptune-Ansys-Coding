# Setup Guide: Python, Git, and VS Code for PyFluent

This guide gets your Windows machine ready to run the group's PyFluent scripts.
Do the steps **in order**. Each one ends with a **✅ Check** that confirms it worked before you move on.
The step numbers match your **Setup checklist** issue on GitHub.

**Time:** about 30–45 minutes (most of it is waiting for downloads).

---

## How the pieces fit together

It helps to know what you're installing and why:

| Piece | What it does |
|---|---|
| **Ansys Fluent 2023 R1** | The solver. PyFluent doesn't replace it; it *drives* it. |
| **Python 3.10** | The language our scripts are written in. |
| **Virtual environment (`.venv`)** | A private copy of Python packages just for this project, so versions here can't clash with anything else on your PC. |
| **PyFluent (`ansys-fluent-core`)** | A Python library that launches Fluent and sends it commands over a network connection (gRPC). |
| **Git + GitHub** | Version control: how we share code and keep everyone's copy in sync. |
| **VS Code** | The editor where you write and run scripts. |

When you run a script, it goes like this: your script runs in the `.venv`, PyFluent finds your Fluent
install through an environment variable (`AWP_ROOT231`), starts Fluent in the background, and sends
it setup/solve commands.

---

## Step 0 — Before you start

- [ ] **Ansys 2023 R1 is installed and Fluent opens normally** from the Start menu (it gets a
      license and shows the launcher). If Fluent can't open by itself, PyFluent can't either.
      Fix that first.
- [ ] **You have a GitHub account** and have **accepted the invite** to this repository
      (check your email or github.com/notifications).

✅ **Check:** Open PowerShell (Start → type `PowerShell`) and run:

```powershell
echo $env:AWP_ROOT231
```

You should see something like `C:\Program Files\ANSYS Inc\v231\`. The Ansys installer sets this
variable, and it's how PyFluent finds Fluent. If it prints nothing, see
[Troubleshooting](#troubleshooting).

---

## Step 1 — Install Python 3.10 (64-bit)

We use **3.10** because it matches the PyFluent version that supports our Fluent 2023 R1.
It's fine if you already have another Python installed; they can live side by side.

1. Go to <https://www.python.org/downloads/release/python-31011/>.
2. Scroll to **Files** and download **Windows installer (64-bit)**.
   (3.10.11 is the last 3.10 release that has a Windows installer, so it's the one to use.)
3. Run the installer. On the **first screen**:
   - ✔ **Use admin privileges when installing py.exe**
   - ✔ **Add python.exe to PATH** (optional; we use the `py` launcher below either way)
   - Click **Install Now**.
4. If it offers **Disable path length limit** at the end, click it.

✅ **Check:** Open a **new** PowerShell window and run:

```powershell
py -0
py -3.10 --version
```

`py -0` lists every Python on your machine. You should see `-V:3.10` in the list, and the second
command should print `Python 3.10.11`.

> **Why `py -3.10` instead of `python`?** If you have several Pythons installed, `python` runs
> whichever one comes first on your PATH, and that might not be 3.10. The `py` launcher lets you
> pick the exact version.

---

## Step 2 — Install Git and set your name

1. Download Git for Windows from <https://git-scm.com/downloads/win> and run the installer.
2. The defaults are fine. One change worth making: when asked for the **default editor**, choose
   **Visual Studio Code**.
3. Open a **new** PowerShell window and tell Git who you are (use the email on your GitHub account):

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

✅ **Check:**

```powershell
git --version
git config --global user.name
```

You should see a version number and your name.

---

## Step 3 — Install VS Code and the Python extension

1. Download and install VS Code from <https://code.visualstudio.com/>.
   During install, ✔ **Add "Open with Code" action to Windows Explorer** (handy, optional).
2. Open VS Code → click the **Extensions** icon in the left sidebar (four squares) or press
   `Ctrl+Shift+X`.
3. Search **Python** and install the one published by **Microsoft** (`ms-python.python`).
   It installs **Pylance** with it.

✅ **Check:** In the Extensions panel, **Python** and **Pylance** both show as installed.

---

## Step 4 — Clone the repository

"Cloning" downloads the repo to your PC with its Git history, so you can pull updates and push changes.

1. In VS Code press `Ctrl+Shift+P` (the **Command Palette**) and run **Git: Clone**.
2. Choose **Clone from GitHub**. A browser window opens; sign in and **authorize VS Code**.
3. Pick this repository from the list.
4. Choose a parent folder, for example `C:\Users\<you>\`. VS Code creates the `ansys-automation`
   folder inside it.
5. When asked, click **Open** (and **Yes, I trust the authors**).

> **Folder location matters:**
> - **Avoid OneDrive folders** (Desktop/Documents are often synced). OneDrive fights with the
>   thousands of small files in `.venv` and Fluent's output files.
> - **Avoid spaces and special characters** in the path. Fluent can have trouble with them.
>   `C:\Users\you\ansys-automation` is good.

✅ **Check:** The VS Code Explorer (left sidebar) shows `README.md`, `requirements.txt`, `docs`,
`scripts`, and `models`.

---

## Step 5 — Create the virtual environment

1. In VS Code open a terminal: **Terminal → New Terminal** (or `` Ctrl+` ``).
   It should be **PowerShell** and already in the repo folder.
2. Create the venv with Python 3.10:

```powershell
py -3.10 -m venv .venv
```

   This creates a `.venv` folder containing a private Python 3.10. (`-m venv` means "run Python's
   built-in `venv` module".) Git ignores this folder, so it never gets uploaded.

3. Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

   If you get **"running scripts is disabled on this system"**, run this once, then try again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

✅ **Check:** Your prompt now starts with `(.venv)`, and:

```powershell
python --version
```

prints `Python 3.10.11`. Once the venv is active, `python` means the venv's Python.

---

## Step 6 — Install the project packages

With the venv **active** (you see `(.venv)`):

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

`-r requirements.txt` installs the **exact** versions listed in that file, the same versions
everyone else has. This can take a few minutes.

> Always use `python -m pip`, not just `pip`. It guarantees you're installing into the Python
> that's active, not some other one.
>
> **Do not upgrade `ansys-fluent-core`.** Newer versions don't support Fluent 2023 R1.

✅ **Check:**

```powershell
python -m pip show ansys-fluent-core
```

The `Version:` shown matches the one in `requirements.txt`.

---

## Step 7 — Point VS Code at the venv

VS Code needs to know which Python to use when you click **Run**.

1. Press `Ctrl+Shift+P` → **Python: Select Interpreter**.
2. Choose the one marked **`.venv`**, at the path `.\.venv\Scripts\python.exe`.
   (The repo's `.vscode/settings.json` usually selects it for you. Confirm it anyway.)
3. Close the terminal (trash-can icon) and open a new one. It should activate `(.venv)` on its own.

✅ **Check:** The bottom-right of the VS Code status bar shows **3.10.11 ('.venv')** when a `.py`
file is open.

---

## Step 8 — Verify everything

In the VS Code terminal, with `(.venv)` active:

```powershell
python scripts/check_setup.py
```

This checks your Python version, the venv, PyFluent, and the Fluent install. Fix anything marked
`FAIL`, then do the real test, which actually starts Fluent in the background, connects to it, and
shuts it down:

```powershell
python scripts/check_setup.py --launch
```

The first launch can take 1–2 minutes.

✅ **Check:** The last line says `ALL CHECKS PASSED`. Copy the full output into your checklist issue.

🎉 You're set up. Next, read [GIT_BASICS.md](GIT_BASICS.md) for the day-to-day pull/commit/push routine.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `py` is not recognized | Python wasn't installed with the launcher. Re-run the 3.10.11 installer → **Modify** → make sure **py launcher** is checked. |
| `py -3.10` says "No suitable Python runtime found" | 3.10 isn't installed, or you installed the 32-bit build. Install the **64-bit** installer from Step 1. |
| `Activate.ps1 cannot be loaded… running scripts is disabled` | Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`, then activate again. |
| Prompt doesn't show `(.venv)` | You're not activated. Run `.\.venv\Scripts\Activate.ps1` from the repo folder. |
| `No matching distribution found for ansys-fluent-core==REPLACE_WITH_WORKING_VERSION` | The repo lead hasn't pinned the version yet. Tell them. |
| `ModuleNotFoundError: No module named 'ansys'` | You ran a Python that isn't the venv. Activate the venv, and check the interpreter in the status bar (Step 7). |
| `echo $env:AWP_ROOT231` prints nothing | Ansys 2023 R1 isn't installed, or it's in a non-default place. Find the `v231` folder (default `C:\Program Files\ANSYS Inc\v231`), then set the variable: Start → "Edit environment variables for your account" → **New** → Name `AWP_ROOT231`, Value = that folder path. Restart VS Code. |
| Fluent launch hangs or times out | First, confirm Fluent opens normally from the Start menu (license OK). Then allow Fluent through Windows Firewall if prompted; PyFluent talks to Fluent over a local network port. |
| Installed something wrong and want to start over | Close VS Code, delete the `.venv` folder, and redo Steps 5–7. Nothing else is affected. |

Still stuck? Comment on your checklist issue with the **step number**, the **exact command**, and a
**screenshot of the full error**.
