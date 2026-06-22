---
name: Observability Designer
description: Use when adding observability to a new service, fixing noisy alerting, or designing dashboards across metrics/logs/traces before scaling production load.
tags: [observability, dashboards, grafana, alerting, alert-noise, golden-signals, metrics, logs, traces, sli]
source: alirezarezvani/claude-skills
derived_from: observability-designer
---

# Observability Designer

Production observability across the three pillars (metrics, logs, traces): dashboards, alert-noise reduction, and quick SLO scaffolds. NOTE: for full SLO/SLI design with error-budget math and multi-window burn-rate alerts, route to a dedicated SLO skill — this skill's lane is dashboards and alert-noise.

## Flow
1. **Dashboard spec** (Grafana JSON + docs) per service: type, name, criticality, role (SRE/dev/exec). Import into Grafana and confirm every golden-signal panel renders with live data.
2. **Alert analysis**: analyze an existing alert config for noise, duplicates, coverage gaps first; emit the optimized config only after the report is reviewed.
3. **SLO scaffold**: quick SLI/SLO skeleton (hand off real error-budget work to the SLO skill).
4. **Verify**: track noise metrics for one on-call rotation; if actionable-alert ratio didn't improve, re-analyze the live config and iterate.

## Three pillars
- **Metrics**: Golden Signals (latency, traffic, errors, saturation); RED (rate/errors/duration) for request services; USE (utilization/saturation/errors) for resources; plus business + infra metrics.
- **Logs**: structured JSON, centralized aggregation, correct levels, correlation IDs for distributed tracing, sampling for high-throughput.
- **Traces**: distributed tracing, meaningful span boundaries, head/tail/adaptive sampling, service maps, trace-driven root-cause.

## Dashboard design
Hierarchy: Overview → Service → Component → Instance. 80% operational / 20% exploratory. Max 7±2 panels per screen. Role-based personas. Time series for trends, heatmaps for distributions, gauges for status. Red/amber/green semantics. Reference lines for SLO targets + capacity thresholds. Default windows: 4h incidents, 7d trends.

## Alert design (fatigue prevention)
Severity: Critical (service down / high burn rate), Warning (approaching thresholds), Info (deploys, capacity). Every alert must have a clear response action. Prefer high precision (few false positives) over high recall. Use hysteresis (different fire vs resolve thresholds), dependent-alert suppression during outages, and grouping of related alerts. Test rules against historical data.

## Golden signals detail
- Latency: P50/P95/P99 request, queue, network, DB.
- Traffic: RPS with burst detection, bandwidth, sessions, feature usage.
- Errors: 4xx/5xx rates, error budget consumption, error distribution, silent failures.
- Saturation: CPU/mem/disk/net, queue depth, connection pools, rate-limit exhaustion.

## Runbooks per alert
Alert context (what/why fired), impact assessment (user-facing vs internal), ordered investigation steps with time estimates, resolution + escalation, post-incident follow-ups.

## Cost optimization
Tiered metric retention, intelligent log + trace sampling, cold storage archival, cardinality management (detect + mitigate high-cardinality metrics), efficient queries.

## Integrations
Prometheus + Grafana, Elasticsearch/Kibana, Jaeger/Zipkin, PagerDuty/VictorOps, Slack/Teams, JIRA/ServiceNow. CI/CD: pipeline monitoring, deployment correlation, performance-regression checks.
