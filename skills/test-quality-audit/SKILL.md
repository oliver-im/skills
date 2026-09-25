---
name: test-quality-audit
description: Audit existing tests for weak assertions, missing protection, and costly redundancy. Use for test-quality reviews, test-bloat investigations, and evaluating proposed test cleanup; ordinary feature implementation does not require a suite audit.
---

# Test Quality Audit

Improve confidence in required behavior relative to test maintenance cost.
Strengthening, consolidating, removing, and keeping tests are all valid outcomes.
Do not optimize for test count, coverage percentage, or deleted lines.

## Understand the contracts

Use the requested scope. If it is broad, start with a coherent area and make
partial coverage explicit. Read applicable repository guidance and testing docs,
then inspect the relevant tests, production paths, fixtures, history, and
known-issue records.
Identify critical behaviors, supported interfaces, and reasons for unusual tests.
Verify these explanations against the code; documentation is context, not an
automatic exemption.

Adapt to existing repository conventions without requiring a new configuration
file or repository-specific skill. When documentation changes are in scope,
record newly established, non-obvious contracts in the existing repository docs.

An audit normally produces findings. When the user also requests remediation,
carry the supported changes through validation within that scope.

## Investigate the protection

For each candidate, establish the behavior it protects, a credible failure it
detects, and where the expected result comes from. Requirements, independently
checked examples, and reviewed fixtures can supply expectations. Writing a test
before or after implementation does not establish its value.

Look for plausible wrong behavior that would still pass. Useful leads include
expectations calculated by the code under test, mocks supplying the asserted
behavior, comparisons that discard meaningful relationships, omitted
boundaries, and limits that one component produces and another enforces.
Failure-path tests may inject their fault before the side effects they claim to
clean up. Also examine duplicated assertions and costly test support. These
are investigation prompts, not automatic deletion rules.

Constants, serialization, call ordering, and fixture checks can enforce real
contracts. Overlapping tests can justify their cost through faster feedback,
better diagnosis, or distinct failure modes. Choose the smallest scope that
faithfully exercises the failure; no test layer is universally preferred.

Use focused execution or a deliberate fault when it resolves uncertainty.
Establish a baseline first. Inject faults in an isolated copy or worktree,
rebuild what the tests execute, and restore each fault before the next probe.
Confirm failures occur for the intended reason. Setup or compilation failures
and behavior-preserving mutations do not demonstrate regression protection.
Distinguish injected faults from defects observed in the original code; selected
probes do not establish a suite-wide effectiveness or safe-deletion rate.

Before recommending removal or consolidation, explain what protection remains,
or why the behavior no longer needs protection, and why the maintenance saving
is worthwhile. Passing tests after deletion are insufficient evidence. Keep
uncertain candidates pending further evidence. Diagnose baseline failures
rather than deleting their tests to obtain a passing run.

## Recommend and verify

Report actionable findings with test/source locations, the affected contract,
evidence, and a proposed action. Separate demonstrated gaps, existing defects,
and unverified concerns. Mention valuable tests retained when they could easily
be mistaken for redundancy. State the scope actually reviewed, checks run, and
limitations; a no-change result is valid.

When implementing changes, establish replacement protection before removing old
assertions. For a regression check, demonstrate failure on the buggy behavior
and success on the repair when practical, under the settings where the check
runs, such as CI's time zone or platform. Run focused checks and required
repository gates. Review changes to expected outputs deliberately, and preserve
existing user work throughout.
