# Online CI Repair Report

Repository: OMNIA-VALIDATION

Timestamp UTC: 2026-05-21T18:27:19Z

Purpose:
Repair red GitHub Actions by replacing the CI workflow with a canonical workflow.

Release created: false
Tag created: false

Boundary:
measurement != inference != decision

Before online snapshot:
{
  "repo": "OMNIA-VALIDATION",
  "ok": true,
  "api_status": 200,
  "latest_runs": [
    {
      "id": 26244898379,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26244898379",
      "created_at": "2026-05-21T18:20:49Z",
      "updated_at": "2026-05-21T18:20:49Z",
      "head_sha": "d717613cdd5d09b7c0d94fbc183c2a4c566078e4"
    },
    {
      "id": 26244187335,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26244187335",
      "created_at": "2026-05-21T18:06:40Z",
      "updated_at": "2026-05-21T18:06:40Z",
      "head_sha": "c61ca6158b5a0b424525b89247c3ffd93270a69b"
    },
    {
      "id": 26240257009,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26240257009",
      "created_at": "2026-05-21T16:51:24Z",
      "updated_at": "2026-05-21T16:51:24Z",
      "head_sha": "8c8d64724904ac86263489bda559ea1744233bcf"
    },
    {
      "id": 26233218575,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26233218575",
      "created_at": "2026-05-21T14:43:38Z",
      "updated_at": "2026-05-21T14:43:38Z",
      "head_sha": "50ae5d6a5e8f92091caa5c271c76d8a76c276691"
    },
    {
      "id": 26232451816,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26232451816",
      "created_at": "2026-05-21T14:30:07Z",
      "updated_at": "2026-05-21T14:30:07Z",
      "head_sha": "c668566d2ab99932123b73af39992cb1ad646f69"
    },
    {
      "id": 26232058009,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26232058009",
      "created_at": "2026-05-21T14:23:17Z",
      "updated_at": "2026-05-21T14:23:51Z",
      "head_sha": "bb00182a25eb1da939bd2cf21f6a330ac656226c"
    },
    {
      "id": 26231244172,
      "name": ".github/workflows/ci.yml",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26231244172",
      "created_at": "2026-05-21T14:08:53Z",
      "updated_at": "2026-05-21T14:08:53Z",
      "head_sha": "01629d354d50f506a79a4abacfc2880c17bebe4a"
    },
    {
      "id": 26224199062,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26224199062",
      "created_at": "2026-05-21T11:51:59Z",
      "updated_at": "2026-05-21T11:52:34Z",
      "head_sha": "dc4b2bce156832256ec8f4ce735741c8857063ae"
    },
    {
      "id": 26220611953,
      "name": "CI",
      "status": "completed",
      "conclusion": "failure",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26220611953",
      "created_at": "2026-05-21T10:31:59Z",
      "updated_at": "2026-05-21T10:32:34Z",
      "head_sha": "e98a397c2e98011c431725f53b80f038ae741ef8"
    },
    {
      "id": 26218963160,
      "name": "CI",
      "status": "completed",
      "conclusion": "success",
      "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26218963160",
      "created_at": "2026-05-21T09:56:22Z",
      "updated_at": "2026-05-21T09:56:55Z",
      "head_sha": "99b0eeb2d1e28fa01b59f36eea4d3ec8143ce0be"
    }
  ],
  "latest_failure": {
    "id": 26244898379,
    "name": ".github/workflows/ci.yml",
    "status": "completed",
    "conclusion": "failure",
    "html_url": "https://github.com/Tuttotorna/OMNIA-VALIDATION/actions/runs/26244898379",
    "created_at": "2026-05-21T18:20:49Z",
    "updated_at": "2026-05-21T18:20:49Z",
    "head_sha": "d717613cdd5d09b7c0d94fbc183c2a4c566078e4"
  }
}

Patch:
{
  "ci_changed": true,
  "legacy_removed": [],
  "duplicate_removed": []
}

Local tests:
{
  "status": "pass",
  "passed": 355,
  "failed": 0,
  "errors": 0,
  "returncode": 0,
  "summary": "355 passed in 3.19s"
}

Push:
null

After online check:
null
