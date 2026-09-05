## 1. Skill draft (skill-creator: write the SKILL.md)

- [x] 1.1 Create `skills/flow-launcher-csharp-plugin/SKILL.md` with pushy trigger description and body sections: working approach, core contract (JSON-RPC vs in-proc distinction, `IPlugin`/`IAsyncPlugin`), manifest rules (`plugin.json` fields, `Language: "csharp"`, stable ID), settings trap (`SettingsTemplate.yaml` is JSON-RPC-only; use `ISettingProvider` + `LoadSettingJsonStorage<T>`), verification ladder, final-response format. Verify: file exists, frontmatter has `name` + `description`, body under ~200 lines, `dotnet`-free content review against spec scenarios.
- [x] 1.2 Create `skills/flow-launcher-csharp-plugin/references/csharp-plugin-reference.md`: official-docs summary with source URLs (develop-dotnet-plugins, plugin.json, API Reference pages, testing.md), code templates for `IAsyncPlugin` + `IContextMenu` + `IResultUpdated` + settings (`ISettingProvider`/JsonStorage) + i18n (`Languages/*.xaml`), Query/Result property tables, pitfalls (stale template pins, `Search` vs `RawQuery`, `AsyncAction` with source citation). Verify: every claim carries its source URL; code templates compile-plausible C#.
- [x] 1.3 Create `skills/flow-launcher-csharp-plugin/references/release-and-store.md`: `dotnet publish -c Release -r win-x64 --no-self-contained` + zip checklist, GitHub Actions workflow (setup-dotnet, read Version from plugin.json, publish zip as release), PluginsManifest entry fields with placeholder-flagging rule. Verify: zip include/exclude lists present; workflow YAML valid; manifest example lists real-URL placeholders explicitly.

## 2. Evals (skill-creator: test prompts)

- [x] 2.1 Create `skills/flow-launcher-csharp-plugin/evals/evals.json` with 3 prompts mirroring the Node.js skill shapes: (1) scaffold a new C# plugin with action keyword, async query, and settings; (2) fix an existing plugin bug (e.g., stale Result or blocking async call) preserving project shape; (3) prepare release + store manifest. Verify: JSON parses (`python -m json.tool`); prompts are realistic user-style requests.

## 3. Evaluation run (skill-creator loop; depth may be shortened by user at apply)
- [x] 3.1 Run the test prompts with the skill available (with-skill runs; baseline = no skill), saving outputs to a `flow-launcher-csharp-plugin-workspace/` sibling directory, one `eval-N/` per prompt. Verify: each run directory contains the generated plugin project outputs.
- [x] 3.2 Review outputs (eval-viewer per skill-creator, or inline summary if subagent infra is unavailable), capture user feedback, and iterate on the skill until scaffolds are correct. Verify: generated projects contain loadable plugin structure (manifest + IAsyncPlugin class + csproj + icon) and no `SettingsTemplate.yaml` for C# plugins.

## 4. Integration and final verification

- [x] 4.1 Update `README.md` custom-skills list and add the `npx skills add ... --skill flow-launcher-csharp-plugin` install block, following the existing entries' format. Verify: README renders the new skill name in the same code block pattern as `flow-launcher-nodejs-plugin`.
- [x] 4.2 Final check: `openspec validate flow-launcher-csharp-plugin` passes; skill directory contains exactly `SKILL.md`, 2 reference files, `evals/evals.json`; no other repo files modified. Verify: directory listing + git status shows only intended changes.
