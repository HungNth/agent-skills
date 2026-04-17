# UXP Scripting Basics

Official docs:

- https://developer.adobe.com/photoshop/uxp/2022/scripting/
- https://developer.adobe.com/photoshop/uxp/2022/ps_reference/media/uxpscripting/

---

## What is UXP Scripting?

UXP Scripting lets you execute a single JavaScript file (`.psjs`) directly in Photoshop — no plugin manifest, no distribution, no install required. The script runs and is unloaded when complete.

Available since **Photoshop 23.5** (2022 release).

---

## File Extension

Scripts must use the `.psjs` extension:

```
my-automation.psjs
batch-resize.psjs
add-watermark.psjs
```

The file contains standard JavaScript (ES6+). No special wrapper or module format required.

---

## Running a Script

Three ways to run a `.psjs` file:

| Method            | Steps                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **File menu**     | `File > Scripts > Browse...` → select your `.psjs` file                                                                   |
| **Drag and drop** | Drag the `.psjs` onto the Photoshop icon in the Dock (Mac) or onto the Photoshop window frame (not onto an open document) |
| **Via an Action** | Record an Action step that plays a script file                                                                            |

---

## Minimal Working Script

```javascript
// hello.psjs
const { core } = require('photoshop');
await core.showAlert('Hello from UXP!');
```

That's it — no `manifest.json`, no plugin ID, no setup required.

---

## UXP Scripts vs UXP Plugins

| Feature                | Script (`.psjs`)                            | Plugin                              |
| ---------------------- | ------------------------------------------- | ----------------------------------- |
| **Lifetime**           | Runs and exits                              | Persistent (panel stays open)       |
| **UI**                 | Dialog only (modal HTML dialogs)            | Full panel UI                       |
| **Persistent storage** | ❌ No `localStorage`, no plugin data folder | ✅ Full storage access              |
| **Manifest needed**    | ❌ No                                       | ✅ Yes (`manifest.json`)            |
| **Plugin ID**          | ❌ None                                     | ✅ Required for distribution        |
| **Distribution**       | Share the `.psjs` file directly             | Creative Cloud marketplace          |
| **UXP modules**        | Limited subset                              | Full access                         |
| **Code reuse**         | Script code works in plugins                | Plugin code may not work in scripts |

---

## UXP Scripts vs ExtendScript (Legacy)

| Feature                            | UXP Script (`.psjs`)       | ExtendScript (`.jsx`)             |
| ---------------------------------- | -------------------------- | --------------------------------- |
| **JavaScript version**             | ES6+ (V8 engine)           | ES3 (very old)                    |
| **Async/await**                    | ✅ Native support          | ❌ Not supported                  |
| **Photoshop DOM**                  | `require('photoshop').app` | `app` (different object model)    |
| **Arrow functions, destructuring** | ✅                         | ❌                                |
| **batchPlay**                      | ✅                         | ❌ (used `executeAction` instead) |
| **Future support**                 | ✅ Actively developed      | ⚠️ Legacy, being phased out       |

---

## Available UXP Modules in Scripts

Scripts have a **limited subset** of UXP modules compared to plugins (the host application controls access):

| Module                   | Available in Scripts                          |
| ------------------------ | --------------------------------------------- |
| `require('photoshop')`   | ✅ Full PS API (app, action, core, constants) |
| `require('uxp').storage` | ✅ Local file system read/write               |
| `require('uxp').shell`   | ✅ Open URLs, open file paths in OS           |
| `require('uxp').network` | ⚠️ May not be available                       |
| `window.localStorage`    | ❌ Not available                              |

---

## Using the File System in Scripts

```javascript
const uxp = require('uxp');
const storage = uxp.storage;

// Let user pick a folder
const folder = await storage.localFileSystem.getFolder();

// Read a file from that folder
const file = await folder.getEntry('data.json');
const content = await file.read({ format: storage.formats.utf8 });
const data = JSON.parse(content);

// Write a file
const outFile = await folder.createFile('output.txt', { overwrite: true });
await outFile.write('Hello file!', { format: storage.formats.utf8 });
```

---

## Simple Dialog UI in Scripts

Scripts can show dialog boxes using standard HTML/DOM APIs (no panel, just modal dialogs):

```javascript
const { core } = require('photoshop');

// Built-in simple alert
await core.showAlert('Processing complete!');

// Custom HTML input dialog
function showPrompt(title, label, defaultValue = '') {
    return new Promise((resolve) => {
        const dialog = document.createElement('dialog');
        dialog.innerHTML = `
      <form method="dialog" style="padding:16px; display:flex; flex-direction:column; gap:12px;">
        <h3 style="margin:0;">${title}</h3>
        <label>${label}: <input id="val" type="text" value="${defaultValue}" /></label>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" id="cancel-btn">Cancel</button>
          <button type="submit">OK</button>
        </div>
      </form>
    `;
        dialog.querySelector('#cancel-btn').onclick = () => {
            dialog.close();
            resolve(null);
        };
        dialog.addEventListener('close', () =>
            resolve(dialog.querySelector('#val').value || null),
        );
        document.body.appendChild(dialog);
        dialog.showModal();
    });
}

const name = await showPrompt('Rename', 'New name:', 'Layer 1');
```

---

## Debugging Scripts

### UXP Developer Tool (UDT)

1. Download UDT from [Adobe Developer Distribution](https://developer.adobe.com/developer-distribution/)
2. Open UDT and connect to Photoshop
3. Go to **Scripts** tab, load your `.psjs` file
4. Use the built-in DevTools console for `console.log()`, breakpoints, and inspecting variables
5. Run the script directly from UDT for an integrated debug experience

### Quick console.log debugging

```javascript
console.log('Document:', doc.width, 'x', doc.height);
console.log(
    'Layers:',
    doc.layers.map((l) => `${l.name} (${l.kind})`),
);
```

### Enabling Developer Mode

Some features (like "Copy As JavaScript" in the Actions panel, notification listeners) require:

`Plugins > Development > Enable Developer Mode`

After enabling, debug menu items appear under `Plugins > Development`:

- **Record Action Commands...** — saves batchPlay descriptors to a file as you work
- **Record Action Notifications...** — saves commands + change notifications
- **Stop Action Recording**
