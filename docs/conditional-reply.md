# Conditional Reply Phase

## Feasibility

Yes. Once messages are collected and normalized, the archive can support condition-based reply behavior.

Examples:

- If a selected person asks for a known document, draft a reply with the matching file link.
- If a group chat contains a deadline keyword, create a task or reminder.
- If a known customer asks an FAQ, draft a canned answer.
- If urgency words appear after business hours, notify the operator.

## Recommended Safety Model

Start with `draft-only`.

```text
message -> rule match -> draft reply -> human confirmation -> send
```

Only after enough false-positive testing should any rule become auto-send.

## Rule Shape

```json
{
  "id": "faq-price",
  "enabled": true,
  "chatLabels": ["example-group"],
  "conditions": {
    "containsAny": ["가격", "비용", "견적"]
  },
  "action": {
    "type": "draft_reply",
    "template": "가격 안내 자료를 확인해보겠습니다."
  }
}
```

## Sending

The current Mac path can use `kakaocli send`, but real chat sending should require confirmation. Use self-chat only for automated tests.

