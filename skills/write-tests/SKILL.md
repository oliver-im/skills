---
name: write-tests
description: Write or strengthen tests only where they catch a credible failure, and skip tests that merely restate the implementation. Use whenever adding or changing tests, including during feature work and bug fixes, and when auditing existing code for missing protection. For removing or consolidating existing tests, use prune-tests.
---

# Write Tests

A test earns its place when it catches a credible failure that other tests miss, or catches it much sooner or more clearly, and its expected result does not come from the code under test. Write tests that meet this bar and skip the rest. Test count and coverage percentage are not goals.

## Start from failures

Identify the contracts the work establishes or touches: requirements, supported interfaces, documented guarantees, and past regressions. Read the repository's guidance, testing docs, and existing test conventions for this context. For each contract, list the plausible ways an implementation could get it wrong. Do this before implementing substantial behavior when you can; tests written after the code tend to copy what the code does rather than what it should do. A contract with no plausible failure needs no new test.

Check what already catches each failure before adding anything. Prefer strengthening an existing test, with a tighter assertion, a missing boundary, or another row in a table, over adding a new one. Choose the smallest scope that faithfully exercises the failure; no test layer is universally preferred.

## Write the check

Take expected results from requirements, hand-checked examples, or reviewed fixtures. An expectation computed by the code under test can change alongside a defect and keep passing. Output pasted into an unreviewed snapshot detects changes, but does not establish that the original output was correct. Review such output against the contract before treating it as an expectation.

Assert the contract rather than the route to it. Pin private helpers, intermediate data, call order, or exact output only when a caller or requirement depends on that exact form; constants, serialization, and call order sometimes do. Mock only at boundaries the code does not own. Reject checks where the mock supplies the behavior supposedly under test. Mock data can still support a useful assertion that production code selects, forwards, transforms, or preserves a dependency's result as required by a contract.

Skip tests for trivial changes, for wiring or accessors with no logic, and for failures an existing test already catches at similar speed and clarity.

## Show that it bites

When practical, show each new or strengthened check failing on the wrong behavior and passing on the right one. For a bug fix, fail on the original bug. Otherwise inject the fault in an isolated copy or worktree, rebuild what the tests execute, and restore it afterward. Confirm the failure happens for the intended reason; setup or compilation errors do not count. Check under the settings where the test runs, such as CI's time zone or platform. Run the repository's required gates.

## Auditing for gaps

When asked to find missing protection in existing code, work through contracts rather than tests; judging existing tests one by one is the job of prune-tests. Use the requested scope, start with a coherent area if it is broad, and make partial coverage explicit. Consult known-issue records so you do not re-report logged problems.

Establish a green baseline, then probe credible faults one at a time. Useful leads include expectations calculated by the code under test, mocks supplying the asserted behavior, comparisons that discard meaningful relationships, omitted boundaries, limits that one component produces and another enforces, and failure-path tests that inject their fault before the side effects they claim to clean up.

Report each gap with its contract, the fault that escaped, its consequence, and test and source locations. Distinguish injected faults from defects in the original code; a sample of probes does not measure suite-wide effectiveness. A no-change result is valid. When remediation is requested, close gaps as described above. List weak or redundant tests noticed along the way as candidates for prune-tests instead of leaving them unmentioned.
