The move from single-document extraction to cross-document synthesis. The fact that deviation is bidirectional — the script found favourable deviations in Agreement A as well as unfavourable ones in Agreement B. The equity cure flag as an example of the model holding two concepts in relation rather than pattern matching against a single threshold. And the max_tokens lesson — a truncated response produces a JSON parse error, not a graceful failure. That is a production consideration.

--------

Here is the full sequence for today:

Session startup
Navigated to Lab root from a fresh PowerShell session. Activated the virtual environment. Ran git status to confirm clean state. Committed and pushed the Day 1 and Day 2 lab notes that had been touched since the last session.

Day 3 setup
Navigated into day03. Copied .env from day01. Confirmed directory contents before building.

File creation
Created credit_agreement_apex.txt — a clean unitranche with standard covenant terms. Created credit_agreement_harrier.txt via Set-Content after a VS Code paste failure left the file missing. Created covenant_compare.py with an internal standard dictionary, a multi-document prompt, JSON output parsing and a file writer for covenant_comparison.json.

Debugging
First run failed with FileNotFoundError — Harrier agreement not saved. Recreated via terminal. Second run failed with JSONDecodeError — response truncated at 2048 tokens. Increased max_tokens to 4096. Third run succeeded.

Output
Six HIGH severity deviations flagged in Agreement B. Two LOW severity favourable deviations identified in Agreement A. Summary produced with a clear credit committee disposition. Output written to covenant_comparison.json.

VS Code workspace
Added day03 to the workspace via File → Add Folder to Workspace. Saved workspace file.

Git
Committed Day 3 files and pushed. Caught .env committed again — removed from tracking with git rm --cached, committed the fix and pushed.

Pending
Day 3 lab_notes.txt to be written and committed before Day 4.