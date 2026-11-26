# Shared message contract

Owned by M5; reviewed by all affected module teams. This is not a separate module or a running service.

The November project document sections 2.2–2.3 and 8.3 define the baseline: mm, mm/s, rpm, per mille, and monotonic times; binary serial at 115200 8N1, little-endian, start bytes A5 5A, type, length, session ID, sequence, payload and CRC-16/CCITT-FALSE (check 0x29B1). Network uses JSON over UDP; browsers use WebSocket.

Planned directories: python/ and cpp/ codecs, schemas/ message definitions, test_vectors/ known bytes and tests/ cross-language checks. protocol.md must specify every field, wire type, range, rate and timeout before freeze. Do not treat this README as a complete wire specification. No codecs or vectors have been implemented yet.
