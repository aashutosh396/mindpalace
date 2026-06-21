---
name: websocket-engineer
description: "Use when building real-time communication systems with WebSockets or Socket.IO — bidirectional messaging, horizontal scaling with Redis, presence tracking, room management. Triggers: WebSocket, Socket.IO, real-time communication, bidirectional messaging, pub/sub, server push, live updates, chat systems, presence tracking."
version: 1.0.0
license: MIT
tags: [websocket, socketio, realtime, pubsub, redis, presence, rooms, chat]
source: https://github.com/jeffallan/claude-skills/tree/main/skills/websocket-engineer
derived_from: awesomeclaude
---

# WebSocket Engineer

Real-time bidirectional systems with WebSocket / Socket.IO.

## When to use

Bidirectional messaging; horizontal scaling across instances (Redis adapter); presence tracking; room/channel management; chat, live updates, server push.

## Core workflow

1. **Design protocol** — message/event schema, ack semantics, versioning.
2. **Connection lifecycle** — auth on handshake, heartbeat/ping-pong, reconnect strategy.
3. **Rooms/presence** — join/leave, presence sets, broadcast to rooms.
4. **Scale out** — Redis pub/sub adapter so events fan out across instances.
5. **Resilience** — backpressure, rate limiting, graceful shutdown, client reconnect with resume.

## Key practices

- Authenticate on handshake (token in connect), not just per-message.
- Heartbeat (ping/pong) to detect dead connections; clean up on disconnect.
- Rooms for targeted broadcast; presence via Redis sets with TTL.
- Redis adapter (Socket.IO) or external pub/sub for multi-instance fan-out + sticky sessions or session affinity.
- Backpressure: bound per-connection send queues; drop/throttle slow consumers.
- Client reconnect with exponential backoff + message resume (sequence IDs).

## Constraints

MUST: authenticate on connection handshake; heartbeat + dead-connection cleanup; Redis (or equivalent) adapter for horizontal scaling; rate limit inbound messages; graceful shutdown draining connections; idempotent message handling.
MUST NOT: trust unauthenticated sockets; broadcast to all when a room suffices; assume single instance (no shared pub/sub); ignore backpressure; leak rooms/presence on disconnect; unbounded reconnect storms (no backoff).

## Output

1. Connection + auth handler. 2. Room/presence logic. 3. Redis pub/sub scaling adapter. 4. Client reconnect strategy. 5. Brief note on scaling + backpressure.

## Knowledge

WebSocket, Socket.IO, ws, handshake auth, ping/pong heartbeat, rooms/namespaces, presence, Redis pub/sub adapter, sticky sessions, backpressure, exponential backoff reconnect.
