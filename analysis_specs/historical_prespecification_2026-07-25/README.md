# Pre-specification of 2026-07-25 (historical record)

| file | content |
|---|---|
| `ANALYSIS_PLAN_as_committed_2026-07-25.md` | the analysis plan as committed on 2026-07-25 (UTC 01:14:41), with two workstation directory names redacted (see below) |
| `PRESPEC_STAMP.txt` | the stamped bundle: commit hash, tree hash, UTC commit time and the sha256 of the committed plan, `87a2da6275033531449a8d668865f2d02916eee5f11cdd96cee2703c9cfea2d7` |
| `PRESPEC_STAMP.txt.ots` | the OpenTimestamps proof of `PRESPEC_STAMP.txt`, upgraded to a Bitcoin block attestation |

Verification of the timestamp (requires the `opentimestamps-client` Python package):

```bash
ots verify PRESPEC_STAMP.txt.ots      # PRESPEC_STAMP.txt must be alongside
```

**What the timestamp proof authenticates.** The timestamp proof corresponds to the original private unredacted
record. The publicly released copy of the plan has been redacted for privacy and therefore does not have the same
cryptographic hash. The proof must not be interpreted as authenticating the exact bytes of the public redacted
copy: it authenticates `PRESPEC_STAMP.txt` (reproduced unchanged), whose plan hash `87a2da62…` is that of the
unredacted original held in the private record.

Redaction. The committed plan contained, in its "Paths relocated" note, two home-folder directory names of the
development workstation and the name of a folder-synchronisation service. This public copy replaces those three
strings with `~/<former-workspace>/`, `~/<former-archive>/` and "folder synchronisation"
(`docs/CODE_MODIFICATIONS.md` lists the exact edit); every other character is identical to the committed file.
The proof file and the stamp file are byte-identical to the originals.

Status. This plan specified the earlier cross-fitted design with permutation-based inference. A reproducibility
audit later established that the statistic that design called AUTOC was non-standard, and the analysis reported in
the manuscript follows the amendments under `amendments/` instead, which were protocol-locked after the audit and
before execution and are not treated as a prospectively pre-registered confirmatory analysis. The plan is retained
as the historical record referred to in the manuscript.
