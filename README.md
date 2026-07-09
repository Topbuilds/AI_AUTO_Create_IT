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

## Notes

If `python` is not available on your command line, install Python and add it to PATH.
If using the Windows `python.exe` alias from the Microsoft Store, ensure it is enabled in App execution aliases.
