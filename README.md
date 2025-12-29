# vrit-test-automation

## Quick summary
This repo contains automation tests implemented in Python using Selenium and pytest. The instructions below assume a typical development machine (macOS/Linux/Windows WSL). 

## Prerequisites
- Git
- Python 3.10 or 3.11 (3.8+ may work, but examples use 3.10+)
- pip (comes with Python)
- Google Chrome (or Firefox) browser for browser-based tests

Driver versions
- Selenium Python package: 4.8+ (install via requirements)
- Chrome and ChromeDriver: ChromeDriver must match the installed Chrome major version. Example: Chrome 116 requires ChromeDriver 116.x.

## Environment / Setup
- Python: 3.10 or 3.11
- Selenium: 4.8+
- pytest: 7.0+
- webdriver-manager: latest
- OS: macOS / Linux / Windows (WSL recommended for Windows)
- Browser: Chrome (recommended)

## Installation (step-by-step)

1. Clone your repo and enter it:
   ```bash
   git clone https://github.com/user/vrit-test-automation.git
   cd vrit-test-automation
   ```

2. Create and activate a Python virtual environment:
   macOS / Linux
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
   Windows (PowerShell)
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   - Install the packages:
     ```bash
     pip install selenium pytest webdriver-manager python-dotenv
     ```

4. Verify Python & pip:
   ```bash
   python --version
   pip --version
   ```


## Configuration / Environment variables

1. Copy the example env file and update:
   ```bash
   cp .env.example .env
   ```
   If `.env.example` is not present, create a `.env` file in the repo root.

## How to run the tests

1. Ensure `.env` is set.

2. Run all tests:
   ```bash
   python3 testdemo_abhishek.py
   ```
---
