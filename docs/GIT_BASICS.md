# Git Basics: the day-to-day routine

You only need a handful of Git actions. Everything below can be done from VS Code's
**Source Control** panel (the branch icon in the left sidebar, `Ctrl+Shift+G`) or from the terminal.

## The loop

```
pull  →  work  →  stage  →  commit  →  pull  →  push
```

| Action | What it means | VS Code | Terminal |
|---|---|---|---|
| **Pull** | Download everyone else's latest changes | `…` menu → **Pull** | `git pull` |
| **Stage** | Choose which changed files go into your next snapshot | **+** next to the file | `git add <file>` |
| **Commit** | Save a snapshot locally, with a message | type a message → **Commit** | `git commit -m "message"` |
| **Push** | Upload your commits to GitHub | **Sync Changes** / **Push** | `git push` |

**Always pull before you start working**, and pull again right before you push.

## Good commit messages

Short, present tense, says *what* changed:

- ✅ `Add Mach sweep loop to bullet script`
- ✅ `Fix inlet velocity units in mixing elbow`
- ❌ `stuff`, `update`, `asdf`

## Working on something bigger? Use a branch

A branch is your own copy of the code to experiment in without affecting `main`.

1. Bottom-left of VS Code, click the branch name (`main`) → **Create new branch** →
   name it like `matt/bullet-mach-sweep`.
2. Commit and push as usual.
3. On GitHub, open a **Pull Request** from your branch into `main` so someone can review it
   before it's merged.

## What never goes in Git

The `.gitignore` handles this automatically, but know why:

- `.venv/` — everyone builds their own from `requirements.txt`.
- Fluent case/data/mesh files (`.cas.h5`, `.dat.h5`, `.msh`) — often hundreds of MB.
  GitHub rejects files over 100 MB, and big files bloat the repo for everyone forever.
- Transcripts and logs (`.trn`, `.log`).

Commit **scripts and small settings files**. Share big meshes/results another way (shared drive)
and note the location in the model's README.

## Uh-oh moments

| Situation | Fix |
|---|---|
| "Your local changes would be overwritten by merge" on pull | Commit your changes first, then pull. |
| Merge conflict (`<<<<<<<` markers in a file) | VS Code highlights both versions. Click **Accept Current / Incoming / Both**, save, stage, commit. Ask if unsure. |
| Committed something you shouldn't have, not pushed yet | Ask the repo lead before trying to undo it. |
