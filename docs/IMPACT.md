# Madad — Impact & Deployment Plan

> Who uses it on Day 1. What changes measurably in six months. Who we work
> with. What we won't do.

## 1. First user, first week

**Cohort:** 25 Deaf students, ages 14–22, at the **Deaf Reach campus in
Rashidabad, Sindh** (the largest Deaf school network in Pakistan). They each
receive a side-loaded APK on their personal phone, with a 30-minute
orientation. One interpreter from the school is present for the first
session.

**Success criterion for week 1:** ≥ 60 % of students voluntarily open the
app at least three times outside the orientation. We track this via a
locally-stored, anonymous counter that the user can disable.

## 2. Partners we have talked to (or will, before launch)

| Organisation | Role | Status |
|---|---|---|
| [Family Educational Services Foundation / Deaf Reach](https://www.fesf.org.pk/) | Pilot deployment, 25 students | Outreach letter drafted in `partners/deaf_reach.md` |
| National Association of the Deaf, Pakistan | Policy endorsement, PSL accuracy review | Outreach letter drafted in `partners/nad.md` |
| ConnectHear (local PSL interpretation startup) | Vocabulary review, labelling help | Public contact form submitted |
| Pakistan Association of the Deaf PSL dictionary project | Source for ground-truth glosses | CC-BY citation, see `docs/DATA.md` |

> All four outreach letters ship with the submission. None of the above are
> confirmed sponsors — we are transparent about that.

## 3. Six-month plan

| Month | Milestone | Measurable outcome |
|---|---|---|
| 1 | v0.1 pilot launch, Deaf Reach | 25 active users |
| 2 | Add **medical-visit mode** — curated hospital glossary in-prompt | Tested in 5 LRH Peshawar OPD visits |
| 3 | Expand PSL-100 → PSL-500 via community recording sessions | Benchmark v2 published |
| 4 | Sindhi + Pashto output for bilingual households | 3-language A/B test with Karachi pilot |
| 5 | Classroom-mode: live-caption a teacher's Urdu lecture into signs | Deployed to 2 Deaf Reach classrooms |
| 6 | Public v1.0 APK on Google Play | Independent evaluation report published |

## 4. What we explicitly will not do

- **We do not claim to replace human interpreters.** Madad's current
  accuracy means it works for simple exchanges — greetings, directions,
  symptom reporting. Legal, mental-health and complex medical consultations
  still require a trained human.
- **We do not collect user data.** Everything is on-device. No analytics,
  no telemetry. This is non-negotiable — Deaf users in Pakistan already
  have reasons to distrust institutions tracking them.
- **We do not gate the model behind an account.** APK, not subscription.

## 5. Sustainability

Madad is Apache 2.0. Sustainability plan:

- Low-cost to run (zero server): no hosting budget needed.
- Model updates quarterly, funded by (a) this competition's prize if won,
  (b) Google DeepMind / Kaggle follow-on grants if available, (c) in-kind
  volunteer time from the Pakistani Deaf community.
- A maintainer org ("Madad Collective") formed at v1.0 to own the model
  card, dataset, and accessibility audits.

## 6. Risks we've named

| Risk | Mitigation |
|---|---|
| Model gets a medical sign wrong, patient is harmed | Confidence threshold 0.7 for medical-mode; below it we explicitly show *"I'm not sure — please find an interpreter"* |
| Regional dialect variation inside PSL | PSL-500 benchmark will include Karachi, Lahore, Peshawar signers separately |
| Deaf users feel the technology is patronising / imposed | Co-design with Deaf Reach students; every PSL-100 clip is signed by a Deaf signer, not a hearing interpreter |
| Model size too big for low-end phones | E2B variant (~1.0 GB int4) already tested; falls back gracefully on < 3 GB RAM devices |

---

*This is not a one-shot hackathon demo. It's the first version of a product
we intend to run.*
