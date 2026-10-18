# Incident at 03:00

Pager lights the rack. Traffic still flows. You have **one minute** and **one decision chain**.

No JavaScript — each choice is a link. Every path ends in something real.

---

## 03:00 — alert fires

> **SYMPTOM:** Deploy pipeline green, but error rate climbing on the edge.  
> **SCOPE:** Hybrid — workload spans **data center Kubernetes** and **Cloud Run**.  
> **COMMS:** On-call lead (you). No heroics — reduce blast radius first.

What do you do **first**?

- [A — Roll back the last release](#a--rollback)
- [B — Scale out before you diagnose](#b--scale)
- [C — Isolate the failing slice](#c--isolate)
- [D — Pull logs and traces](#d--observe)

---

## A — Rollback

> GitOps means rollback is a **revert**, not a prayer. You check what changed in git, not what someone ran by hand.

- [multicloud-karmada-gitops](https://github.com/Rahul-ramakrishnan06/multicloud-karmada-gitops) — how desired state should have moved.
- [Rules of engagement](#rules) — GitOps is step 03.

**Next:** [Did you verify identity before the deploy?](#identity-check) · [Back to 03:00](#0300--alert-fires)

---

## B — Scale

> Scaling without isolation can amplify a bad build. You pause and ask: is this load or corruption?

- [gcp-cloudrun-iac-rest-api](https://github.com/Rahul-ramakrishnan06/gcp-cloudrun-iac-rest-api) — serverless scaling knobs live in IaC.
- [Mission log on profile](README.md#mission-log) — Soneium uptime came from **controlled** change, not blind scale.

**Next:** [Isolate instead](#c--isolate) · [Back to 03:00](#0300--alert-fires)

---

## C — Isolate

> Cut the blast radius: single cluster, single region, single deployment. Traffic shift only when you know the slice is clean.

- [supabase-selfhosted-k8s](https://github.com/Rahul-ramakrishnan06/supabase-selfhosted-k8s) — data plane boundaries on K8s.
- [multicloud-karmada-setup](https://github.com/Rahul-ramakrishnan06/multicloud-karmada-setup) — federation & placement.

**Next:** [Observe](#d--observe) · [Back to 03:00](#0300--alert-fires)

---

## D — Observe

> Metrics, logs, traces — in that order if the SLO is on fire. You need **one** golden signal before you touch prod.

- [DevOps_Projects](https://github.com/Rahul-ramakrishnan06/DevOps_Projects) — dashboards & automation experiments.
- Runbook tab **05 SLO** on the [profile README](README.md).

**Next:** [Rollback if change correlates](#a--rollback) · [Back to 03:00](#0300--alert-fires)

---

## Identity check

> A “green” pipeline with **long-lived keys** is a green lie. Federation or short-lived tokens — or you do not ship.

- iCliniq field note: **WIF** across **15+** pipelines (see [mission log](README.md#mission-log)).
- Runbook tab **01 WIF** on the [profile README](README.md).

- [Close incident — send intel](mailto:rahulkarthi06@gmail.com)
- [Back to 03:00](#0300--alert-fires)

---

## Rules

1. Mechanism — network, identity, state.  
2. Least privilege — no standing credentials in CI.  
3. GitOps — desired state in version control.  
4. Supply chain — scan and harden in the build.  
5. Observability — uptime, cost, recovery time.  
6. Outcomes — blast radius over tool fashion.

---

[← Back to perimeter map](https://github.com/Rahul-ramakrishnan06)
