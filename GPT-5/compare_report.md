# Comparison Report

## Summary Table
| Metric | Faulty | Optimized | Improvement |
|--------|--------|-----------|-------------|
| Test cases | 5 | 5 | - |
| Pass count | 4 | 5 | 1 |
| Pass rate | 80.00% | 100.00% | 20.00% |
| Avg time per run (5x large) | 0.001177s | 0.001319s | -12.01% faster |

## Key Fixes
- Removed unsafe eval; replaced with regex numeric parsing.
- Implemented full-depth traversal with iterative stack.
- Single-pass aggregation reduces complexity from O(n^2) to O(n).
- Proper handling of negative numeric strings and exclusion of malformed inputs.

## Reliability Differences
- Faulty version crashes on injection case; optimized handles securely.
- Faulty miscounts nested values; optimized returns complete statistics.
- Performance improved measurably on large dataset.