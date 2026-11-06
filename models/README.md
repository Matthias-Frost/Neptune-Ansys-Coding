# Models

One folder per simulation. Keep each model self-contained:

```
models/
└── <model-name>/          e.g. mixing-elbow, 9mm-bullet
    ├── README.md          what it is, inputs, how to run, where big files live
    ├── run.py             the main PyFluent script
    ├── mesh/              (ignored by Git; large mesh files stay local or on the shared drive)
    └── results/           (ignored by Git; written by the script)
```

**Rules of thumb**

- Scripts should use **paths relative to the script**, not `C:\Users\<you>\...`, so they run on
  anyone's machine:

  ```python
  from pathlib import Path
  HERE = Path(__file__).resolve().parent
  mesh_file = HERE / "mesh" / "bullet.msh.h5"
  ```

- Put every number you might change (Mach numbers, iterations, core count) in a clearly labeled
  block at the top of `run.py`.
- If a mesh is too big for Git, write in the model's README where to get it.
