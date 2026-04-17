# Common Photoshop UXP Patterns & Recipes

Ready-to-use code patterns for the most common Photoshop automation tasks.

## Table of Contents

1. [Script boilerplate with history suspension](#1-script-boilerplate-with-history-suspension)
2. [Create document and add layers](#2-create-document-and-add-layers)
3. [Batch process all open documents](#3-batch-process-all-open-documents)
4. [Iterate all layers including groups (recursive)](#4-iterate-all-layers-including-groups-recursive)
5. [Export document as JPEG or PNG](#5-export-document-as-jpeg-or-png)
6. [Add a text watermark via batchPlay](#6-add-a-text-watermark-via-batchplay)
7. [Find a layer by name (recursive)](#7-find-a-layer-by-name-recursive)
8. [Set layer properties](#8-set-layer-properties)
9. [Replace Smart Object contents](#9-replace-smart-object-contents)
10. [Find and play an Action](#10-find-and-play-an-action)
11. [Set foreground and background color](#11-set-foreground-and-background-color)
12. [Fill active layer with solid color](#12-fill-active-layer-with-solid-color)
13. [Deselect all / select all](#13-deselect-all--select-all)
14. [Read all document properties (dev only)](#14-read-all-document-properties-dev-only)
15. [Show a custom input prompt dialog](#15-show-a-custom-input-prompt-dialog)

---

## 1. Script Boilerplate with History Suspension

```javascript
// my-script.psjs
const { app, action, core, constants } = require('photoshop');

async function main(executionContext) {
    const { hostControl } = executionContext;
    const doc = app.activeDocument;

    // Group all changes into one undo step
    const suspensionID = await hostControl.suspendHistory({
        documentID: doc.id,
        name: 'My Script Operation',
    });

    try {
        // === YOUR WORK GOES HERE ===
    } catch (err) {
        console.error('Script error:', err);
    } finally {
        await hostControl.resumeHistory(suspensionID);
    }
}

await core.executeAsModal(main, { commandName: 'My Script Operation' });
```

---

## 2. Create Document and Add Layers

```javascript
const { app, core, constants } = require('photoshop');

await core.executeAsModal(
    async () => {
        const doc = await app.createDocument({
            width: 1920,
            height: 1080,
            resolution: 72,
            mode: constants.ColorMode.RGB,
            fill: constants.DocumentFill.TRANSPARENT,
            name: 'New Document',
        });

        const bg = await doc.createLayer({
            name: 'Background',
            opacity: 100,
            blendMode: constants.BlendMode.NORMAL,
        });

        const overlay = await doc.createLayer({
            name: 'Overlay',
            opacity: 50,
            blendMode: constants.BlendMode.MULTIPLY,
        });

        // Group both layers into a folder
        await doc.createLayerGroup({
            name: 'Content',
            fromLayers: [bg, overlay],
        });
    },
    { commandName: 'Create New Document' },
);
```

---

## 3. Batch Process All Open Documents

```javascript
const { app, core, constants } = require('photoshop');

await core.executeAsModal(
    async (executionContext) => {
        const docs = [...app.documents]; // snapshot the list

        for (let i = 0; i < docs.length; i++) {
            if (executionContext.isCancelled) break;

            const doc = docs[i];
            executionContext.reportProgress({
                value: i / docs.length,
                commandName: `Processing: ${doc.name}`,
            });

            // Example: flatten, resize, save each document
            await doc.flatten();
            await doc.resizeImage(
                1920,
                1080,
                72,
                constants.ResampleMethod.BICUBIC,
            );
            await doc.save();
        }
    },
    { commandName: 'Batch Process All Documents' },
);
```

---

## 4. Iterate All Layers Including Groups (Recursive)

```javascript
const { constants } = require('photoshop');

function getAllLayers(layerList) {
    let all = [];
    for (const layer of layerList) {
        all.push(layer);
        if (layer.kind === constants.LayerKind.GROUP && layer.layers) {
            all = all.concat(getAllLayers(layer.layers));
        }
    }
    return all;
}

// Usage:
const { app, core } = require('photoshop');
await core.executeAsModal(
    async () => {
        const doc = app.activeDocument;
        const allLayers = getAllLayers(doc.layers);
        console.log(
            'All layers:',
            allLayers.map((l) => l.name),
        );
    },
    { commandName: 'List All Layers' },
);
```

---

## 5. Export Document as JPEG or PNG

```javascript
const { app, core } = require('photoshop');
const uxp = require('uxp');

await core.executeAsModal(
    async () => {
        const doc = app.activeDocument;
        const folder = await uxp.storage.localFileSystem.getFolder();

        // Export as JPEG
        const jpegFile = await folder.createFile(`${doc.name}.jpg`, {
            overwrite: true,
        });
        await doc.saveAs.jpg(jpegFile, {
            quality: 85,
            embedColorProfile: true,
        });

        // Export as PNG (use instead of JPEG if needed)
        // const pngFile = await folder.createFile(`${doc.name}.png`, { overwrite: true });
        // await doc.saveAs.png(pngFile, { compression: 6, interlaced: false });

        // Open the output folder in the OS
        await uxp.shell.openPath(folder.nativePath);
    },
    { commandName: 'Export Document' },
);
```

---

## 6. Add a Text Watermark via batchPlay

```javascript
const { app, action, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        const doc = app.activeDocument;

        // Create text layer via batchPlay (DOM doesn't expose createTextLayer directly)
        await action.batchPlay(
            [
                {
                    _obj: 'make',
                    _target: [{ _ref: 'layer' }],
                    using: {
                        _obj: 'layer',
                        type: {
                            _obj: 'textLayer',
                            textKey: '© My Brand 2024',
                            textStyleRange: [
                                {
                                    _obj: 'textStyleRange',
                                    from: 0,
                                    to: 14,
                                    textStyle: {
                                        _obj: 'textStyle',
                                        size: {
                                            _unit: 'pointsUnit',
                                            _value: 48,
                                        },
                                        color: {
                                            _obj: 'RGBColor',
                                            red: 255,
                                            grain: 255,
                                            blue: 255,
                                        },
                                    },
                                },
                            ],
                        },
                    },
                },
            ],
            {},
        );

        const textLayer = doc.activeLayers[0];
        textLayer.name = 'Watermark';
        textLayer.opacity = 60;
        await textLayer.bringToFront();
    },
    { commandName: 'Add Watermark' },
);
```

---

## 7. Find a Layer by Name (Recursive)

```javascript
const { constants } = require('photoshop');

function findLayerByName(layerList, name) {
    for (const layer of layerList) {
        if (layer.name === name) return layer;
        if (layer.kind === constants.LayerKind.GROUP && layer.layers) {
            const found = findLayerByName(layer.layers, name);
            if (found) return found;
        }
    }
    return null;
}

// Usage:
const { app, core } = require('photoshop');
await core.executeAsModal(
    async () => {
        const doc = app.activeDocument;
        const layer = findLayerByName(doc.layers, 'Logo');
        if (layer) {
            layer.visible = true;
            console.log('Found layer:', layer.name, layer.bounds);
        } else {
            console.log('Layer not found');
        }
    },
    { commandName: 'Find Layer' },
);
```

---

## 8. Set Layer Properties

```javascript
const { app, core, constants } = require('photoshop');

await core.executeAsModal(
    async () => {
        const layer = app.activeDocument.activeLayers[0];

        // Synchronous property assignments (no await needed)
        layer.name = 'Renamed Layer';
        layer.opacity = 75;
        layer.fillOpacity = 100;
        layer.visible = true;
        layer.blendMode = constants.BlendMode.MULTIPLY;

        // Async transform methods (await required)
        await layer.scale(50, 50); // 50% of current size
        await layer.translate(100, 0); // move right 100px
        await layer.rotate(15); // rotate 15 degrees
        await layer.bringToFront();
    },
    { commandName: 'Modify Layer' },
);
```

---

## 9. Replace Smart Object Contents

```javascript
const { app, action, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        const layer = app.activeDocument.activeLayers[0]; // must be a Smart Object

        await action.batchPlay(
            [
                {
                    _obj: 'placedLayerReplaceContents',
                    _target: [{ _ref: 'layer', _id: layer.id }],
                    null: {
                        _path: 'C:/path/to/new-image.png',
                        _kind: 'local',
                    },
                },
            ],
            {},
        );
    },
    { commandName: 'Replace Smart Object' },
);
```

---

## 10. Find and Play an Action

```javascript
const { app, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        const SET_NAME = 'Default Actions';
        const ACTION_NAME = 'Wood Frame - 50 pixel';

        const actionSet = app.actionTree.find((s) => s.name === SET_NAME);
        if (!actionSet) {
            console.log('Action set not found');
            return;
        }

        const act = actionSet.actions.find((a) => a.name === ACTION_NAME);
        if (!act) {
            console.log('Action not found');
            return;
        }

        await act.play();
    },
    { commandName: 'Play Action' },
);
```

---

## 11. Set Foreground and Background Color

```javascript
const { action, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        // Set foreground to red
        await action.batchPlay(
            [
                {
                    _obj: 'set',
                    _target: [{ _ref: 'color', _property: 'foregroundColor' }],
                    to: { _obj: 'RGBColor', red: 255, grain: 0, blue: 0 },
                },
            ],
            {},
        );

        // Set background to white
        await action.batchPlay(
            [
                {
                    _obj: 'set',
                    _target: [{ _ref: 'color', _property: 'backgroundColor' }],
                    to: { _obj: 'RGBColor', red: 255, grain: 255, blue: 255 },
                },
            ],
            {},
        );
    },
    { commandName: 'Set Colors' },
);
```

---

## 12. Fill Active Layer with Solid Color

```javascript
const { action, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        // First set foreground to desired color (see pattern #11)
        await action.batchPlay(
            [
                {
                    _obj: 'fill',
                    using: { _enum: 'fillContents', _value: 'foregroundColor' },
                    opacity: { _unit: 'percentUnit', _value: 100 },
                    mode: { _enum: 'blendMode', _value: 'normal' },
                },
            ],
            {},
        );
    },
    { commandName: 'Fill Layer' },
);
```

---

## 13. Deselect All / Select All

```javascript
const { action, core } = require('photoshop');

await core.executeAsModal(
    async () => {
        // Deselect all
        await action.batchPlay(
            [
                {
                    _obj: 'set',
                    _target: [{ _ref: 'channel', _property: 'selection' }],
                    to: { _enum: 'ordinal', _value: 'none' },
                },
            ],
            {},
        );

        // Select all (use instead if needed)
        // await action.batchPlay([{ _obj: "selectAll" }], {});
    },
    { commandName: 'Deselect' },
);
```

---

## 14. Read All Document Properties (Dev Only)

```javascript
// WARNING: slow — use only during development to discover property names
const { app, action } = require('photoshop');

const doc = app.activeDocument;
const result = await action.batchPlay(
    [
        {
            _obj: 'get',
            _target: {
                _ref: [
                    { _ref: 'document', _id: doc.id },
                    { _ref: 'application' },
                ],
            },
        },
    ],
    {},
);

console.log(JSON.stringify(result[0], null, 2));
```

---

## 15. Show a Custom Input Prompt Dialog

```javascript
function showPrompt(title, label, defaultValue = '') {
    return new Promise((resolve) => {
        const dialog = document.createElement('dialog');
        dialog.style.cssText =
            'padding:20px; min-width:340px; font-family:sans-serif;';
        dialog.innerHTML = `
      <form method="dialog" style="display:flex; flex-direction:column; gap:14px;">
        <h3 style="margin:0; font-size:15px;">${title}</h3>
        <label style="display:flex; flex-direction:column; gap:5px; font-size:13px;">
          ${label}
          <input id="inp" type="text" value="${defaultValue}"
            style="padding:6px 8px; font-size:13px; border:1px solid #888; border-radius:4px;" />
        </label>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" id="cancel-btn"
            style="padding:6px 14px; cursor:pointer;">Cancel</button>
          <button type="submit"
            style="padding:6px 14px; background:#0070d1; color:#fff; border:none; border-radius:4px; cursor:pointer;">OK</button>
        </div>
      </form>
    `;
        dialog.querySelector('#cancel-btn').onclick = () => {
            dialog.close();
            resolve(null);
        };
        dialog.addEventListener('close', () =>
            resolve(dialog.querySelector('#inp').value.trim() || null),
        );
        document.body.appendChild(dialog);
        dialog.showModal();
        dialog.querySelector('#inp').select();
    });
}

// Usage:
const { app, core } = require('photoshop');
const newName = await showPrompt(
    'Rename Layer',
    'Enter layer name:',
    'My Layer',
);
if (newName) {
    await core.executeAsModal(
        async () => {
            app.activeDocument.activeLayers[0].name = newName;
        },
        { commandName: 'Rename Layer' },
    );
}
```
