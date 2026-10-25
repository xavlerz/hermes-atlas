# Hermes skill pack onboarding (manual; owner review required)

The repository keeps skills under `skills/` as a dedicated external skill root. No Hermes configuration is changed by this repository.

## Official behavior checked

- Skills system: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- External skill directories: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#external-skill-directories

The current official documentation says to add paths under `skills.external_dirs` in the active profile's `config.yaml`; paths can expand `~` and `${VAR}`. External skills appear in the system prompt, `skills_list`, `skill_view`, and slash commands. External directories are not write-protection boundaries: skill maintenance can edit files there. Documented precedence is project → local → create_dir → external_dirs, so same-named higher-precedence skills can shadow these. Re-check official documentation before use because configuration behavior may change.

## Recommended config diff (illustrative only; do not apply automatically)

Merge this single entry into the existing profile config's `skills.external_dirs` list; preserve all other settings and existing entries:

```yaml
skills:
  external_dirs:
    - /ABSOLUTE/PATH/TO/hermes-atlas/skills
```

Do not paste the snippet over an existing `config.yaml`, and do not configure a repo-relative path unless you have verified how your active Hermes profile resolves it. This illustrative snippet does not configure Hermes settings automatically.

## Isolated manual acceptance scenarios

Run only in a disposable Hermes profile with a temporary project fixture. Do not point a test at a production profile, server process, or a writable user repository. These scenarios assess runtime skill selection and behavior; repository unit tests and static validators do not prove activation. No scenario below was executed as part of this source-only change.

1. **Find a function:** ask for the definition of a known function. Confirm `project-navigator` is selected, returns the current path/definition and relevant direct callers, and does not modify files.
2. **Trace related files:** ask which tests and callers exercise a named component. Confirm the answer follows source references and labels any inferred dependency instead of presenting path-based guesswork as fact.
3. **Detect stale documentation:** provide a fixture where docs contradict a source-backed behavior. Ask for an audit; confirm `project-docs-maintainer` identifies the conflict with evidence and does not claim the stale prose is current behavior.
4. **Maintain docs after a source change:** change a documented behavior in a disposable fixture, then request a documentation update. Confirm the maintainer checks source and relevant tests, edits only affected docs, and distinguishes implemented behavior from proposed follow-up.
5. **Handle an incomplete index:** remove a relevant link from the fixture's project index while leaving the source file. Confirm the navigator searches the requested symbol, reports the missing/stale map, and does not treat the map as exhaustive proof.
6. **Preserve unrelated Git work:** create tracked staged and unstaged edits plus an untracked file, then ask the maintainer to review docs. Confirm it does not discard, stage, or overwrite those changes.
7. **Resolve overlapping requests:** ask once for code locations only, then separately ask to update docs for the same behavior. Confirm navigator handles lookup and defers maintenance; docs-maintainer handles the audit/update. Check `skills_list`/`skill_view` and explicit skill invocation if automatic routing is ambiguous.

Record the Hermes version, profile isolation method, prompts, selected skill, changed paths, and observed outcome when these scenarios are run. Treat results as runtime evidence for that tested version only.

## Owner-controlled connection and rollback

1. Back up the disposable profile config and inspect its current `skills` section.
2. Add only the absolute repository `skills/` path; save the file yourself.
3. Restart/reload the relevant Hermes process if required by the installation.
4. Run `skills_list`; confirm both skill names are discovered; inspect them with `skill_view` and test manual invocation.
5. Roll back by removing only this path from `skills.external_dirs`, preserving other entries, then reload Hermes. No repository files or installed skills need deletion.
6. For deeper isolation, make the skills directory read-only to the Hermes process; external-dir configuration itself does not prevent writes.

A previous owner reported successfully testing both skill packs in Hermes v0.22.2 with a test profile. That historical report was not independently rerun for this change and is not evidence of current automatic skill selection. The repository's automated checks do not provide live Hermes integration testing.
