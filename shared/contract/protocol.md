# Shared message protocol — draft baseline

**Status: DRAFT, not frozen.** M5 owns implementation and coordinates review with M1–M4 (issue #1). Source: November 2026 Project and Module Documentation, sections 2.2–2.6 and 8.3. This document is not a complete wire specification.

## Transport and units

- Height: ball centre above bottom grille in mm; velocity: mm/s; speed: rpm; power: per mille (0–1000); time: ms (capture time may use µs). JSON may contain decimal frequency and gains.
- Serial: 115200 baud, 8N1; little-endian multi-byte fields.
- Binary frame: A5 5A (2 bytes), type (1), payload length (1), session ID (4), sequence (4), payload, CRC (2).
- CRC-16/CCITT-FALSE: polynomial 0x1021, initial 0xFFFF, no reflection, final XOR 0x0000. Covers type through payload, excluding start bytes and CRC. ASCII 123456789 gives 0x29B1.
- UDP: one JSON message per datagram with type, src, session and t. Gateway relays JSON to browsers via WebSocket.

## Message inventory

| Message | Direction / transport | Rate | Content |
|---|---|---|---|
| height | M2 → M3 serial; M2 → M5/M1 tool UDP | every frame ≥60 Hz | raw height and validity, filtered height, velocity, validity, bridged, frame number, capture time, fps |
| fan_cmd | M3 → M1 serial | 100 Hz | requested bottom rpm, top assist, enable, re-arm, sequence |
| fan_config | M3 → M1 serial | on change | speed-loop gains, rate and power limits |
| fan_state | M1 → M3 serial | 100 Hz | measured bottom speed, applied power, state, fault, echoed sequence |
| target_points | M4 → M3 UDP | 30 Hz | timestamped heights up to 200 ms ahead, extra rpm above hover, top assist |
| game_in | M3 → M5 game board serial | 30 Hz | height or invalid, usable range, game enabled, obstacle speed |
| game_out | M5 game board → M3 serial | 30 Hz and events | target level, hit, phase, score |
| status | M3 → M5/M4 UDP | 30 Hz | state, mode, target, height used, speed/power, game phase/score, fault |
| model_height | M4 → M5 UDP | 30 Hz | predicted ghost-ball height |
| command, ack | M5 ↔ M2/M3/M4 UDP | on change | parameter, value, request ID; result, applied value or reason |
| marker, health | M5 → browser WebSocket | on change / 1 Hz | accepted parameter changes; module online state |

## Safety and freshness

- New serial frames carry increasing sequence numbers within a session. Duplicate and older frames are ignored and must not refresh timeouts.
- New sender sessions reset receiver sequence tracking. Restart behavior must be verified per module; returning traffic cannot automatically restart blowers.
- M3: no new real measurement for 200 ms → Fault and disabled zero-speed command. Bridged and duplicate heights never refresh this timer.
- M1: no new valid fan_cmd for 100 ms → outputs off. M3: missing fan_state for 100 ms → Fault.
- Missing trajectory/game targets: hold last target. Game pauses after 200 ms without game_in. Command unconfirmed after 500 ms; module offline after 3 s.
- Receiver monotonic clocks measure timeouts; camera capture-time differences determine PID dt. Target clock offsets require explicit handling.
- Hardware watchdog cutoff at most 250 ms; E-stop independently cuts supply. These are not software-only validation claims.

## Port baseline

M2 commands 5003; M3 5005; M4 trajectory 5006 and model 5007; M5 gateway 5010; HTTP/WebSocket 8080. Use configuration files.

## Freeze checklist (M5 with all affected teams)

- [ ] Define exact message type IDs, field names, widths, signedness, units, ranges and payload layouts; CRC byte order and parser resynchronization.
- [ ] Define JSON schemas, request ID and retry/duplicate handling, timestamps and session behavior.
- [ ] Resolve ambiguous restart cases, sequence wrap and command scheduling tolerances with affected teams.
- [ ] Specify characterization CSV, model file and session log formats.
- [ ] Implement compatible Python/C++ codecs and validators.
- [ ] Create golden vectors for every message plus malformed, duplicate and restarted-session cases.
- [ ] Run T5.1 on Windows/Linux; document actual results.
- [ ] Obtain affected teams' agreement; record version and freeze date.

No new field layouts, IDs or safety limits are approved by this draft. A protocol change after freeze requires coordinated review.
