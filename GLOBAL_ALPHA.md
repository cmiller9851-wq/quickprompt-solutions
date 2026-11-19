# QuickPrompt Solutions — Global Alpha Charter

**Status:** Global Alpha · Branch: `global-alpha`
**Canonical repository:** `cmiller9851-wq/quickprompt-solutions`
**Owner:** QuickPrompt Solutions

## Purpose

This repository is the public coordination point for the QuickPrompt Solutions alpha. It provides a reproducible place to review protocol artifacts, automation, manifests, and implementation experiments.

Global Alpha means the project is organized for public technical review—not that every legal, financial, ownership, settlement, or network claim is independently verified or recognized by a court, regulator, bank, or blockchain network.

## Alpha operating principles

1. **Reproducibility:** Every material change is committed, reviewable, and accompanied by the commands needed to reproduce it.
2. **Traceability:** Protocol artifacts use stable filenames, explicit metadata, and linked commit history.
3. **Separation of concerns:** Technical observations, owner-authored assertions, and externally verified facts are labeled separately.
4. **Fail-closed automation:** CI must reject malformed JSON, invalid Python syntax, and broken repository metadata.
5. **No implied authority:** A hash, manifest, or repository record alone does not establish legal title, settlement, admissibility, or institutional recognition.
6. **Safe release discipline:** Default-branch releases require a passing validation run and human review of the change set.

## Alpha release gates

A change is ready for alpha review when:

- the repository validation workflow passes;
- JSON manifests parse successfully;
- Python sources compile successfully;
- the README and this charter describe the current scope accurately;
- new claims identify their source or are labeled as owner-authored assertions;
- no secret, private key, seed phrase, or unredacted personal financial data is committed.

## Scope of this branch

This branch establishes the project-level alpha baseline and automated hygiene checks. It does **not** deploy contracts, move assets, publish legal filings, make financial representations, or alter external network state.

## Verification commands

```bash
python3 -m json.tool path/to/file.json >/dev/null
python3 -m compileall -q .
```

The authoritative automated checks are defined in `.github/workflows/global-alpha.yml`.

## Change control

Use pull requests for changes intended for `main`. Keep commits focused, explain the operational impact, and include rollback notes for changes that affect workflows or deployment behavior.
