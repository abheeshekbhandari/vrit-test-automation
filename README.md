# Installation

1. Clone the repo
   ```bash
   git clone https://github.com/user/vrit-test-automation.git
   cd </user/vrit-test-automation>
   ```

2. Prerequisites
   - For Python: Python 3.8+ and pip

3. Python setup (if project is Python)
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # macOS/Linux
   .venv\Scripts\activate         # Windows (PowerShell)
   pip install -r requirements.txt
   ```

4. Configuration
   - Copy example env/config and update secrets:
     ```bash
     cp .env.example .env
     # edit .env and/or config.yml with required values (API keys, endpoints, etc.)
     ```

# Running / Starting

1. Run the main automation task (Python example)
   ```bash
   # run once with a config
   python -m automation.main --config config.yml

   # dry-run example
   python -m automation.main --config config.yml --dry-run
   ```

2. Run automation tests
   ```bash
   # Python
   pytest tests/

