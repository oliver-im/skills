---
name: prune-tests
description: Sweep an existing test suite, give every test in scope a verdict, and implement removals or consolidation when cleanup is requested. Use when the user asks to prune, slim, de-bloat, or clean up existing tests, or to find redundant or low-value tests. Not for writing new tests or finding missing coverage; use write-tests for that.
---

# Prune Tests

A test earns its place when it catches a credible failure that other retained tests miss, or catches it much sooner or more clearly, and its expected result does not come from the code under test. Every test in scope must show this; already being in the suite is not a reason to stay.

For requests to find or review redundancy, report the ledger and recommended changes. For requests to prune or otherwise implement cleanup, apply the justified removals, merges, and rewrites.

This is a pass over tests, not over behaviors. Probing behaviors finds gaps but never reaches most tests, so it cannot find waste. If you notice a gap along the way, record it for write-tests and keep sweeping.

Count maintenance cost as breakage on behavior-preserving refactors, fixtures and mocks to maintain, and the reading time a test adds. Runtime rarely decides.

## Build the ledger

Enumerate every test in the requested scope before judging any, so none is skipped by omission. Record each in a ledger with its location, the contract it claims to protect, a verdict, and a one-line reason. The sweep is complete when every entry has a verdict; report partial coverage plainly.

Record each test as its source defines it: a table, a parametrized test, or a loop that generates tests is one entry, even when the runner and tools report each case separately. Attribute catches to the whole group.

For large suites, work in chunks by module or file, and fan out across subagents when available, giving each the same bar and ledger format. Share a common baseline and evidence across chunks so their verdicts can be reconciled. Keep the ledger where the next run can resume it, such as the PR description or an unmerged working file.

Establish a green baseline first. Diagnose failing tests rather than deleting them to get a passing run.

## Gather evidence

Two lenses find different waste; apply both.

**Redundancy.** Find what each test uniquely catches. Prefer mutation testing that records every test failing for each mutant. When no tool fits, inject faults directly and record their catchers. For a report in StrykerJS's JSON format, `scripts/attribute.py` lists what each test catches alone, checks a set of removals jointly, and compares a rerun against the baseline. Limit mutation to the source the chunk's tests exercise, and exclude mutants rejected by the required type check or compile step. Count a unique catch only when the fault violates a contract worth preserving. Per-test coverage is a weaker fallback: it shows what a test executes, not what it checks.

Mutation and probe results cover only the faults exercised. A lack of unique catches in that sample does not establish redundancy. Check that the evidence reaches the code and contract each test claims to protect. For each removal candidate, name the credible failures outside the sample and probe the ones that decide its verdict. Credit failures on the intended contract, rather than unrelated failures caused by the probe. Inject faults in an isolated copy, rebuild what the tests execute, collect the suite's catchers, and restore each fault afterward.

Count a catch only when it reproduces. Before a verdict rests on a catch, confirm the injected fault caused it; an intermittent catch does not preserve the protection of a reliable one. Bound probe runs so a fault that hangs the suite can be assessed without stalling the sweep.

**Restating the implementation.** Read each test against its code and contract; mutation results alone cannot establish that its expectations are sound. An expectation computed by the code under test can change alongside a defect and keep passing. An unreviewed snapshot detects output changes without proving the original output correct. Assertions on private helpers, call sequences, or intermediate data that no caller relies on can reject correct refactors. Constants, serialization, and call order can be contracts; name the caller or requirement that depends on them before keeping a test on that basis.

Reject checks where mocks supply the behavior supposedly under test. Mock data can still support a useful check that production code selects, forwards, transforms, or preserves a dependency's result as required by a contract.

Also look for tests whose assertions do not match their names, tests of code with no production caller, and near-duplicates that differ only in inputs. Verify that each test's setup allows its assertions to expose the failure it claims to catch.

## Decide

Judge removals together against the suite that will remain. For each removal, record which retained tests preserve its protection, or why the behavior no longer needs protection. Two equivalent tests may each have no unique catch; retain at least one while their contract still needs protection. Reconcile these dependencies across chunks before applying changes.

- **Keep** a test that uniquely catches a credible failure among the retained tests, and name that failure. Keep an overlapping test only when you can name the failure it pinpoints much faster or more clearly than the others that catch it.
- **Remove** a test that catches nothing unique and has no named reason to stay, or that restates the implementation.
- **Merge** tests that exercise one contract with different inputs, for example into a table-driven test; a table pays off when its rows share setup and assertions. Trimming the rows of an existing table rarely saves maintenance.
- **Rewrite** a test for a real contract when it relies on implementation details, has a misleading name, cannot expose its claimed failure, or costs more than a smaller test would.
- **Unresolved** only when the evidence could not be gathered in this run, or when the verdict waits on a decision only the code's owner can make. Record what would settle it, so the next run can.

Before removing a test that uniquely catches something, add or strengthen the replacement protection first, following write-tests.

When the code a test covers has no production caller, decide with that code rather than the test. Distinguish unused behavior from a deliberate defensive contract or planned use: judge whether the behavior should remain before removing its protection. Retire code and tests together when the behavior is no longer needed; preserve both when it is. After deleting code, check whether it was the last caller of anything else.

## Apply and verify

When cleanup is requested, make the changes on a focused branch, and update anything that names a removed test or deleted code, such as docs and agent guidance, in the same change. Keep before-and-after evidence comparable, and distinguish protection lost through test changes from intentionally retired behavior. Verify that rewritten tests catch their named failure and retain the protection of tests they replace. Rerun the suite and the same mutation run or fault probes. Every fault caught before must still be caught, apart from ones you deliberately accepted and explained. This establishes preservation for the exercised faults, not all possible regressions. A green suite alone does not show that protection survived. Run the repository's required gates.

Report verdict counts, tests and lines removed, suite time before and after, mutation or probe results before and after, the keeps that rest on reasoning rather than a caught fault, the unresolved entries, and the scope not yet swept. For a review-only request, report proposed changes and available evidence without implying that changes or post-change checks ran.
