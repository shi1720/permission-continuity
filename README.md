# Permission continuity in Indo-Pacific infrastructure governance

Research by Shivam Gupta. This artifact supports **Continuity by Permission:
Small-State Agency across Cable Repair, Satellite Licensing and Power Trade**.

## Scope

The empirical component is a structured documentary comparison, not a causal
impact evaluation or a census of national resilience. The code verifies exact
interval consequences under declared assumptions. No synthetic result is an
observed outage or a probability of future failure. No new interval algorithm
is claimed. Licence terms do not establish technical readiness, provider
commitment, emergency priority or applicable scope.

## Reproduce

Python 3.10+; analysis and tests require only the standard library.

```
python3 -m unittest discover -s tests -v
python3 -m src.run_analysis
python3 -m src.check_portfolio data/example_portfolio.json
```

PDF generation requires ReportLab 4.4.9 (see requirements-artifacts.txt):

```
python3 -m src.make_figures
python3 -m src.build_pdf
```

`data/evidence.csv` records sources, locators, observations, unknowns and the
limits of inference. `data/sources.json` provides verified URLs and bibliographic
information. Access date: 14 October 2026. Original third-party publications are
linked, not republished. PDF page locators use printed page labels unless noted.

## Boundary conventions

Window [a,b) contains integer days a through b-1. A disruption starting at t
with duration R needs permission on every day t through t+R-1. Candidate starts
are [0,365); recovery may extend beyond day 365. A 365-day window therefore
covers 365-R+1 start days, not 365-R. The 180-day and 365-day stress terms are
model inputs and are not calendar conversions of the reported licence terms.

`switching=False` requires one complete path throughout recovery. `True`
allows instantaneous compatible handoff with adequate capacity and permissions;
it supplies an optimistic bound. Required authorizations are intersected before
paths are combined. Unreported permission terms remain unknown in the evidence;
they are never assigned model windows.

The tests compare the interval implementation to a separately written daily
oracle over 27,000 cases. These are implementation checks, not 27,000 empirical
observations. The stress grid contains 1,800 deterministic configurations.
The JSON CLI also requires explicit evidence-review fields and withholds a
coverage result for unknown validity, scope, readiness or handoff. It does not
validate the truth of a user's review fields. Commercial positioning and existing
vendor capabilities are documented in `paper/commercial_assessment.txt`.

## Status

Workshop manuscript and reproducibility artifact. Not peer reviewed. Publication
or patentability is not established. The literature search is documented in
`paper/research_notes.md`; it supports a scoped contribution, not an exhaustive
priority claim.
