# ADR 0003 — Numerical Backend for $\mathrm{dejai^2}$

## Status
Proposed

## Context
The project must support:
- **Lightweight local runs** on the instructor’s MacBook Air (Apple Silicon).
- **Fast array math** for solvers, autograding, and moderate simulations.
- **Cross-platform portability** (Linux + CUDA, Mac + Metal, CI with CPU).
- **Future scalability** to heavier hardware if needed.

Options considered:
- **NumPy only:** simple, portable, but lacks GPU/TPU backends.
- **PyTorch:** powerful, but heavier dependency; GPU drivers vary.
- **JAX:** NumPy-like API, supports CPU, CUDA, and Apple Metal (experimental), good for functional composition and JIT.

## Decision
- Standardize on **JAX** as the numerical backend.
- Use **CPU backend** as the baseline (portable, stable).
- Enable **Metal GPU backend** on Apple Silicon for acceleration, but treat as experimental.
- For small, simple routines (grading, demos), allow fallback to pure NumPy.
- Avoid CUDA-only or vendor-locked code paths.

## Consequences
**Positive**
+ Unified array programming model (NumPy-like).  
+ Runs cross-platform (CPU everywhere; GPU where available).  
+ Potential to JIT-compile kernels for speedups.  
+ Students can run on MacBooks without extra setup.  

**Negative**
− Metal backend incomplete (no float64, missing ops).  
− JAX adds learning curve beyond NumPy.  
− May need guards/fallbacks for unsupported ops.  
− Less mature ecosystem on macOS vs Linux/CUDA.

## Out of Scope
- Training large ML models (dejai² is not an ML training pipeline).  
- Custom CUDA kernels (unnecessary at this stage).  
- Full reliance on Metal GPU (keep CPU baseline first).

## Milestones
1. Add JAX dependency (CPU backend) and validate on Mac + Linux.  
2. Wrap solvers with JAX vectorized/`jit` variants.  
3. Provide NumPy fallback for unsupported ops or CI sanity.  
4. Add Metal GPU option for Apple Silicon; document dtype/feature caveats.  
5. Benchmark representative problems (SR, mechanics) to guide usage.

## See Also
- ADR-0001 (Vision & Scope)
- ADR-0002 (Units Handling)
- ADR-0004 (Slide Engine)
