# batchPlay Guide

Official docs: https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/batchplay/

batchPlay is the low-level API that sends action descriptor commands directly into Photoshop's event queue. Think of it as the modern replacement for ExtendScript's `executeAction`, but accepting plain JSON (called **actionJSON**) instead of custom descriptor objects.

**Only use batchPlay when a feature is NOT available in the higher-level DOM API.**

---

## Signature

```javascript
const { action, core } = require('photoshop');

// Returns Promise<Object[]> — one result per descriptor
const results = await action.batchPlay(
    descriptors, // ActionDescriptor[] — array of action commands
    options, // Object — execution options
);
```

Write operations must run inside `executeAsModal`. Read-only operations (using `_obj: "get"`) can run outside.

---

## Descriptor Structure (actionJSON)

Each descriptor is a plain JS object:

| Field      | Role                               | Example                                        |
| ---------- | ---------------------------------- | ---------------------------------------------- |
| `_obj`     | **Command name** (required)        | `"make"`, `"hide"`, `"set"`, `"get"`, `"fill"` |
| `_target`  | Target DOM element (array of refs) | See action references below                    |
| other keys | Command parameters                 | `{ name: "My Layer", opacity: 80 }`            |

### Example: Hide the active layer

```javascript
await core.executeAsModal(
    async () => {
        await action.batchPlay(
            [
                {
                    _obj: 'hide',
                    _target: [
                        {
                            _ref: 'layer',
                            _enum: 'ordinal',
                            _value: 'targetEnum',
                        },
                        {
                            _ref: 'document',
                            _enum: 'ordinal',
                            _value: 'targetEnum',
                        },
                    ],
                },
            ],
            {},
        );
    },
    { commandName: 'Hide Layer' },
);
```

### Example: Make a new empty layer

```javascript
await core.executeAsModal(
    async () => {
        await action.batchPlay(
            [
                {
                    _obj: 'make',
                    _target: [{ _ref: 'layer' }],
                },
            ],
            {},
        );
    },
    { commandName: 'Make Layer' },
);
```

---

## Action References (`_target`)

Action references are arrays that specify which DOM element to target, ordered from **most specific → least specific** (like a postal address in reverse):

```javascript
// Target the active layer in the active document:
_target: [
    { _ref: 'layer', _enum: 'ordinal', _value: 'targetEnum' }, // active layer
    { _ref: 'document', _enum: 'ordinal', _value: 'targetEnum' }, // active document
];
```

### Item reference forms

| Form        | Example                                                     | Notes                                     |
| ----------- | ----------------------------------------------------------- | ----------------------------------------- |
| By ID       | `{ _ref: "layer", _id: 42 }`                                | **Preferred** — stable throughout session |
| By index    | `{ _ref: "layer", _index: 3 }`                              | Can change if layers are added/removed    |
| By name     | `{ _ref: "layer", _name: "Background" }`                    | Fragile if names change                   |
| By ordinal  | `{ _ref: "layer", _enum: "ordinal", _value: "targetEnum" }` | Active/selected element                   |
| By property | `{ _property: "title" }`                                    | Used in "get" commands                    |

### Common ordinal `_value` options

| Value          | Meaning                             |
| -------------- | ----------------------------------- |
| `"targetEnum"` | Currently active/selected (default) |
| `"first"`      | First in list                       |
| `"last"`       | Last in list                        |
| `"front"`      | Front-most                          |

> **Best practice:** Use `_id` from `layer.id` / `doc.id` whenever available — IDs are stable and don't break when the stack order changes.

---

## Options Object

```javascript
await action.batchPlay(descriptors, {
    synchronousExecution: false, // avoid in new code
    continueOnError: false, // run all descriptors even if one fails
    immediateRedraw: false, // force Photoshop UI update after execution
});
```

| Option                 | Default | Description                                                                                        |
| ---------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| `synchronousExecution` | `false` | Blocks the JS thread until resolved. Used internally by DOM getters/setters. Avoid in custom code. |
| `continueOnError`      | `false` | When `false`, stops on first failure. When `true`, runs all and accumulates errors.                |
| `immediateRedraw`      | `false` | Forces Photoshop to redraw the UI after all descriptors finish.                                    |

---

## Result Value

Returns an array with one entry per descriptor.

### Success example

```javascript
[{ title: 'Untitled-1' }];
```

### Error example (target not found)

```javascript
[
    {
        _obj: 'error',
        message: 'The object "current document" is not currently available.',
        result: -25922,
    },
];
```

`result === 0` = no error. `result === -128` = user cancelled. Always check for `_obj === "error"` if you need robust error handling.

---

## Reading State from Photoshop (GET command)

Use `_obj: "get"` to read properties not accessible via the DOM API:

```javascript
// Get a specific property
const result = await action.batchPlay(
    [
        {
            _obj: 'get',
            _target: {
                _ref: [
                    { _property: 'title' },
                    { _ref: 'document', _id: doc.id },
                    { _ref: 'application' },
                ],
            },
        },
    ],
    {},
);
console.log(result[0].title); // "My Document.psd"
```

### Get ALL properties (development only — can be slow)

```javascript
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

## Discovering Descriptors

You often need to figure out what JSON to pass. Four techniques:

### 1. Actions Panel → "Copy As JavaScript" (easiest)

1. Enable developer mode: `Plugins > Development > Enable Developer Mode`
2. Open the Actions panel, record a new action doing exactly what you need
3. Select the action step(s), then from the panel flyout → **Copy As JavaScript**
4. The clipboard contains valid batchPlay JavaScript — paste and use directly

### 2. Notification Listener (live capture)

```javascript
// Paste in UXP Developer Tool console to log all PS events in real-time
action.addNotificationListener(['all'], (event, descriptor) => {
    console.log('Event:', event);
    console.log('Descriptor:', JSON.stringify(descriptor, null, 2));
});
```

### 3. Record Action Commands to File

1. `Plugins > Development > Record Action Commands...` → choose a destination file
2. Perform operations in the Photoshop UI normally
3. `Plugins > Development > Stop Action Recording`
4. Open the file — it contains actionJSON for every command performed

### 4. Export Actions as actionJSON

1. Select an Action Set in the Actions panel
2. Hold `Shift + Ctrl + Alt` (Win) or `Shift + Option + Cmd` (Mac)
3. Choose **Save Actions...** from the panel flyout menu
4. The saved file is in actionJSON format

---

## Common batchPlay Recipes

### Fill with foreground color

```javascript
await action.batchPlay(
    [
        {
            _obj: 'fill',
            using: { _enum: 'fillContents', _value: 'foregroundColor' },
        },
    ],
    {},
);
```

### Set foreground color via batchPlay

```javascript
await action.batchPlay(
    [
        {
            _obj: 'set',
            _target: [{ _ref: 'color', _property: 'foregroundColor' }],
            to: { _obj: 'RGBColor', red: 255, grain: 128, blue: 0 },
        },
    ],
    {},
);
```

### Apply Gaussian Blur

```javascript
await action.batchPlay(
    [
        {
            _obj: 'gaussianBlur',
            radius: { _unit: 'pixel', _value: 5.0 },
        },
    ],
    {},
);
```

### Deselect all

```javascript
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
```
