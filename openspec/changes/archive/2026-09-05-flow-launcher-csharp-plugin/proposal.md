## Why

The repo has a `flow-launcher-nodejs-plugin` skill for Flow Launcher plugin development, but nothing for C#/.NET plugins — the platform Flow Launcher itself is written in. C# plugins are the highest-performance plugin type and use a fundamentally different model (in-process .NET assemblies implementing `IPlugin`/`IAsyncPlugin`, no JSON-RPC), so the Node.js skill cannot be reused for this. A verified, source-backed C# skill is needed because the official dotnet template is stale (pins `Flow.Launcher.Plugin 4.4.0` / `net7.0-windows` while the current NuGet package is 5.3.1 targeting `net9.0-windows7.0`) and community guides contain verified-wrong patterns (e.g., using `SettingsTemplate.yaml` for C# plugins, which is a JSON-RPC-plugin-only mechanism confirmed from Flow Launcher source code).

## What Changes

- Add new skill `skills/flow-launcher-csharp-plugin/` following the existing repo skill layout (`SKILL.md` + `references/` + `evals/evals.json`), mirroring the structure of `flow-launcher-nodejs-plugin`.
- `SKILL.md`: working approach, core contract (`IPlugin`/`IAsyncPlugin`), manifest rules (`plugin.json` with `Language: "csharp"`), project shape, settings guidance (`ISettingProvider` + `LoadSettingJsonStorage<T>` — explicitly NOT `SettingsTemplate.yaml`), verification, and final-response format.
- `references/csharp-plugin-reference.md`: condensed, source-linked API reference (interfaces, `Query`, `Result`, `PluginInitContext`, `IPublicAPI`, feature interfaces `IContextMenu`/`IReloadable`/`IPluginI18n`/`IResultUpdated`/`IDisposable`), code templates, and pitfalls with evidence.
- `references/release-and-store.md`: `dotnet publish` packaging, GitHub Actions release workflow using `microsoft/setup-dotnet`, and Plugin Store manifest submission (same `Flow-Launcher/Flow.Launcher.PluginsManifest` process as other languages).
- `evals/evals.json`: 3 realistic test prompts (new plugin scaffold, bug fix, release/store prep) matching the Node.js skill's eval pattern.
- The skill is created and evaluated through the skill-creator process (draft → test prompts → review → iterate).

## Capabilities

### New Capabilities
- `flow-launcher-csharp-plugin`: Skill that guides agents to scaffold, develop, debug, package, and release Flow Launcher plugins written in C#, grounded in the official Flow Launcher documentation and verified against the current Flow Launcher source.

### Modified Capabilities

- None. Existing skills and specs are untouched.

## Non-goals

- No changes to `skills/flow-launcher-nodejs-plugin/` or any other existing skill.
- No support for F# plugins (the official docs and API cover them, but the skill targets C# per user request; the skill may note F# differences only where docs state them).
- No bundling of scripts or assets beyond reference markdown — the model generates code from templates; no `dotnet new` wrapper script is created.
- No Python/JS/JSON-RPC plugin coverage (already handled by the Node.js skill and official docs).

## Assumptions and unresolved decisions

- Target framework guidance: the skill will instruct checking the latest `Flow.Launcher.Plugin` NuGet package version (5.3.1 as of 2026-06, targeting `net9.0-windows7.0`) instead of trusting the stale template pin. Assumption: Flow Launcher app v2.1.3+ loads `net9.0-windows` assemblies; verified against the dev branch and NuGet metadata, not a live plugin install.
- Eval depth at apply time is not yet decided: tasks include the standard skill-creator loop (draft → test prompts with subagents → review); the user may shorten it during apply.
- `Plugin ID` format: official docs say "32 bit UUID"; sample manifests show both dashed-GUID and 32-hex-no-dash forms. The skill will follow the official docs wording and recommend one stable identifier generated once and never regenerated.
