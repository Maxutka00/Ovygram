# Working rules for Ovygram

- The authorized scope includes both `/workspace/ovygram-info/plugin-distribution.md`
  and the complete SDK plan in `/workspace/ovygram-info/README.md`.
- Windows builds run only through GitHub Actions and only after the owner
  explicitly commands a build. Do not run local Windows CMake/compiler/native
  smoke builds, or dispatch a workflow merely because a change is ready.
- Linux builds do not require GitHub Actions. Do not add a Linux Actions build
  workflow as a plan requirement. No Linux build is authorized by this clarification;
  run one only on a separate explicit owner request. Python tests without
  compilation and source checks may run normally.
- Official packages require the exact literal author `Ovygram`. Case variants
  remain reserved but cannot receive `official` without a corrected file.
- Settings/data/handlers belong to installation_id. A separate plugin permission
  model is not part of the current scope; do not introduce permission grants/UI.
- Full protection of application-owned windows/tabs against arbitrary plugin
  code is deferred by the owner. Keep the future TODO in
  `docs/protected-ui-architecture.md`; do not implement process/OS isolation now.
- Registry/index URLs will be supplied at deployment. Keep them configurable;
  their absence is not an implementation blocker. Pin the generated public key
  in the client. Never commit the private signing key or put it in client files.
- Keep upstream and submodules pinned to the selected official release.
  The owner requested the update to Telegram Desktop v7.4.3 on 2026-11-13;
  preserve existing Ovygram changes while merging that release.
- Do not report full plan completion from unit-test counts. Track source
  implementation, executed tests, and pending GitHub/manual validation separately.
