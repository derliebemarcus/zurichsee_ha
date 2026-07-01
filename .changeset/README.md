# Changesets

Add one Markdown file in this directory for every change that should produce a release.

Example:

```markdown
---
"homeassistant_zurichsee": patch
---

Describe the user-visible change.
```

Use `patch`, `minor` or `major` explicitly. CI-only and documentation-only changes do not require a Changeset.

Jenkins consumes pending Changesets into a version pull request. After that pull request is merged and the next `main` quality build passes, Jenkins creates the tag, uploads the integration archive to a draft GitHub Release and publishes the immutable release.
