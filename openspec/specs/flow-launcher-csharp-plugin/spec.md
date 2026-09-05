# Flow Launcher C# Plugin Skill Specification

## Purpose

Defines the observable behavior of the `flow-launcher-csharp-plugin` skill: what an agent invoking the skill must produce for scaffolding new C# Flow Launcher plugins, modifying existing ones, fixing bugs, and preparing releases/store submissions.

## Requirements

### Requirement: Skill triggers on Flow Launcher C# plugin work
The skill SHALL trigger whenever a user asks to create, modify, debug, package, or publish a Flow Launcher plugin written in C#, or asks about Flow Launcher plugin concepts (`plugin.json`, `ActionKeyword`, `IPlugin`, `IAsyncPlugin`, the `Flow.Launcher.Plugin` NuGet package), even when the user only says "flow plugin" without naming the language.

#### Scenario: User asks for a new plugin without naming the language
- **WHEN** the user asks "create a Flow Launcher plugin that searches GitHub issues" without specifying a language
- **THEN** the skill is considered triggered and the agent either follows the C# guidance or explicitly confirms the language choice with the user

#### Scenario: User asks about a Node.js Flow plugin
- **WHEN** the user's request is clearly about a JSON-RPC/Node.js Flow plugin (e.g., mentions `main.js`, `console.log` in results)
- **THEN** the skill does not misdirect the agent into C# guidance; the agent uses the appropriate Node.js skill or general docs

### Requirement: Scaffolding produces a loadable plugin structure
When asked to create a new C# plugin, the skill SHALL guide the agent to produce a project containing, at minimum:

1. A `plugin.json` manifest in the plugin root with fields `ID`, `ActionKeyword`, `Name`, `Description`, `Author`, `Version`, `Language` (`"csharp"`), `Website`, `IcoPath`, and `ExecuteFileName` pointing to the built DLL.
2. A .NET class library project that references the `Flow.Launcher.Plugin` NuGet package and contains a class implementing `IPlugin` or `IAsyncPlugin`.
3. An icon file matching `IcoPath`.

#### Scenario: Scaffold via official template
- **WHEN** the agent scaffolds with the official dotnet template (`dotnet new install Flow.Launcher.Plugin.Template` + `dotnet new flow-plugin ...`)
- **THEN** the generated project is corrected for stale pins if needed: the `Flow.Launcher.Plugin` package version and `TargetFramework` are checked against the latest NuGet package metadata before building

#### Scenario: Manifest correctness
- **WHEN** the skill produces or edits `plugin.json`
- **THEN** `Language` is `"csharp"`, `ExecuteFileName` names the plugin's built DLL, `ActionKeyword` is non-empty (or `"*"` only for deliberate global-search plugins), and the plugin `ID` is a stable identifier generated once and never regenerated for an existing plugin

### Requirement: Query handling follows the async-first pattern
For new plugin code, the skill SHALL prefer `IAsyncPlugin` (`InitAsync` + `QueryAsync` with `CancellationToken`) over synchronous `IPlugin`, and SHALL produce `Result` objects whose `Action` (or `AsyncAction`) delegate returns `true` to hide the Flow window or `false` to keep it open, with every result carrying a `Title` and an `IcoPath`.

#### Scenario: Expensive initialization
- **WHEN** the plugin needs to load caches, indexes, or perform I/O at startup
- **THEN** the work is placed in `Init`/`InitAsync` (which runs in parallel with other plugins) rather than the object constructor

#### Scenario: Cancellation awareness
- **WHEN** a query performs network or long-running work
- **THEN** the generated `QueryAsync` respects the provided `CancellationToken` (e.g., passes it to async calls or checks `IsCancellationRequested`)

### Requirement: Settings guidance is C#-correct
The skill SHALL state that `SettingsTemplate.yaml` is a JSON-RPC-plugin mechanism (Python/JS/executable) and is not loaded for .NET plugins, and SHALL guide C# settings via the plugin API's JSON settings storage (`LoadSettingJsonStorage<T>()` / `SaveSettingJsonStorage<T>()`) and/or a custom settings panel through `ISettingProvider`.

#### Scenario: User asks for plugin settings
- **WHEN** the user asks the agent to add user-configurable settings to a C# Flow plugin
- **THEN** the agent does not create a `SettingsTemplate.yaml` for the C# plugin and instead uses the C#-correct settings mechanism

### Requirement: Debug and verification guidance matches Flow's behavior
The skill SHALL instruct that after building, the publish output is copied to Flow Launcher's `Plugins` directory and Flow must be restarted for .NET plugins (unlike Python/JS plugins which hot-reload), and SHALL warn that duplicate plugin IDs cause no plugin to load.

#### Scenario: Agent verifies a plugin locally
- **WHEN** the agent finishes a change and needs to verify it in Flow Launcher
- **THEN** the agent can describe or perform: build/publish, copy output to the plugins folder (`userdata` command locates it), restart Flow Launcher, and exercise the action keyword

#### Scenario: Build without Flow installed
- **WHEN** Flow Launcher is not available in the environment
- **THEN** the skill's minimum verification is a successful `dotnet build`/`dotnet publish` of the plugin project plus manifest sanity checks (required fields present, `ExecuteFileName` matches built DLL)

### Requirement: Release guidance produces store-ready artifacts
When asked to release or submit, the skill SHALL guide producing a zip from `dotnet publish` output containing `plugin.json`, the DLL with all dependency assemblies, icons, and language files; a GitHub Actions workflow using the .NET SDK setup and reading `Version` from `plugin.json`; and a Plugin Store manifest entry (`Flow-Launcher/Flow.Launcher.PluginsManifest`) with `UrlDownload`, `UrlSourceCode`, and a CDN-accessible `IcoPath`.

#### Scenario: Release zip contents
- **WHEN** the agent packages a release
- **THEN** the zip does not include `.git`, source-only clutter, or local caches, and does include everything Flow needs to load the plugin at runtime

#### Scenario: Store manifest placeholders
- **WHEN** the agent prepares a manifest entry without real repository URLs
- **THEN** the agent explicitly lists which fields need real values instead of fabricating URLs

### Requirement: Reference material is sourced
The skill's reference files SHALL cite the official Flow Launcher documentation URLs (develop-dotnet-plugins, plugin.json, API Reference, testing) and repositories (dotnet-template, plugin-samples) they summarize, so an agent can re-verify any claim.

#### Scenario: Agent needs a deeper API detail
- **WHEN** the skill's condensed reference does not cover an API question (e.g., an uncommon `Result` property)
- **THEN** the reference file points to the specific official docs page where the detail can be checked
