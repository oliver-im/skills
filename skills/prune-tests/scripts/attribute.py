#!/usr/bin/env python3
"""Attribute a StrykerJS JSON report's killed mutants to the tests that catch them.

With only a report, prints each test's catches and the mutants it catches alone.
With --remove, lists the mutants that would lose every catcher if the named tests
went. With --compare, lists mutants detected in the first report but not in a
rerun; it matches mutants by location, so the source under mutation must be
unchanged between the two runs.

Attribution needs a report produced with every failing test recorded:

  "coverageAnalysis": "perTest", "disableBail": true, "reporters": ["json"]

Also enable the checker for the language, such as "checkers": ["typescript"],
so mutants CI would reject count as CompileError rather than test catches.
"""

import argparse
import json
from collections import defaultdict

DETECTED = {"Killed", "Timeout"}


def load(path):
    with open(path) as f:
        return json.load(f)


def test_labels(report):
    return {
        test["id"]: f"{path} :: {test['name']}"
        for path, test_file in report.get("testFiles", {}).items()
        for test in test_file["tests"]
    }


def mutants(report):
    for path, source in report["files"].items():
        for mutant in source["mutants"]:
            yield path, mutant


def describe(path, mutant):
    line = mutant["location"]["start"]["line"]
    replacement = mutant.get("replacement", "").replace("\n", " ")[:60]
    return f"{path}:{line} {mutant['mutatorName']} -> {replacement!r}"


def key(path, mutant):
    start, end = mutant["location"]["start"], mutant["location"]["end"]
    return (path, start["line"], start["column"], end["line"], end["column"],
            mutant["mutatorName"], mutant.get("replacement"))


def status_counts(report):
    counts = defaultdict(int)
    for _, mutant in mutants(report):
        counts[mutant["status"]] += 1
    return dict(counts)


def require_attribution(parser, report):
    config = report.get("config", {})
    if config and (config.get("coverageAnalysis") != "perTest" or not config.get("disableBail")):
        parser.exit(2, "This report stops at the first failing test, so it cannot "
                       "attribute catches. Rerun with coverageAnalysis \"perTest\" "
                       "and disableBail true.\n")


def attribute(report, labels):
    catches = defaultdict(int)
    unique = defaultdict(list)
    for path, mutant in mutants(report):
        killers = (mutant.get("killedBy") or []) if mutant["status"] == "Killed" else []
        for test in killers:
            catches[test] += 1
        if len(killers) == 1:
            unique[killers[0]].append(describe(path, mutant))
    for test, label in sorted(labels.items(), key=lambda item: item[1]):
        print(f"{catches[test]:4d} caught {len(unique[test]):3d} alone | {label}")
        for line in unique[test]:
            print(f"          {line}")


def check_removal(parser, report, labels, removal_file):
    with open(removal_file) as f:
        names = {line.strip() for line in f if line.strip()}
    removed = {test for test, label in labels.items() if label in names}
    unmatched = names - {labels[test] for test in removed}
    if unmatched:
        parser.exit(2, "No test in the report matches:\n  " + "\n  ".join(sorted(unmatched)) + "\n")
    lost = [
        (path, mutant) for path, mutant in mutants(report)
        if mutant["status"] == "Killed" and set(mutant.get("killedBy") or []) <= removed
    ]
    print(f"Removing {len(removed)} tests leaves {len(lost)} killed mutants without a catcher.")
    for path, mutant in lost:
        catchers = ", ".join(labels[test] for test in mutant.get("killedBy") or [])
        print(f"  {describe(path, mutant)}\n      caught only by {catchers}")


def compare(before, after):
    after_status = {key(path, mutant): mutant["status"] for path, mutant in mutants(after)}
    detected = [(path, mutant) for path, mutant in mutants(before) if mutant["status"] in DETECTED]
    missing = [(p, m) for p, m in detected if key(p, m) not in after_status]
    lost = [(p, m) for p, m in detected if after_status.get(key(p, m), "Killed") not in DETECTED]
    print(f"Detected before: {len(detected)}; detected after: "
          f"{sum(status in DETECTED for status in after_status.values())}")
    if missing:
        print(f"{len(missing)} detected mutants are absent from the rerun; "
              "the source changed, so this comparison is unreliable.")
    print(f"No longer detected: {len(lost)}")
    for path, mutant in lost:
        print(f"  {describe(path, mutant)} is now {after_status[key(path, mutant)]}")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("report", help="StrykerJS JSON report")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--remove", metavar="FILE",
                      help="tests to remove, one 'path :: name' label per line as printed")
    mode.add_argument("--compare", metavar="AFTER",
                      help="report from a rerun after the test changes")
    args = parser.parse_args()
    report = load(args.report)
    print("Mutant statuses:", status_counts(report))
    if args.compare:
        compare(report, load(args.compare))
        return
    require_attribution(parser, report)
    labels = test_labels(report)
    if args.remove:
        check_removal(parser, report, labels, args.remove)
    else:
        attribute(report, labels)


if __name__ == "__main__":
    main()
