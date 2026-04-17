# Photoshop DOM API Reference

Official docs: https://developer.adobe.com/photoshop/uxp/2022/ps_reference/

## Accessing the API

```javascript
const { app, action, core, constants } = require('photoshop');
```

The `require('photoshop')` module exposes four top-level exports:

- `app` — root of the Photoshop object model
- `action` — low-level batchPlay and notification system
- `core` — executeAsModal, showAlert, host info
- `constants` — all enumerations (BlendMode, LayerKind, etc.)

---

## `app` — Photoshop Application

Root DOM object. Access application-level settings, open documents, and the action tree.

### Properties (synchronous — no await needed)

| Property              | Type          | Description                          |
| --------------------- | ------------- | ------------------------------------ |
| `app.activeDocument`  | `Document`    | The currently active document        |
| `app.documents`       | `Documents[]` | Array of all open documents          |
| `app.actionTree`      | `ActionSet[]` | All action sets in the Actions panel |
| `app.foregroundColor` | `SolidColor`  | Current foreground color             |
| `app.backgroundColor` | `SolidColor`  | Current background color             |
| `app.preferences`     | `Preferences` | Application preferences              |

### Methods (async — use await, must be inside executeAsModal)

```javascript
// Open a document
const doc = await app.open('/path/to/file.psd');

// Create a new document
const doc = await app.createDocument({
    preset: 'My Web Preset 1',
    // OR specify manually:
    width: 1920,
    height: 1080,
    resolution: 72,
    mode: constants.ColorMode.RGB,
    fill: constants.DocumentFill.TRANSPARENT,
});

// Show built-in dialogs (does NOT require executeAsModal)
await core.showAlert('Done!');
```

---

## `Document`

Represents a single open PSD/image. Access from `app.activeDocument` or `app.documents[i]`.

### Properties (synchronous)

| Property               | Type                  | Description                             |
| ---------------------- | --------------------- | --------------------------------------- |
| `doc.id`               | `number`              | Unique document ID (stable for session) |
| `doc.name`             | `string`              | Filename                                |
| `doc.title`            | `string`              | Display title                           |
| `doc.width`            | `number`              | Width in pixels                         |
| `doc.height`           | `number`              | Height in pixels                        |
| `doc.resolution`       | `number`              | Resolution in PPI                       |
| `doc.colorProfileName` | `string`              | ICC profile name                        |
| `doc.mode`             | `constants.ColorMode` | RGB, CMYK, Grayscale, etc.              |
| `doc.layers`           | `Layer[]`             | Top-level layers                        |
| `doc.activeLayers`     | `Layer[]`             | Currently selected layers               |
| `doc.saved`            | `boolean`             | Whether doc has unsaved changes         |
| `doc.path`             | `string`              | Full file path                          |

### Methods (async — must be inside executeAsModal)

```javascript
// Save (overwrites original)
await doc.save();

// Close (optional: with/without saving)
await doc.close(constants.SaveOptions.DONOTSAVECHANGES);

// Flatten all layers
await doc.flatten();

// Merge visible layers
await doc.mergeVisibleLayers();

// Crop
await doc.crop({ left: 0, top: 0, right: 1920, bottom: 1080 });

// Resize image pixels
await doc.resizeImage(800, 600, 72, constants.ResampleMethod.BICUBIC);

// Resize canvas
await doc.resizeCanvas(1920, 1080, constants.AnchorPosition.MIDDLECENTER);

// Create a new empty pixel layer
const layer = await doc.createLayer({
    name: 'My Layer',
    opacity: 100,
    blendMode: constants.BlendMode.NORMAL,
});

// Create a layer group
const group = await doc.createLayerGroup({
    name: 'My Group',
    fromLayers: [layer1, layer2], // optional: move layers into group
});

// Duplicate the document
const copy = await doc.duplicate();
```

---

## `Layer`

Represents a layer or layer group. Key property: `layer.kind` tells you the type.

### Layer Kinds

| Constant                                                         | Description          |
| ---------------------------------------------------------------- | -------------------- |
| `constants.LayerKind.NORMAL`                                     | Regular pixel layer  |
| `constants.LayerKind.TEXT`                                       | Text layer           |
| `constants.LayerKind.SMARTOBJECT`                                | Smart Object         |
| `constants.LayerKind.SOLIDFILL` / `GRADIENTFILL` / `PATTERNFILL` | Fill layers          |
| `constants.LayerKind.BRIGHTNESSCONTRAST` (etc.)                  | Adjustment layers    |
| `constants.LayerKind.GROUP`                                      | Layer group / folder |

### Properties (synchronous)

| Property                  | Type                  | Description                              |
| ------------------------- | --------------------- | ---------------------------------------- |
| `layer.id`                | `number`              | Unique stable layer ID                   |
| `layer.name`              | `string`              | Layer name (writable)                    |
| `layer.opacity`           | `number`              | 0–100 (writable)                         |
| `layer.fillOpacity`       | `number`              | Fill opacity 0–100 (writable)            |
| `layer.blendMode`         | `constants.BlendMode` | Blend mode (writable)                    |
| `layer.kind`              | `constants.LayerKind` | Layer type (read-only)                   |
| `layer.visible`           | `boolean`             | Visibility (writable)                    |
| `layer.locked`            | `boolean`             | Fully locked (writable)                  |
| `layer.isBackgroundLayer` | `boolean`             | Is background layer                      |
| `layer.bounds`            | `Bounds`              | `{ left, top, right, bottom }` in pixels |
| `layer.parent`            | `Document\|Layer`     | Parent document or group layer           |
| `layer.layers`            | `Layer[]`             | Children (only for GROUP layers)         |
| `layer.document`          | `Document`            | Owning document                          |

### Methods (async — must be inside executeAsModal)

```javascript
// Move within layer stack
await layer.bringToFront();
await layer.bringForward();
await layer.sendToBack();
await layer.sendBackward();
await layer.moveAbove(otherLayer);
await layer.moveBelow(otherLayer);

// Transform
await layer.scale(50, 50); // scale to 50% width and height
await layer.rotate(45); // rotate 45 degrees
await layer.translate(100, -50); // move right 100px, up 50px
await layer.flip('horizontal'); // or 'vertical'

// Duplicate and delete
const copy = await layer.duplicate();
await layer.delete();

// Rasterize
await layer.rasterize(constants.RasterizeType.ENTIRELAYER);

// Apply pixel filters (on rasterized/normal layers)
await layer.applyGaussianBlur({ radius: 5 });
await layer.applyUnsharpMask({ amount: 85, radius: 1, threshold: 4 });
await layer.applyMotionBlur({ angle: 0, distance: 10 });
await layer.applyClouds();

// Smart Object operations
await layer.convertToSmartObject();
```

---

## `Action` and `ActionSet`

Photoshop's recorded macros. Actions live inside ActionSets. They're app-wide (not per-document).

```javascript
const allSets = app.actionTree; // ActionSet[]
const firstSet = allSets[0];
const actions = firstSet.actions; // Action[]

// Find and play an action by name
const myAction = actions.find((a) => a.name === 'My Action Name');
if (myAction) {
    await core.executeAsModal(
        async () => {
            await myAction.play();
        },
        { commandName: 'Play Action' },
    );
}

// ActionSet / Action methods
await actionSet.play();
await actionSet.duplicate();
await actionSet.delete();
actionSet.name = 'New Name'; // rename (synchronous property)

await action.play();
await action.duplicate();
await action.delete();
action.name = 'New Name';
```

---

## `Constants` (Enumerations)

Key enums. Access via `require('photoshop').constants`:

```javascript
const { constants } = require('photoshop');

// Blend modes
constants.BlendMode.NORMAL / MULTIPLY / SCREEN / OVERLAY;
constants.BlendMode.COLORDODGE / COLORBURN / SOFTLIGHT / HARDLIGHT;
constants.BlendMode.LUMINOSITY / HUE / SATURATION / COLOR;

// Color modes
constants.ColorMode.RGB / CMYK / GRAYSCALE / LAB;

// Save options
constants.SaveOptions.SAVECHANGES;
constants.SaveOptions.DONOTSAVECHANGES;
constants.SaveOptions.PROMPTTOSAVECHANGES;

// Resample methods
constants.ResampleMethod.BICUBIC / BILINEAR / NEARESTNEIGHBOR / PRESERVEDETAILS;

// Anchor positions (for resizeCanvas)
constants.AnchorPosition.TOPLEFT / TOPCENTER / TOPRIGHT;
constants.AnchorPosition.MIDDLELEFT / MIDDLECENTER / MIDDLERIGHT;
constants.AnchorPosition.BOTTOMLEFT / BOTTOMCENTER / BOTTOMRIGHT;
```
