# Skill Benchmark: openspec-agy-delivery

**Model**: cliproxyapi/gpt-5.6-sol
**Date**: 2026-09-03T07:48:19Z
**Evals**: 4, 5, 6 (1 run each per configuration)

**Tested skill SHA-256**: `662c16bad4251476f7f7c3cb468c7d442eaee133cda99535c45df9879de6064a`
**Baseline SHA-256**: `e4666a7afd2bd34db226c2e74887172268738b244e2f67b5a7ee08f4787bf1cc`

## Summary

| Metric | Old Skill | With Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 72% ± 30% | 100% ± 0% | +0.28 |
| Time | 49.7s ± 22.8s | 40.6s ± 26.9s | -9.1s |
| Output chars | 6421 ± 4728 | 5430 ± 5699 | -991 |

Delta is `with_skill - old_skill`. Output characters are a token proxy.

Eval 7 is a fresh-OMP integration check with a 100% grade. It is retained beside this benchmark and excluded from paired statistics because no old-skill resolver baseline was run.