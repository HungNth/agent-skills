# Agent Skills

This repo is used to:

- store custom skills in `skills/`
- store skill installation commands grouped by purpose for quick copy/paste later

## Custom skills

Custom skills currently available in this repo:

```text
skills/
└─ photoshop-uxp-scripting/
```

### Install custom skills

```bash
npx skills add https://github.com/HungNth/agent-skills --skill photoshop-uxp-scripting
```

---

## Useful skills

### Plan

```bash
npx skills add https://github.com/obra/superpowers --skill executing-plans
npx skills add https://github.com/obra/superpowers --skill writing-plans
```

### Frontend

```bash
npx skills add https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
npx skills add https://github.com/wshobson/agents --skill typescript-advanced-types
```

---

## Quick add template

Use this block when you want to add a new group or add another skill:

```md
npx skills add https://github.com/HungNth/agent-skills --skill <alias>
```
