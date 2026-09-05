## Context

See proposal.md for motivation. Facts established by research (all verified against official sources on 2026-09-05):

- Repo already contains `skills/flow-launcher-nodejs-plugin/` (`SKILL.md` ~150 lines + 2 references + `evals/evals.json`) — the direct structural template for this skill.
- Flow Launcher's docs (`/docs/#/develop-dotnet-plugins`, `/docs/#/plugin.json`, API Reference, `/docs/#/testing`): C# plugins are in-process .NET assemblies implementing `IPlugin` (sync) or `IAsyncPlugin` (async, `CancellationToken`), requiring `plugin.json` with `Language: "csharp"` and `ExecuteFileName` = DLL.
- Official dotnet template (`Flow-Launcher/dotnet-template`, master): `dotnet new flow-plugin --name X --keyword kw --pluginAuthor A`, but pins `Flow.Launcher.Plugin 4.4.0` / `net7.0-windows` — stale.
- NuGet `Flow.Launcher.Plugin` latest: 5.3.1 (2026-06-08), targets `net9.0-windows7.0`. Flow app latest release: v2.1.3 (2026-06-08). Flow dev branch uses .NET 9 packages.
- **Settings trap, verified in source** (`Flow.Launcher.Core/Plugin/JsonRPCPluginBase.cs`, branch `dev`): `SettingsTemplate.yaml` is only read by `JsonRPCPluginBase` (base class for Python/JS/executable plugins). .NET plugins never hit this path. C# settings = `ISettingProvider.CreateSettingPanel()` (WPF) + `LoadSettingJsonStorage<T>()`/`SaveSettingJsonStorage<T>()`. Built-in C# plugins (e.g., Calculator) confirm: `Settings.cs` + `Views/`/`ViewModels/`, no `SettingsTemplate.yaml`.
- `Result.AsyncAction` (`Func<ActionContext, ValueTask<bool>>`) exists in source (`Flow.Launcher.Plugin/Result.cs` line 207) although the generated API docs do not list it — safe to document, with source citation.
- Debug model (docs `testing.md`): copy publish output into `%APPDATA%\FlowLauncher\Plugins\<Name>\`; .NET plugins require a Flow restart after every rebuild; duplicate plugin IDs = no plugin loads.
- Release: template's `release.ps1` = `dotnet publish -c Release -r win-x64 --no-self-contained` + `Compress-Archive`. Store submission is language-independent: PR to `Flow-Launcher/Flow.Launcher.PluginsManifest` with `UrlDownload`/`UrlSourceCode`/CDN `IcoPath`.
- Community guides (e.g., BYJRK's `flow-launcher-plugin-dev`) contain verified-wrong content: `ActionKeywords` as array (official docs: `ActionKeyword` string), "class MUST be named Main" (official requirement is only implementing `IPlugin`), pinned package 4.0.0. The skill must be grounded in official docs + source, not community copies.

## Goals / Non-Goals

**Goals:**
- A single new skill directory mirroring the existing Node.js skill's layout, so the repo stays uniform and the agent-facing contract is familiar.
- All guidance verified: every API claim traceable to official docs or Flow Launcher source; stale/contradictory guidance explicitly flagged as pitfalls.
- Progressive disclosure: SKILL.md stays lean (<~200 lines); depth lives in two reference files loaded on demand.

**Non-Goals:**
- F# coverage (may be mentioned only where official docs cover it).
- Bundled scripts/assets or a `dotnet new` wrapper — code templates live in markdown.
- Modifying any existing skill, including the Node.js one.

## Decisions

1. **Mirror the `flow-launcher-nodejs-plugin` structure** (`SKILL.md` + `references/csharp-plugin-reference.md` + `references/release-and-store.md` + `evals/evals.json`).
   - Rationale: repo convention (second skill in the same family); the Node.js skill already proved this shape works for Flow plugin tasks.
   - Rejected: a single monolithic SKILL.md — the C# API surface (`IPublicAPI` has 30+ methods, 6 feature interfaces) would blow past the ~500-line skill guideline.

2. **SKILL.md teaches the contract, references teach the API.** SKILL.md carries: trigger description (pushy, per skill-creator guidance), working approach, the two-model distinction (JSON-RPC vs in-proc), manifest rules, the settings trap, verification, final-response format. Reference 1 carries interfaces/code templates; Reference 2 carries release/store.

3. **Pin nothing; check versions.** The skill instructs checking the latest `Flow.Launcher.Plugin` on NuGet and matching `TargetFramework` to it (5.3.1 → `net9.0-windows`), explicitly warning the official template's 4.4.0/net7.0-windows pins are stale. Rationale: Flow's runtime moves (app v2.1.3, .NET 9); any pin in the skill would rot the same way the template did.

4. **Settings section leads with the trap.** "Do not create SettingsTemplate.yaml for C# plugins" with the source-level evidence, then the two C# mechanisms. Rationale: this is the most likely wrong-path migration from the Node.js skill and from SettingsTemplate-based community plugins.

5. **Verification ladder, Flow optional.** Minimum verification = `dotnet build`/`publish` + manifest sanity (works in CI/dev containers without Flow); full verification = deploy to `%APPDATA%\FlowLauncher\Plugins`, restart Flow, exercise the action keyword. Rationale: agents often run without a GUI; the docs-mandated restart step must still be stated for environments that do have Flow.

6. **Evals mirror the Node.js skill's three shapes**: new-plugin scaffold (with settings), bug fix in an existing plugin, release/store preparation. This keeps apply-time evaluation comparable across the two sibling skills.

## Risks / Trade-offs

- **API drift**: Flow Launcher evolves quickly (5.x SDK line is young). Mitigation: every reference claim carries its source URL; the skill instructs re-checking the NuGet package version rather than trusting baked-in numbers.
- **AsyncAction undocumented**: documented from source with citation; if a future SDK release changes its shape, the skill's guidance ("prefer `Action` for simple cases; `AsyncAction` for async work, verified in source") degrades safely to the documented `Action`.
- **Settings panel depth**: `ISettingProvider` panels are WPF; deep WPF/XAML guidance is out of scope. The skill covers the wiring (interface, panel creation, settings persistence) and defers XAML details to the Calculator/Explorer built-in plugins cited as references.
