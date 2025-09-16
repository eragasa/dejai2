# ADR 0002 — Units Handling in $\mathrm{dejai^2}$

## Status
Proposed

## Context
Physics problems must carry units correctly for teaching and grading.  
- **Pint** provides transparent unit checking, useful for classroom demos and catching mistakes.  
- However, Pint introduces overhead that becomes significant in computationally heavy routines (loops, simulations).  
- We need a compromise: safety for small/medium tasks, speed for larger numerical kernels.

## Decision
- Adopt a **two-layer solver pattern**:
  - **Wrapper layer:** Pint quantities for inputs/outputs (unit safety, pedagogy).  
  - **Core layer:** raw floats/arrays (NumPy, JAX) for performance.  
- Use SI base units internally (`m`, `s`, `kg`, etc.) for all computations.  
- Limit Pint use to:
  - Autograder checks
  - Demo notebooks
  - Lightweight classroom computations
- For production/large runs, convert at boundaries and compute with floats.

## Consequences
**Positive**
+ Students and instructors see units explicitly in examples.  
+ Safer autograding (unit mismatches trigger errors).  
+ Performance preserved for heavier workloads.  

**Negative**
− Slight code duplication (wrapper + core).  
− Extra conversion steps when bridging Pint ↔ floats.  
− Must maintain discipline: don’t leak Pint into core loops.

## Out of Scope
- Symbolic units algebra beyond what SymPy provides.  
- Optimizing Pint for HPC (not required).  
- Supporting multiple unit systems beyond SI (may revisit later).

## Milestones
1. Create base `dejai2/solvers/` modules with float cores.  
2. Wrap cores with Pint-safe interfaces.  
3. Add `pytest` unit tests for both wrappers and cores.  
4. Document usage guidelines (when to use Pint vs floats).  
5. Add autograder checks for unit consistency.

## See Also
- [[adr0001-vision-and-scope]]
- ADR-0003 (Numerical Backend — JAX on ARM)
