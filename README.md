# Agent Skills

This repo is used to:

- store custom skills in `skills/`
- store skill installation commands grouped by purpose for quick copy/paste later

## Custom skills

Custom skills currently available in this repo:

```text
skills/
├─ flow-launcher-nodejs-plugin/
├─ openspec-agy-delivery/
└─ photoshop-uxp-scripting/
```

### Install custom skills

```bash
npx skills add https://github.com/HungNth/agent-skills --skill photoshop-uxp-scripting -y
```

```bash
npx skills add https://github.com/HungNth/agent-skills --skill flow-launcher-nodejs-plugin -y
```

```bash
npx skills add https://github.com/HungNth/agent-skills --skill openspec-agy-delivery --agent universal --copy -y
```

Install this orchestration skill for OMP only. Do not install or invoke it as an AGY implementation skill.

Use OpenSpec planning first, then send a separate delivery request after reviewing the artifacts:

```text
/opsx-explore
/opsx-propose <change>

Deliver <change> through openspec-agy-delivery.
```

---

## Useful skills

### Optional supporting skills

- Install **Global** Skills:

```bash
npx skills add https://github.com/github/awesome-copilot --skill create-readme -g -y
```

- Optionally use [Superpowers](https://github.com/obra/superpowers) with [OpenSpec](https://github.com/Fission-AI/OpenSpec). The delivery workflow does not require these skills.

```bash

npx skills add https://github.com/obra/superpowers --skill requesting-code-review -y
npx skills add https://github.com/obra/superpowers --skill test-driven-development -y
npx skills add https://github.com/obra/superpowers --skill systematic-debugging -y
npx skills add https://github.com/obra/superpowers --skill receiving-code-review -y
npx skills add https://github.com/obra/superpowers --skill verification-before-completion -y

# Git
npx skills add https://github.com/obra/superpowers --skill finishing-a-development-branch
npx skills add https://github.com/obra/superpowers --skill using-git-worktrees -y

```

- None OpenSpec:

```bash
npx skills add https://github.com/obra/superpowers --skill executing-plans -y
npx skills add https://github.com/obra/superpowers --skill writing-plans -y
npx skills add https://github.com/obra/superpowers --skill brainstorming -y

npx skills add https://github.com/obra/superpowers --skill requesting-code-review -y
npx skills add https://github.com/obra/superpowers --skill test-driven-development -y
npx skills add https://github.com/obra/superpowers --skill systematic-debugging -y
npx skills add https://github.com/obra/superpowers --skill requesting-code-review -y
npx skills add https://github.com/obra/superpowers --skill receiving-code-review -y
npx skills add https://github.com/obra/superpowers --skill verification-before-completion -y

npx skills add https://github.com/obra/superpowers --skill finishing-a-development-branch
npx skills add https://github.com/obra/superpowers --skill using-git-worktrees -y

```

### JavaScript / TypeScript

```bash
npx skills add https://github.com/wshobson/agents --skill typescript-advanced-types -y
npx skills add https://github.com/wshobson/agents --skill modern-javascript-patterns -y

npx skills add https://github.com/antfu/skills --skill vite -y
npx skills add https://github.com/antfu/skills --skill pnpm -y
```

### Frontend

```bash
npx skills add https://github.com/Leonxlnx/taste-skill -y
npx skills add https://github.com/anthropics/skills --skill frontend-design -y
npx skills add https://github.com/wshobson/agents --skill web-component-design -y

npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser -y

npx skills add https://github.com/wshobson/agents --skill tailwind-design-system -y
npx skills add https://github.com/secondsky/claude-skills --skill tailwind-v4-shadcn -y
npx skills add https://github.com/shadcn/ui --skill shadcn -y

npx skills add greensock/gsap-skills -y
npx skills add diffusionstudio/lottie -y
```

### React

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices -y
```

### Vue

```bash
npx skills add https://github.com/hyf0/vue-skills --skill vue-best-practices -y
npx skills add https://github.com/antfu/skills --skill vue-router-best-practices -y
npx skills add https://github.com/antfu/skills --skill nuxt -y
npx skills add https://github.com/antfu/skills --skill pinia -y

npx skills add https://github.com/nuxt/ui --skill nuxt-ui -y

```

### Laravel

```bash
npx skills add https://github.com/jeffallan/claude-skills --skill laravel-specialist -y
npx skills add MrPunyapal/laravel-attributes-list --skill laravel-attributes -y
npx skills add https://github.com/laravel/boost --skill laravel-best-practices -y
npx skills add https://github.com/jeffallan/claude-skills --skill php-pro -y
```

### WordPress

```bash
npx skills add https://github.com/wordpress/agent-skills --skill wp-plugin-development -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-rest-api -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-block-themes -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-block-development -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-performance -y
npx skills add https://github.com/wordpress/agent-skills --skill wordpress-router -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-wpcli-and-ops -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-abilities-api -y
npx skills add https://github.com/wordpress/agent-skills --skill wp-interactivity-api -y
npx skills add https://github.com/wordpress/agent-skills --skill wpds -y
npx skills add https://github.com/bartekmis/wordpress-performance-best-practises --skill wordpress-performance-best-practices -y
npx skills add https://github.com/automattic/wordpress-activitypub --skill code-style -y
npx skills add https://github.com/jeffallan/claude-skills --skill wordpress-pro -y

npx skills add https://github.com/sickn33/antigravity-awesome-skills --skill wordpress-woocommerce-development -y

```

# Browser Extension

```bash
npx skills add https://github.com/addyosmani/agent-skills --skill code-simplification -y
npx skills add https://github.com/github/awesome-copilot --skill chrome-devtools -y
npx skills add https://github.com/mindrally/skills --skill chrome-extension-development -y
npx skills add https://github.com/quangpl/browser-extension-skills --skill extension-ui -y
npx skills add https://github.com/quangpl/browser-extension-skills --skill extension-analyze -y
```

### Database

```bash
npx skills add https://github.com/wshobson/agents --skill sql-optimization-patterns -y
npx skills add https://github.com/github/awesome-copilot --skill sql-code-review -y

npx skills add https://github.com/wshobson/agents --skill postgresql-table-design -y
```

### Performance / Optimization

```bash
npx skills add https://github.com/addyosmani/agent-skills --skill performance-optimization -y

npx skills add https://github.com/addyosmani/agent-skills --skill code-simplification -y
```

### API

```bash
npx skills add https://github.com/wshobson/agents --skill api-design-principles -y
```

### Git / Github

```bash
npx skills add https://github.com/addyosmani/agent-skills --skill git-workflow-and-versioning -y
npx skills add https://github.com/wshobson/agents --skill github-actions-templates -y
```

### Swift

```bash
npx skills add https://github.com/avdlee/swiftui-agent-skill --skill swiftui-expert-skill -y
npx skills add https://github.com/twostraws/swiftui-agent-skill --skill swiftui-pro -y
```

### Golang

```bash
npx skills add JetBrains/go-modern-guidelines
```
