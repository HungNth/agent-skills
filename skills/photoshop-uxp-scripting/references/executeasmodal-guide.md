# executeAsModal Guide

Official docs: https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/executeasmodal/

`executeAsModal` is required for any code that modifies Photoshop state. When called, Photoshop enters a modal state that prevents other plugins from interfering, ensuring document integrity. Every write operation — creating/modifying documents, layers, preferences, UI state — must happen inside this scope.

---

## Signature

```javascript
const { core } = require('photoshop');

await core.executeAsModal(targetFunction, options);
```

| Argument         | Type             | Description                                                                                |
| ---------------- | ---------------- | ------------------------------------------------------------------------------------------ |
| `targetFunction` | `async function` | The async function to execute in modal scope. Receives `executionContext` as its argument. |
| `options`        | `Object`         | Must include `commandName`. Optionally: `interactive`.                                     |

---

## Basic Pattern

```javascript
const { app, core } = require('photoshop');

async function doWork(executionContext) {
    const doc = app.activeDocument;
    const layer = await doc.createLayer({ name: 'New Layer' });
    layer.opacity = 75; // synchronous property set — OK inside modal
    await layer.bringToFront(); // async method — needs await
}

await core.executeAsModal(doWork, { commandName: 'Create Layer' });
```

The `commandName` appears in the Photoshop progress dialog and history panel. Choose a human-readable name.

---

## The `executionContext` Object

The target function receives an `executionContext` with tools to control the modal session:

| Property/Method                         | Description                                          |
| --------------------------------------- | ---------------------------------------------------- |
| `executionContext.isCancelled`          | `boolean` — true if the user clicked Cancel          |
| `executionContext.reportProgress(opts)` | Update the progress bar displayed to the user        |
| `executionContext.hostControl`          | Object with `suspendHistory()` and `resumeHistory()` |

---

## User Cancellation

Photoshop shows a progress bar with a Cancel button during modal execution. Check `isCancelled` in long loops:

```javascript
async function processLayers(executionContext) {
    const layers = app.activeDocument.layers;
    for (let i = 0; i < layers.length; i++) {
        if (executionContext.isCancelled) {
            console.log('Cancelled by user');
            break;
        }
        await layers[i].scale(50, 50);
        executionContext.reportProgress({
            value: i / layers.length,
            commandName: `Processing ${i + 1} of ${layers.length}`,
        });
    }
}

await core.executeAsModal(processLayers, { commandName: 'Scale All Layers' });
```

---

## Progress Bar Reporting

```javascript
executionContext.reportProgress({
    value: 0.5, // 0.0 to 1.0
    commandName: 'Step 2 of 4: Merging', // text shown in the progress dialog
});
```

---

## History State Suspension

By default, each DOM method or batchPlay call creates its own undo step. To group all changes into **one undoable step**:

```javascript
async function doMultiStepWork(executionContext) {
    const { hostControl } = executionContext;
    const doc = app.activeDocument;

    // Begin grouping under one history state
    const suspensionID = await hostControl.suspendHistory({
        documentID: doc.id,
        name: 'My Custom Operation', // shown in the History panel
    });

    // Everything here is one undo step
    await doc.createLayer({ name: 'Layer A' });
    await doc.createLayer({ name: 'Layer B' });
    await doc.flatten();

    // End the group
    await hostControl.resumeHistory(suspensionID);
}

await core.executeAsModal(doMultiStepWork, {
    commandName: 'My Custom Operation',
});
```

> **Why this matters:** Without suspension, each operation creates its own history entry. With suspension, the user can undo your entire script's work with a single Ctrl+Z / Cmd+Z.

---

## Interactive Mode

Added in Photoshop 23.3. Use when your script needs the user to interact with Photoshop UI (e.g., a filter dialog, Select and Mask workspace).

In interactive mode:

- No blocking progress dialog is shown
- The user can interact with Photoshop normally
- They can cancel via **Plugins > Cancel Plugin Command**

```javascript
await core.executeAsModal(
    async (executionContext) => {
        // Photoshop will show the filter dialog (no radius = prompts user)
        await action.batchPlay([{ _obj: 'gaussianBlur' }], {});
    },
    {
        commandName: 'Apply Filter Interactively',
        interactive: true,
    },
);
```

---

## Scripts vs Plugins: Modal Differences

| Context                  | Behavior                                                                                                                                                                                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **UXP Plugin**           | Must explicitly use `executeAsModal` for all write operations. Calling a write method outside it throws an error.                                                                                                      |
| **UXP Script (`.psjs`)** | Top-level `await`ed write operations may work without explicit `executeAsModal`, because scripts run in an implicit modal scope. But you should still use it explicitly for history suspension and progress reporting. |

**Recommendation:** Always use `executeAsModal` explicitly — it makes code portable between scripts and plugins and provides better UX.

---

## Don't Nest executeAsModal

`executeAsModal` cannot be nested. Design helpers to do work directly (not wrapping in their own modal):

```javascript
// BAD: helper wraps itself — will throw if called inside an existing modal
async function renameLayer(layer, newName) {
    await core.executeAsModal(
        async () => {
            layer.name = newName;
        },
        { commandName: 'Rename' },
    );
}

// GOOD: helper just does the work; caller provides the modal context
async function renameLayer(layer, newName) {
    layer.name = newName; // synchronous — fine inside parent modal scope
}

await core.executeAsModal(
    async (ctx) => {
        await renameLayer(layerA, 'Name A');
        await renameLayer(layerB, 'Name B');
    },
    { commandName: 'Rename Layers' },
);
```

---

## Error Handling

```javascript
try {
    await core.executeAsModal(
        async (executionContext) => {
            // ... operations
        },
        { commandName: 'My Operation' },
    );
} catch (err) {
    if (err.number === 9) {
        console.log('Cancelled by user');
    } else {
        console.error('Error:', err.message);
    }
}
```
