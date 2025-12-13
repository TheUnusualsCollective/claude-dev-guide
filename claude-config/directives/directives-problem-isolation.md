# Coding Directive: Problem Isolation

**Purpose**: Prevent wasted effort by reducing problems to minimal cases before attempting solutions.

**Last Updated**: 2025-12-13

---

## Core Principle

**Reduce problems to their smallest form, verify thoroughly, then expand scope.**

Solutions that appear correct under one condition often fail under others (false positives). Never scale up until minimal cases pass multiple verification conditions.

---

## The Workflow

```
1. REDUCE  - Isolate smallest case that demonstrates the problem
2. SOLVE   - Fix the minimal case only (in isolation, not production code)
3. VERIFY  - Test against MULTIPLE conditions (not just the failing one)
4. EXPAND  - Increase scope only after thorough verification
```

---

## Protect Working Code

**Do not modify production/canonical code until the fix is proven.**

- Debug in isolation: throwaway scripts, test files, or separate branch
- Production code stays untouched during investigation
- Only apply fix to canonical code after verification passes
- This prevents introducing new bugs while fixing old ones

---

## False Positive Risks

A solution is NOT verified if it only passes one test:

| Single Test | Risk |
|-------------|------|
| One input type | Other types may have different edge cases |
| One test case | May accidentally match without being correct |
| Visual check only | Eye misses subtle errors; verify numerically |
| "It runs without errors" | Silent failures produce plausible-looking wrong output |

---

## Reducing to Minimal Cases

When a problem is discovered:

1. **Don't fix in the full pipeline** - extract the failing case
2. **Isolate the stage** - which step produces wrong output?
3. **Isolate the input** - which specific data triggers the issue?
4. **Print intermediate values** - compare expected vs actual at each step

---

## Expanding Scope Safely

After minimal case passes:

1. Add variations (different inputs, same operation)
2. Add complexity (multiple operations, same input type)
3. Test representative sample before full batch
4. **If any expansion fails: return to minimal case** - don't debug at scale

---

## Checklist

- [ ] Problem reduced to minimal reproducible case
- [ ] Fix developed in isolation (not in production code)
- [ ] Solution verified against multiple conditions
- [ ] Intermediate values checked (not just final output)
- [ ] Expansion tested incrementally, not all at once
- [ ] Production code modified only after full verification

---
