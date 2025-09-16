# ADR 0005 — Student Compute Environment (Google Colab)

## Status
Proposed

## Context
Students need a zero-install way to:
- Run solvers (NumPy/SymPy/JAX) for physics problems.
- Visualize results and work through labs interactively.
- Submit outputs to Canvas for grading.

Google Colab provides free CPU runtimes (always available) and optional GPU runtimes (NVIDIA). It is widely accessible and familiar to students, but it has session limits and varying package versions. Copyrighted textbook content must remain outside notebooks; problem statements are delivered via Canvas.

## Decision
- Adopt **Google Colab** as the official student compute environment.
- Use **NumPy + SymPy** as the baseline, available in all runtimes.
- Enable **JAX** where available:
  - CPU backend by default.
  - GPU backend (CUDA) in Colab’s GPU runtimes when supported.
- Use **Pint** only at the edges (inputs/outputs, unit checking), not in heavy loops.
- Distribute notebooks via **Canvas** (not public repos). Notebooks contain setup cells that pin versions.
- Students submit via Canvas:
  - Either download notebook outputs as PDF.
  - Or copy/paste structured JSON outputs for autograding.

## Consequences
**Positive**
+ No local installs required; works on laptops, Chromebooks, tablets.
+ Consistent experience across platforms.
+ Optional GPU acceleration for larger arrays.
+ Easy integration with Canvas assignments.

**Negative**
− GPU availability/versioning is inconsistent.  
− Internet connection required; sessions may time out.  
− Not suitable for long simulations (>1–2 hours).  
− Adds a dependency on Google’s service.

## Out of Scope
- Embedding copyrighted textbook text in notebooks.
- Running very large or long-duration simulations.
- Managing Google Drive permissions (handled by LMS policies).

## Milestones
1. Provide a **Colab template notebook** with setup, backend selector, and test cells.
2. Convert core demos (Galilean, Lorentz, time dilation) into Colab labs.
3. Add autograder-friendly cells (JSON schema outputs).
4. Document student workflow: open → run → export → submit via Canvas.
5. Validate version pins for each new semester.

## See Also
- [[adr0002-units]]
- [[adr0003-numerics_architecture]]
- 



##### Google Template Notebook
```python
#@title Setup (versions + installs)
!pip -q install numpy==1.26.4 sympy==1.12 pint==0.24.3

USE_JAX = True  #@param {type:"boolean"}

if USE_JAX:
  try:
    import os, subprocess, sys
    # Try CPU-only JAX first (works everywhere)
    !pip -q install --upgrade "jax[cpu]"
    import jax; print("JAX devices:", jax.devices())
    JAX_OK = True
  except Exception as e:
    print("JAX install failed, falling back to NumPy only.", e)
    JAX_OK = False
else:
  JAX_OK = False

import numpy as np, sympy as sp
from pint import UnitRegistry
u = UnitRegistry()
np.random.seed(123);  # reproducibility

```

##### Backend selection helper
```python
#@title Backend selection helpers
def gamma_numpy(beta):
  beta = np.asarray(beta, dtype=np.float64)
  if np.any((beta < 0) | (beta >= 1)): raise ValueError("0 ≤ β < 1 required")
  return 1.0 / np.sqrt(1.0 - beta**2)

if JAX_OK:
  import jax, jax.numpy as jnp
  @jax.jit
  def gamma_jax(beta):
    return 1.0 / jnp.sqrt(1.0 - beta**2)

def gamma(beta):
  return gamma_jax(beta) if JAX_OK else gamma_numpy(beta)
```

##### Example: Time dilation (with Pint at the edges)
```python
#@title Time dilation demo
def time_dilation(delta_t, v):
  """
  delta_t: Pint Quantity (seconds)
  v: Pint Quantity (m/s); v < c
  returns: Pint seconds
  """
  delta_t = delta_t.to(u.s)
  c = u.c
  beta = (v / c).to_base_units().magnitude
  g = float(gamma(beta))
  return g * delta_t

print(time_dilation(1*u.s, 0.6*u.c))
```

##### Quick check (Lorentz transform for one event)
```python
#@title Lorentz transform (1D boost)
def lorentz_transform(x, t, v):
  """
  x: Pint meters, t: Pint seconds, v: Pint m/s
  returns: (x', t') as Pint quantities
  """
  x = x.to(u.m); t = t.to(u.s); v = v.to(u.m/u.s); c = u.c
  beta = (v/c).magnitude
  g = float(gamma(beta))
  x_p = g * (x - v*t)
  t_p = g * (t - (v/(c**2))*x)
  return x_p.to(u.m), t_p.to(u.s)

x_p, t_p = lorentz_transform(300*u.m, 1.0e-6*u.s, 0.6*u.c)
x_p, t_p
```

##### Autograder-friendly output cell
```python
#@title Print results in JSON schema (for Canvas upload)
import json
res = {
  "td_0.6c": float(time_dilation(1*u.s, 0.6*u.c).to(u.s).magnitude),
  "lorentz_event": {"xprime_m": float(x_p.magnitude), "tprime_s": float(t_p.magnitude)},
  "backend": "jax" if JAX_OK else "numpy"
}
print(json.dumps(res, indent=2))
```