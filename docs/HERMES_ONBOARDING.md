# Hermes skill pack onboarding (manual; owner review required)

The repository keeps skills under `skills/` as a dedicated external skill root. No Hermes configuration has been changed.

## Official behavior checked
- Skills system: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- External skill directories section: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#external-skill-directories

The current official documentation says to add paths under `skills.external_dirs` in the active profile's `config.yaml`; paths can expand `~` and `${VAR}`. It says external skills appear in the system prompt, `skills_list`, `skill_view`, and slash commands. **Important:** external dirs are not write-protection boundaries: skill maintenance can edit files in them. Review profile/path and write permissions before connecting. Current documented precedence is project → local → create_dir → external_dirs, so same-named higher-precedence skills can shadow these. Re-check official docs before use because config behavior may change.

## Recommended config diff (illustrative only; do not apply automatically)
Merge this single entry into the existing profile config's `skills.external_dirs` list; preserve all other settings and existing entries:

```yaml
skills:
  external_dirs:
    - /ABSOLUTE/PATH/TO/hermes-atlas/skills
```

Do not paste the snippet over an existing `config.yaml`, and do not configure a repo-relative path unless you have verified how your active Hermes profile resolves it. This illustrative snippet does not configure Hermes settings automatically.

## Owner-controlled verification and rollback
1. Back up the active profile config and inspect its current `skills` section.
2. Add only the absolute repo `skills/` path; save the file yourself.
3. Restart/reload the relevant Hermes process if required by your installation.
4. Run `skills_list` and confirm `project-navigator` and `project-docs-maintainer` are discovered; inspect each with `skill_view` or invoke its slash command.
5. Roll back by removing only this path from `skills.external_dirs`, preserving other entries, then reload Hermes. No repository files or installed skills need deletion.
6. For deeper isolation, make the skills directory read-only to the Hermes process; external-dir configuration itself does not prevent writes.

The owner reports that both skill packs were successfully tested in Hermes v0.22.2 using a test profile; this result was not independently rerun for this snapshot. Connecting the skill packs remains a manual, owner-controlled configuration step. The repository's automated checks do not provide live Hermes integration testing.
