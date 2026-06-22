---
name: Claude API / Anthropic SDK Reference
description: Use BEFORE writing any Claude/Anthropic LLM code (or answering pricing/model/limits/caching questions) — model IDs, params, streaming, tool use, MCP, agents, caching, token counting, migration. Skip only if another provider is named.
tags: [claude, anthropic, sdk, llm, tool-use, streaming, prompt-caching, managed-agents, mcp, model-migration, token-counting]
source: anthropics/skills
derived_from: skills/claude-api
---

# Building LLM-Powered Applications with Claude

Read this before writing Claude/Anthropic code. Skip only when another provider (OpenAI/GPT/Gemini/Llama/Mistral/Cohere/Ollama) is named or detected — never edit a non-Anthropic file with Anthropic SDK calls.

## Before you start
Scan the target file/project for non-Anthropic markers (`import openai`, `gpt-4`, `langchain_openai`, etc.). If found, stop and ask. Output must call Claude via the official Anthropic SDK (`anthropic`, `@anthropic-ai/sdk`, etc.) — or raw HTTP only when explicitly asked. Never mix the two; never use OpenAI-compatible shims. **Never guess SDK usage** — names/signatures/imports must come from explicit docs; WebFetch the SDK repo if unsure.

## Defaults
- **Model: `claude-opus-4-8`** unless the user explicitly names another. Never downgrade for cost (user's call).
- **Adaptive thinking** for anything non-trivial: `thinking: {type: "adaptive"}`.
- **Streaming** for long input/output or high max_tokens (prevents timeouts); use `.get_final_message()` / `.finalMessage()`.

## Current models (cached 2026-06-04)
| Model | ID | Context | In/Out $1M |
|---|---|---|---|
| Claude Fable 5 | `claude-fable-5` | 1M | 10/50 |
| Claude Opus 4.8 | `claude-opus-4-8` | 1M | 5/25 |
| Claude Opus 4.7/4.6 | `claude-opus-4-7`/`-6` | 1M | 5/25 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 1M | 3/15 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | 1/5 |

Use exact IDs — never append date suffixes. Models newer than your training cutoff are real. For live capability/context lookup use the Models API (`client.models.retrieve/list`).

## Thinking & effort
- **Fable 5 / Opus 4.8 / 4.7:** adaptive only. `{type:"enabled", budget_tokens:N}` → 400 (budget_tokens removed, along with temperature/top_p/top_k). Fable 5 also rejects explicit `{type:"disabled"}` — omit the param. Prefill removed across the 4.6+ family.
- **Opus 4.6 / Sonnet 4.6:** adaptive recommended; `budget_tokens` deprecated (transitional escape hatch only).
- **Effort:** `output_config: {effort: "low"|"medium"|"high"|"xhigh"|"max"}` (default high). `xhigh` is best for coding/agentic on Fable5/4.7/4.8. Older models only: `{type:"enabled", budget_tokens:N}` (≥1024, < max_tokens).
- **Thinking display:** `"omitted"` is default on Fable5/4.8/4.7 (empty thinking text); set `display:"summarized"` to stream reasoning. Echo thinking blocks back unchanged on the same model; other models silently ignore them but still bill — strip when switching.

## Choosing a surface
Single call (classify/summarize/extract/Q&A) → Claude API. Code-orchestrated multi-step with your tools → Claude API + tool use (you control the loop). Server-managed stateful agent with hosted workspace/containers → **Managed Agents** (create agent once, reference by ID; `model`/`system`/`tools` live on the agent, not the session). Start simple — only reach for agents when the task is genuinely open-ended.

## Key facts
- Everything goes through `POST /v1/messages`; tools + structured outputs are features of this one endpoint.
- **Structured outputs:** `output_config: {format: {...}}` (old `output_format` deprecated); prefer `client.messages.parse()`.
- **Prompt caching:** prefix match — any byte change invalidates everything after. Order: tools→system→messages. Stable content first, volatile after the last `cache_control`. Verify with `usage.cache_read_input_tokens` (zero = silent invalidator like `datetime.now()` in system prompt). Min cacheable ~1024 tokens; max 4 breakpoints.
- **Compaction (beta):** for >1M-context conversations, append `response.content` (not just text) back every turn — compaction blocks replace history.
- **Token counting:** use `messages.count_tokens`, never tiktoken. Fable 5 tokenizer ~30% more tokens — re-baseline.
- **Refusal stop reason (Fable 5):** HTTP 200, `stop_reason:"refusal"` — check `stop_reason` before reading `content`.
- **max_tokens defaults:** non-streaming ~16000, streaming ~64000; classification ~256. 128K output needs streaming.
- **Don't reimplement SDK helpers** (finalMessage, typed exceptions, SDK types) or define custom types for SDK objects.
- **Cloud:** Managed Agents + server-side tools work on first-party API + Claude Platform on AWS; NOT on Bedrock/Vertex/Foundry (use API + tool use there).

## Subcommands
`migrate` → read the model-migration guide; ask scope (which files) + target model before any edit. `managed-agents-onboard` → run the onboarding interview incl. pre-flight viability check.
