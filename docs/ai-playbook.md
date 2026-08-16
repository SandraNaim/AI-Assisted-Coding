# My AI playbook

## When I reach for AI first

I use AI first for bounded, low-risk work: mapping an unfamiliar folder,
drafting a test checklist, reviewing a small diff, or suggesting edge cases.
During this project it helped me turn release requirements into checks, trace a
dependency incompatibility, and notice that the first Dockerfile ran as root.
It is also useful for repetitive scaffolding when the repository already shows
the intended pattern.

## When I do not reach for AI first

I start with the repository when the answer should already be there. I read the
business rule before asking how status transitions should behave, and I run a
command before asking AI whether it works. I slow down when context is missing,
the change affects security or data, or the goal is for me to learn the
mechanism. Product scope comes from the brief and existing application—not from
an AI feature suggestion.

## My non-negotiables

I never paste credentials, private keys, access tokens, customer data, or real
`.env` contents into AI. I do not hide failures, skip tests to get green CI, or
document an expected result as observed evidence. I own every submitted line:
if I cannot explain a change plainly, it is not ready to merge.

## My review rules

I read the entire diff and compare it with neighboring code, tests,
documentation, and scope. I check whether it changes behavior, adds an
unnecessary dependency, weakens an error, or solves an unrequested problem. I
run documented commands from the stated directory, preferably in a clean
environment. I grade findings against file evidence: Valid/Useful when proven
and relevant, False Positive/Wrong when contradicted, and Noise when unrelated
to the release. Plausible-sounding advice is still rejected if verification
shows it would break the project.

## Decision Card

| Situation | My decision rule |
| --- | --- |
| New feature | Check the brief and existing stories first; use AI only after scope is confirmed. |
| Code review | Give AI one real file or diff, then verify every comment against the repository. |
| Debugging | Reproduce and isolate the failure before asking AI for causes or fixes. |
| Infrastructure | Test commands in a clean environment and record exact output; never claim an unrun CI or Docker result. |
| Never-paste | Secrets, tokens, keys, customer data, private `.env` values, or confidential source I am not allowed to share. |
| One rule | AI output is a proposal; evidence and project scope make the decision. |

## What I am still figuring out

I am still deciding how much exact dependency pinning is best for a small
course project: it improves reproducibility now but creates an update burden.
I am also learning how teams should record AI contribution without turning the
record into paperwork. Finally, I do not treat API tests as proof of frontend
behavior; I still want a small manual browser check alongside automation.
