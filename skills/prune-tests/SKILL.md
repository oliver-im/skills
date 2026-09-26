---
name: prune-tests
description: Sweep an existing test suite, give every test in scope a verdict, and implement removals or consolidation when cleanup is requested. Use when the user asks to prune, slim, de-bloat, or clean up existing tests, or to find redundant or low-value tests. Not for writing new tests or finding missing coverage; use write-tests for that.
---

# Prune Tests

A test earns its place when it catches a credible failure that other retained tests miss, or catches it much sooner or more clearly, and its expected result does not come from the code under test. Every test in scope must show this; already being in the suite is not a reason to stay.

For requests to find or review redundancy, report the ledger and recommended changes. For requests to prune or otherwise implement cleanup, apply the justified removals, merges, and rewrites.

This is a pass over tests, not over behaviors. Probing behaviors finds gaps but never reaches most tests, so it cannot find waste. If you notice a gap along the way, record it for write-tests and keep sweeping.

Count maintenance cost as breakage on behavior-preserving refactors, fixtures and mocks to maintain, and the reading time a test adds. Runtime rarely decides. Version history can measure the breakage: apply a past change's source edits without its test edits, see which tests fail, and judge each failure against the test's contract rather than the commit's intent.

## Build the ledger

Enumerate every test in the requested scope before judging any, so none is skipped by omission. Record each in a ledger with its location, the contract it claims to protect, a verdict, and a one-line reason. The sweep is complete when every entry has a verdict; report partial coverage plainly.

Record each test as its source defines it: a table, a parametrized test, or a loop that generates tests is one entry, even when the runner and tools report each case separately. Attribute catches to the whole group.

For large suites, work in chunks by module or file, and fan out across subagents when available, giving each the same bar and ledger format. Build the evidence and its tools once before fanning out, so every chunk judges against the same baseline, mutation run, and way of injecting faults. Have chunk agents record verdicts without editing tests, and keep agents that edit in parallel in separate working copies. Keep the ledger where the next run can resume it, such as the PR description or an unmerged working file.

Establish a green baseline first, including a run in shuffled order; a test that fails only after certain others points at one that leaks state. Diagnose failing tests rather than deleting them to get a passing run.

## Gather evidence

Two lenses find different waste; apply both.

**Redundancy.** Find what each test uniquely catches. Prefer a mutation tool that records every test failing for each mutant, such as StrykerJS with `coverageAnalysis: "perTest"` and `disableBail: true`. When no tool fits the test runner or reaches the code the tests run, apply generated mutants the way you inject faults below: write each into the source, and record every test that fails. For a report in StrykerJS's JSON format, `scripts/attribute.py` lists what each test catches alone, checks a set of removals jointly, and compares a rerun against the baseline. Estimate the run's cost before starting it. Uniqueness needs complete catcher lists only for mutants that one or two tests catch, so when recording every failure is too slow, stop each mutant's run after a few failing tests. Treat a capped list as a lower bound: it can report protection as lost when it is not, never the reverse, so recheck any capped mutant a verdict relies on. Limit mutation to the source the chunk's tests exercise, and enable the type check or compile step CI runs, so mutants CI would reject do not count as test catches. Count a unique catch only when the mutant is a failure a user or caller would notice; a branch that upstream validation makes unreachable does not qualify. A test with no unique catch is a removal candidate, once you have checked that the tool mutated the code it asserts on. Tools skip some regions entirely, such as templates, markup, styles, or the inside of patterns, and a test that guards only those looks inert. Per-test coverage is a weaker fallback: it shows what a test executes, not what it checks.

Mutation and probe results cover only the faults exercised. A lack of unique catches in that sample does not establish redundancy. A fault is exercised only when it reaches the code the tests actually run. A tool that switches mutants on inside the test process never reaches code the tests load another way, such as a built artifact, a child process, or a copied or embedded source, so those tests look inert. Mutation tools also rarely generate off-by-one limits, dropped fields, reordered calls, or narrowed character ranges. For each candidate, name the credible failures of its contract outside the sample and inject the ones that decide its verdict. Inject each in an isolated copy, rebuild what the tests execute, run the whole suite without stopping at the first failure, and restore the fault before the next. A fault that breaks shared setup, an import, or rendering fails every test that loads it, so that catch says nothing about any one test; make the fault reach only the contract under test.

Count a catch only when it reproduces. Load, timing, test order, and shared state can fail a test for reasons unrelated to the fault, and a race may be caught only when the scheduler happens to expose it. Before a verdict rests on a catch, rerun it in isolation; a test that catches a failure only intermittently does not preserve the protection of one that catches it every time. Give every run a timeout, so a fault that makes tests hang is recorded as caught rather than stalling the sweep.

**Restating the implementation.** Read each test against its code and contract; mutation results alone cannot establish that its expectations are sound. An expectation computed by the code under test can change alongside a defect and keep passing. An unreviewed snapshot detects output changes without proving the original output correct. Assertions on private helpers, call sequences, or intermediate data that no caller relies on can reject correct refactors. Constants, serialization, and call order can be contracts; name the caller or requirement that depends on them before keeping a test on that basis.

Reject checks where mocks supply the behavior supposedly under test. Mock data can still support a useful check that production code selects, forwards, transforms, or preserves a dependency's result as required by a contract.

Also look for tests whose assertions do not match their names, tests of code with no production caller, and near-duplicates that differ only in inputs. Look too for tests that cannot fail on the check they name, because their fixture never reaches the case or an earlier guard returns first. A mutant that survives on the exact check a test names is the tell.

## Decide

Judge removals together against the suite that will remain. For each removal, record which retained tests preserve its protection, or why the behavior no longer needs protection. Two equivalent tests may each have no unique catch; retain at least one while their contract still needs protection. Reconcile these dependencies across chunks before applying changes.

- **Keep** a test that uniquely catches a credible failure among the retained tests, and name that failure. Keep an overlapping test only when you can name the failure it pinpoints much faster or more clearly than the others that catch it, for example a focused test that names the rule it checks when the others are broad tests whose failure only shows that output changed. When a focused test and a broader one assert the same contract, let the focused test own it, and judge the broader test on what only it exercises, such as the wiring between parts.
- **Remove** a test that catches nothing unique and has no named reason to stay, or that restates the implementation.
- **Merge** tests that exercise one contract with different inputs, for example into a table-driven test; a table pays off when its rows share setup and assertions. Trimming the rows of an existing table rarely saves maintenance.
- **Rewrite** a test that guards a real contract through implementation details, under a misleading name, with a fixture that cannot fail on its contract, or at a cost a smaller test would avoid. When a test leaks state into later tests, such as a replaced global or a reloaded module, rewrite the leaking test, not the one that fails after it.
- **Unresolved** only when the evidence could not be gathered in this run, or when the verdict waits on a decision only the code's owner can make. Record what would settle it, so the next run can.

Before removing a test that uniquely catches something, add or strengthen the replacement protection first, following write-tests.

When the code a test covers has no production caller, decide with that code rather than the test. This includes an option no caller passes. Delete both, unless a plan records a future use for the code; then keep both and note that plan. Removing only the tests leaves untested dead code. A branch for input no current caller produces, such as one that upstream validation makes unreachable, can still be defense worth keeping where a wrong result would be silent and costly. List such branches for the owner to decide, and keep one test for each branch kept. After deleting code, check whether it was the last caller of anything else.

## Apply and verify

When cleanup is requested, make the changes on a focused branch, and update anything that names a removed test or deleted code, such as docs and agent guidance, in the same change. When the cleanup also deletes code, apply and verify the test changes first with production source unchanged, so the rerun can match mutants by location; delete the code afterward. Probe each rewrite: it must catch the fault its name promises and keep what the removals it preserves relied on, since a joint removal check does not see what a rewrite drops. Afterward, rerun the suite and the same mutation run or fault probes. Every fault caught before must still be caught, apart from ones you deliberately accepted and explained. This establishes preservation for the exercised faults, not all possible regressions. A green suite alone does not show that protection survived. Run the repository's required gates.

Report verdict counts, tests and lines removed, suite time before and after, mutation or probe results before and after, the keeps that rest on reasoning rather than a caught fault, the unresolved entries, and the scope not yet swept. For a review-only request, report proposed changes and available evidence without implying that changes or post-change checks ran.
