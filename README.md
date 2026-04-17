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

### Must have skills for all agents:

```bash
npx skills add https://github.com/obra/superpowers --skill executing-plans
npx skills add https://github.com/obra/superpowers --skill writing-plans
npx skills add https://github.com/obra/superpowers --skill brainstorming

npx skills add https://github.com/anthropics/claude-code --skill 'Skill Development'
npx skills add https://github.com/anthropics/skills --skill skill-creator

npx skills add https://github.com/github/awesome-copilot --skill refactor-plan

npx skills add https://github.com/antfu/skills --skill vite
npx skills add https://github.com/antfu/skills --skill pnpm

npx skills add https://github.com/github/awesome-copilot --skill create-readme
```

### Frontend

```bash
npx skills add https://github.com/anthropics/skills --skill frontend-design
npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max

npx skills add https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser

npx skills add https://github.com/wshobson/agents --skill typescript-advanced-types
npx skills add https://github.com/wshobson/agents --skill modern-javascript-patterns
npx skills add https://github.com/wshobson/agents --skill tailwind-design-system
npx skills add https://github.com/wshobson/agents --skill web-component-design

npx skills add https://github.com/secondsky/claude-skills --skill tailwind-v4-shadcn
npx skills add https://github.com/shadcn/ui --skill shadcn

npx skills add greensock/gsap-skills
```

### Vue

```bash
npx skills add https://github.com/hyf0/vue-skills --skill vue-best-practices
npx skills add https://github.com/antfu/skills --skill vue-router-best-practices
npx skills add https://github.com/antfu/skills --skill nuxt
npx skills add https://github.com/antfu/skills --skill pinia

npx skills add https://github.com/nuxt/ui --skill nuxt-ui

```

### Laravel

```bash
npx skills add https://github.com/jeffallan/claude-skills --skill laravel-specialist
npx skills add https://github.com/laravel/boost --skill laravel-best-practices
npx skills add https://github.com/jeffallan/claude-skills --skill php-pro
```

### Database

```bash
npx skills add https://github.com/wshobson/agents --skill sql-optimization-patterns
npx skills add https://github.com/github/awesome-copilot --skill sql-code-review
```

### API

```bash
npx skills add https://github.com/wshobson/agents --skill api-design-principles
npx skills add https://github.com/supercent-io/skills-template --skill api-documentation
```

### Swift

```bash
npx skills add https://github.com/avdlee/swiftui-agent-skill --skill swiftui-expert-skill
npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro
```

### Github

```bash
npx skills add https://github.com/wshobson/agents --skill github-actions-templates
```

---

## Quick add template

Use this block when you want to add a new group or add another skill:

```md
npx skills add https://github.com/HungNth/agent-skills --skill <alias>
```
