This is a lightweight GUI tool powered by `gradio` for creating fractals.

## Repo Overview

- `./app.py`: main entrypoint, starting the GUI (uses main methods in the app API (see below);
- `./app_api.py`: main functions called by the GUI (uses internally the repo's API, see below);
- `./fractalito/`: main API;
- `./scripts/`: various helper scripts (usually temporary)

The app API file (`app_api.py`) should only contain the methods linked to the UI actionable elements.
The app file (`app.py`) should only contain code strictly related to the GUI (i.e. the web interface).
Everything else should go to the repo's main module (`./fractalito/`).

## Environment

The repo's virtual environment should be located at `./.venv`. Access it via `uv`.

## Expected Behaviour

- **Leave env troubleshooting to the user**: do not try to fix environment problems yourself. If something does not work and it is not due to the code that is being executed, simply report it to the user & try to provide a explanation for the root cause of the problem. Leave the fixing to the user.
- **Avoid git operations**: do not perform git operations unless explicitely asked by the user.
- **Keep it simple, stupid**: always aim for the minimal change when tasked with something. Avoid introducing logic, optimization or additional scaffolding if it is not explicitely requested by the user. Choosing to "optimize" something not directely related to the task at hand is not desirable.
- **Do not create automated tests**: this solution does not require automated testing, so refrain from introducing any.

## Typical workflow

1. Analyse user request and eventually ask for clarifications (if needed prior to analysing codebase).
2. Analyse task & codebase, and provide implementation plan.
3. Apply modifications & test correct execution. Skip testing if local env has issues.
