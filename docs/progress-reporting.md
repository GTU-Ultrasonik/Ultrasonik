# Progress reporting

The private Actions workflow **Progress and contribution report** runs daily at 07:00 UTC and can be run manually. See the workflow run summary for module totals and per-account completed issue assignments and merged PR authorship. This is not a grading or effort measure. Assign issues and link PRs to tasks; close issues as completed only after their acceptance criteria are met. Each tracked task must have exactly one M1–M5 label. Duplicates, canceled tasks and PRs are excluded from task completion.

Public publication is disabled by default. After the team approves aggregate publication, create a fine-grained token restricted to the public website repository with Contents read/write; save it as a secret named PAGES_SYNC_TOKEN in the **private** engineering repository. Never paste the token into a chat or commit it. Run the private workflow manually with publish checked. After validating the website, set repository Actions variable PAGES_SYNC_ENABLED to true to enable daily publishing. To stop automatic publication remove or disable the variable; to revoke access revoke the token. The public website retains the last snapshot until changed or removed.

Only M1–M5 totals, completion counts and snapshot timestamp are exported. No individual contribution records are published. Unchanged totals do not produce a public commit, and the timestamp is the last published change, not the last report run.

Review counts, documentation and test evidence are not separately attributed by this initial implementation.
