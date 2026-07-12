# python Agent exp

A starter Python development environment.

## Setup

1. Install Python 3.11+ from python.org or the Microsoft Store.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:
   - Windows PowerShell: `python -m venv venv` then `venv\Scripts\Activate.ps1`
   - Windows CMD: `python -m venv venv` then `venv\Scripts\activate.bat`
   - `py` launcher: `py -m venv venv`
4. Install development dependencies:
   - `python -m pip install --upgrade pip`
   - `python -m pip install -r requirements-dev.txt`
5. Run tests:
   - `python -m pytest`

## Project layout

- `src/main.py` - sample entrypoint
- `tests/test_main.py` - sample pytest test
- `requirements.txt` - runtime dependencies
- `requirements-dev.txt` - dev dependencies
- `.gitignore` - ignores environment and caches
- `.vscode/` - recommended VS Code settings and extensions

## Cloud deployment

This app is ready for a public cloud deployment using a platform that supports Python web apps, such as Render or Heroku.

Recommended files added:
- `Procfile` - starts the app with Gunicorn
- `runtime.txt` - pins the Python runtime

Deployment steps:
1. Push this repository to GitHub.
2. Create a new web service on Render (or your preferred cloud host).
3. Connect the GitHub repository and set the start command to:
   - `gunicorn --bind 0.0.0.0:$PORT src.main:app`
4. Deploy. The app will be available at the public URL assigned by the provider.

## Notes

If `python` is not available on your command line, install Python and add it to PATH.
If using the Windows `python.exe` alias from the Microsoft Store, ensure it is enabled in App execution aliases.
