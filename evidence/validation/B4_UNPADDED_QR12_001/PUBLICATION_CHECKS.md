# Publication checks

The designated GitHub repository was confirmed public. The staged
set contains the scoped proof, source, tests, project records and
required evidence. A scoped credential-signature scan returned no
matches.

The first local staged-diff check used `git diff --cached --check`
and treated Windows line endings in the preserved draft correction
note as trailing whitespace. Its verification assertion stopped
at `attempts/base-upper-threshold-draft/README.md:1`. That file has
ten CRLF lines and no space or tab before those endings.

The next check used
`git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff --cached --check`.
It identified only the twelve inherited blank lines at EOF in
the three byte-preserved source snapshots of budget.py, dp.py,
search.py and states.py. Each raw snapshot matched the corresponding
source file and its line-ending-normalized contents matched the
accepted parent blob. The same check excluding only those exact
snapshot files passed. The staged blob identities and raw manifest
were checked against the workspace bytes. No evidence was removed
or normalized, and no construction or audit was rerun.
