---
name: photoshop-uxp-scripting
description: >
    Expert knowledge for writing Adobe Photoshop UXP scripts (.psjs files) and UXP plugins using
    the Photoshop DOM API and batchPlay. Use this skill whenever the user is working on Photoshop
    automation, UXP scripting, batchPlay descriptors, executeAsModal, layer manipulation via code,
    document processing scripts, Photoshop plugin development, ExtendScript migration to UXP, or
    any task involving require('photoshop') in JavaScript. Trigger even if the user just asks how
    to automate something in Photoshop, wants to write a .psjs file, or mentions the UXP Developer Tool.
---

# Adobe Photoshop UXP Scripting

Photoshop UXP allows you to automate Photoshop using modern JavaScript (ES6+, V8 engine) via two delivery mechanisms:

- **UXP Scripts** (`.psjs` files) — Run once, no manifest needed. Simple and portable. Best for one-off automation tasks.
- **UXP Plugins** — Long-lived, can have panel UI, require a `manifest.json`. Best for tools users run repeatedly.

---

## Choosing the Right API Approach

When writing automation code, prefer APIs in this priority order:

1. **Photoshop DOM API** (`require('photoshop').app`, `.Document`, `.Layer`, etc.)  
   → High-level, readable, type-safe. Use this first.

2. **batchPlay** (`require('photoshop').action.batchPlay(...)`)  
   → Low-level, sends raw action descriptors to Photoshop's event queue. Use when a feature isn't exposed in the DOM API (e.g., applying certain filters, accessing internal Photoshop state).

See the reference files below for details on each approach.

---

## Standard Script Boilerplate

```javascript
// my-script.psjs
const { app, action, core, constants } = require('photoshop');

async function myTask(executionContext) {
    const doc = app.activeDocument;
    // ... your operations on doc, layers, etc.
}

// Wrap ALL document-modifying operations in executeAsModal
await core.executeAsModal(myTask, { commandName: 'My Custom Task' });
```

**Key rules:**

- Every operation that **modifies** Photoshop state (documents, layers, preferences) must run inside `executeAsModal`.
- Reading properties (`.width`, `.name`, `.opacity`) is synchronous and does NOT require modal scope.
- Scripts using `executeAsModal` don't need `manifest.json` or a plugin ID.

---

## Module Reference

```javascript
const ps = require('photoshop');

ps.app; // Photoshop application root → documents, preferences, actionTree
ps.action; // Low-level batchPlay, notification listeners
ps.core; // executeAsModal, showAlert, getHostEnvironment
ps.constants; // Enumerations: BlendMode, LayerKind, SaveOptions, etc.
```

---

## Critical Gotchas

| Issue                           | Explanation                                                                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| "executeAsModal required" error | You called a write-method outside a modal scope. Wrap the call in `await core.executeAsModal(fn, opts)`.                               |
| Properties are synchronous      | `layer.opacity`, `doc.width` etc. do **not** need `await` — they are synchronous even though they talk to Photoshop in the background. |
| Methods are async               | `layer.scale()`, `doc.save()`, `doc.createLayer()` etc. **do** need `await`.                                                           |
| batchPlay vs DOM                | Always prefer the DOM API. Fall back to `batchPlay` only for unexposed features.                                                       |
| Scripts vs Plugins              | Scripts can't have panel UI, can't use `window.localStorage`, have limited UXP modules.                                                |
| No manifest needed              | Scripts (`.psjs`) run directly — no `manifest.json` required.                                                                          |

---

## Reference Files

Read these files when you need deeper knowledge on a specific topic:

| File                                                                       | When to read                                                                          |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [`references/photoshop-api.md`](references/photoshop-api.md)               | Photoshop DOM objects: `app`, `Document`, `Layer`, `Action`, `ActionSet`, `Constants` |
| [`references/batchplay-guide.md`](references/batchplay-guide.md)           | batchPlay syntax, actionJSON descriptors, action references, options, reading state   |
| [`references/executeasmodal-guide.md`](references/executeasmodal-guide.md) | `executeAsModal` patterns, history suspension, progress bar, interactive mode         |
| [`references/uxp-scripting-basics.md`](references/uxp-scripting-basics.md) | Running scripts, UXP vs ExtendScript, scripts vs plugins, debugging                   |
| [`references/common-patterns.md`](references/common-patterns.md)           | Copy-paste recipes for common tasks                                                   |
