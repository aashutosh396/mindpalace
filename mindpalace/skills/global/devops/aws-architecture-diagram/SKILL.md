---
name: aws-architecture-diagram
description: "Use when the user asks to create, generate, draw, or build an AWS architecture diagram, cloud infrastructure diagram, or system diagram with AWS services (Lambda, DynamoDB, S3, API Gateway, ECS, VPC, etc.) — produces editable .drawio files with official AWS icons, exportable to PNG/SVG/PDF."
version: 1.0.0
license: MIT
tags: [aws, architecture, diagram, drawio, cloud, infrastructure, devops, mxgraph, png-export, system-design]
source: https://github.com/vidanov/aws-architecture-diagram-skill
derived_from: awesomeclaude
platforms: [macos]
prerequisites:
  commands: [drawio]
---

# AWS Architecture Diagram

Generate AWS architecture diagrams as native `.drawio` files using the official AWS Architecture Icons (draw.io's built-in `mxgraph.aws4` stencil library). Optionally export to PNG/SVG/PDF with embedded XML so exports stay editable.

## When to use
User wants an AWS / cloud architecture diagram, system diagram, or infra diagram — especially mentioning AWS services (Lambda, DynamoDB, S3, API Gateway, ECS, EC2, VPC, SNS/SQS, CloudFront, etc.), or asking for a `.drawio` file.

## Workflow
1. Generate draw.io XML in `mxGraphModel` format (rules below).
2. Write it to a `.drawio` file (use the Write tool).
3. If user asked for png/svg/pdf, export via the draw.io CLI (Export section).
4. Open the result (`open` on macOS) or print its path.
5. (Recommended) Export to PNG, eyeball for broken/empty icons + overlapping edges, fix XML, re-export. Raw XML hides rendering bugs.

## Audience mode
Decide first; ask if unclear ("Technical audience or executive/non-technical?").
- Technical: service names, protocol labels (HTTPS/gRPC), CIDR blocks, instance types.
- Non-technical: action labels ("Store Data", "Send Notification"), numbered flow with circled numbers (① ② ③ white for flow A; ❶ ❷ ❸ black for flow B), implementation details hidden.

## Layout rules
- Left-to-right data/request flow. UI/Frontend on LEFT, data sources/external systems on RIGHT.
- Horizontal lanes for parallel paths; secondary services (monitoring, DLQ) BELOW main flow with 280px+ gap.
- Spacing: ≥220px horizontal between icons, ≥250px vertical between lanes.
- Canvas `pageWidth="2400" pageHeight="1400"`, viewport `dx="2800" dy="1600"`.
- Title block top-left, inside the background rect: `text;html=1;align=left;verticalAlign=top;fontSize=14;spacing=8;` with value `<b>Title</b><br>Author | Date | Version`.

## Icon style
- Icons from `mxgraph.aws4` (official AWS icons). Main services 78x78px, secondary 65x65px.
- All icons: `sketch=0`. Service-level icons: `strokeColor=#ffffff`. Resource-level icons: `strokeColor=none`.
- Label font 12px. Group/boundary boxes: `fillColor=none` (no colored backgrounds).

### resourceIcon (78x78 colored square) — style template
`sketch=0;points=[...];outlineConnect=0;fontColor=#232F3E;fillColor=<COLOR>;strokeColor=#ffffff;dashed=0;verticalLabelPosition=bottom;verticalAlign=top;align=center;html=1;fontSize=12;aspect=fixed;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<SERVICE>`

Common resIcon / fillColor: Lambda `lambda`/`#ED7100`, API Gateway `api_gateway`/`#E7157B`, EventBridge `eventbridge`/`#E7157B`, SNS `sns`/`#E7157B`, SES `simple_email_service`/`#DD344C`, Step Functions `step_functions`/`#E7157B`, DynamoDB `dynamodb`/`#C925D1`, RDS `rds`/`#C925D1`, S3 `s3`/`#7AA116`, CloudFront `cloudfront`/`#8C4FFF`, Route 53 `route_53`/`#8C4FFF`, ECS `ecs`/`#ED7100`, EC2 `ec2`/`#ED7100`.

### productIcon (70x100, header bar) — e.g. SQS `sqs`
`...;shape=mxgraph.aws4.productIcon;prIcon=mxgraph.aws4.<SERVICE>`

### Standalone shapes (no resIcon): Client `mxgraph.aws4.client`, Server `traditional_server`, Firewall `generic_firewall`, ALB `application_load_balancer`, NLB `network_load_balancer`, VPC Endpoint `endpoints`.

### Group boundaries (set `container=1;dropTarget=1;`): AWS Cloud `group_aws_cloud_alt`, Account `group_account`, On-premise `group_on_premise`, VPC `group_vpc2`, Subnet `group_security_group`.

## Edges — critical for clean diagrams
Base style: `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeWidth=2;exitX=1;exitY=0.5;...;entryX=0;entryY=0.5;...`
- Labels SHORT (1-2 words); add `labelBackgroundColor=#F5F5F5;fontSize=11;`. Omit `value` for unlabeled edges. Skip obvious labels (Lambda→DynamoDB).
- For services above/below main flow use explicit exits: exit bottom `exitX=0.5;exitY=1`, enter top `entryX=0.5;entryY=0` — prevents routing through other icons.
- Types: solid = primary flow; `dashed=1` = optional/async; `dashed=1;strokeColor=#DD344C` = error path.
- Every edge MUST have both `source` and `target` referencing valid cell IDs (no floating edges — this fixes the "green cross" problem) and `<mxGeometry relative="1" as="geometry" />` child.
- Cross-container edges (source/target in different containers): set the edge's `parent="1"`.

## Container nesting
Child cells inside a boundary use `parent="<boundary-cell-id>"` (not `"1"`); their geometry is relative to the parent container. This keeps children moving with the boundary.

## Icon name gotchas (renamed services keep legacy stencil names)
OpenSearch → `elasticsearch_service`; EventBridge → `eventbridge` (was CloudWatch Events); MSK → `managed_streaming_for_kafka` (NOT `msk`); IAM Identity Center → `single_sign_on` (NOT `iam_identity_center`); VPC Peering → `peering` (NOT `vpc_peering`). Wrong names render as blank squares.

Fallback for unmapped services: use `resIcon=mxgraph.aws4.general_AWScloud` with the service name as label. Never render a service as a plain colored rectangle.

## Broken icons — DO NOT USE
`dynamodb_table`, `dynamodb_stream`, `general_saml_token`, `endpoint`, `kinesis_data_streams` render empty/black. Use `dynamodb` with descriptive labels, `traditional_server` for external systems, `client` for browsers.

## Reference files (canonical stencil names per category)
The source repo ships verified icon-name references — fetch when you need a service not listed above:
`https://raw.githubusercontent.com/vidanov/aws-architecture-diagram-skill/main/references/aws-icons-<category>.md`
Categories: `common`, `compute`, `database`, `storage`, `networking`, `security`, `integration`, `analytics-ml`, `iot-migration-devtools`. Canonical draw.io source: `src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js` in jgraph/drawio.

## XML well-formedness (critical)
- NEVER include XML comments (`<!-- -->`) — they cause parse errors.
- Escape `&amp; &lt; &gt; &quot;`. Unique `id` per mxCell.
- Root needs `id="0"` and `id="1"` (default layer, parent="0").
- PNG export background: first/bottom element = `#F5F5F5` rect covering the full canvas (prevents black background on export).

## Export (draw.io Desktop CLI)
CLI path: macOS `/Applications/draw.io.app/Contents/MacOS/draw.io`; Linux `drawio`; Windows `"C:\Program Files\draw.io\draw.io.exe"`.
```bash
<CLI> -x -f <png|svg|pdf> -e -b 10 -o <output> <input.drawio>
```
`-x` export, `-f` format, `-e` embed XML (output `name.drawio.png` stays re-editable), `-b 10` border.

## Multi-page diagrams
For complex architectures use multiple `<diagram>` pages in one `<mxfile>`: page 1 high-level overview (service-level icons), page 2+ detail (resource-level icons, subnet layouts).

## Companion guide
After the .drawio, optionally emit a markdown guide (same name, `.md`): title, numbered flow description, service list + purpose, key design decisions.

## Validation checklist before finishing
1. Every `resIcon=` exists in the references. 2. Service icons `strokeColor=#ffffff`, resource icons `strokeColor=none`. 3. No XML comments. 4. Unique cell IDs. 5. Every edge has the `mxGeometry relative="1"` child. 6. No guessed stencil names. 7. Every edge has valid `source`+`target`. 8. Boundaries have `container=1;dropTarget=1;`. 9. Children use `parent="<boundary-id>"`.
