---
name: monitoring-expert
description: "Use when setting up application monitoring, adding observability, debugging production issues with logs/metrics/traces, running load tests (k6/Artillery), profiling CPU/memory, or planning capacity. Covers Prometheus/Grafana, structured logging, OpenTelemetry tracing, and alerting. Triggers: monitoring, observability, logging, metrics, tracing, alerting, Prometheus, Grafana, APM, load testing, profiling, capacity planning."
version: 1.0.0
license: MIT
tags: [observability, monitoring, prometheus, grafana, opentelemetry, logging, alerting, load-testing]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/monitoring-expert
derived_from: awesomeclaude
---

# Monitoring Expert

Observability and performance: monitoring, alerting, tracing, and load testing.

## When to use

Setting up monitoring/observability, debugging prod via logs/metrics/traces, load testing, profiling bottlenecks, capacity forecasting.

## Core workflow

1. **Assess** — what to monitor (SLIs, critical paths, business metrics).
2. **Instrument** — add logging, metrics, traces.
3. **Collect** — configure aggregation/storage (Prometheus scrape, log shipper, OTLP); verify data arrives.
4. **Visualize** — dashboards via RED (Rate/Errors/Duration) or USE (Utilization/Saturation/Errors).
5. **Alert** — threshold + anomaly alerts on critical paths; validate no false-positive flood.

## Examples

```js
// Structured logging (Pino) — fields + correlation ID, never string interpolation
logger.info({ requestId: req.id, userId: req.user.id, durationMs: elapsed }, 'order.created');
```
```js
// Prometheus metrics (prom-client)
const httpDuration = new Histogram({ name: 'http_request_duration_seconds',
  help: 'HTTP latency', labelNames: ['method','route'], buckets: [0.05,0.1,0.3,0.5,1,2,5] });
app.use((req,res,next)=>{ const end=httpDuration.startTimer({method:req.method,route:req.path});
  res.on('finish',()=>{ httpRequests.inc({method:req.method,route:req.path,status:res.statusCode}); end(); }); next(); });
app.get('/metrics', async (_,res)=>{ res.set('Content-Type',register.contentType); res.end(await register.metrics()); });
```
```yaml
# Prometheus alert: error rate > 5%
- alert: HighErrorRate
  expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
  for: 2m
  labels: { severity: critical }
  annotations: { summary: "Error rate above 5% on {{ $labels.route }}" }
```
```js
// k6 load test with thresholds
export const options = {
  stages: [{duration:'1m',target:50},{duration:'5m',target:50},{duration:'1m',target:0}],
  thresholds: { http_req_duration:['p(95)<500'], http_req_failed:['rate<0.01'] } };
export default function(){ const res=http.get('https://api.example.com/orders');
  check(res,{'status is 200':(r)=>r.status===200}); sleep(1); }
```

## Constraints

MUST: structured (JSON) logging; request IDs for correlation; alert on critical paths; monitor business metrics (not only technical); use correct metric types (counter/gauge/histogram); health-check endpoints.
MUST NOT: log secrets/PII; alert on every error (fatigue); string interpolation in logs; skip correlation IDs in distributed systems.
