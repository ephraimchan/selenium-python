# Selenium Grid + Jenkins Login Test Automation

A data-driven UI test suite that runs **Selenium (Python + pytest)** against a **Selenium Grid** and is orchestrated by a **Jenkins** pipeline, with everything running in Docker containers.

The tests exercise the login page of [the-internet.herokuapp.com](https://the-internet.herokuapp.com/login) using 10 different credential scenarios (valid, invalid, empty, case-sensitivity, whitespace, special characters, etc.).

---

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Test Scenarios](#test-scenarios)
- [Getting Started](#getting-started)
- [Running the Tests](#running-the-tests)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Configuration](#configuration)
- [Known Issues & Suggested Improvements](#known-issues--suggested-improvements)

---

## Project Structure

```
.
├── Dockerfile                              # Custom Jenkins image with Docker CLI
├── Jenkinsfile                             # Declarative CI pipeline
├── Login_Parameter.py                      # Test data: 10 login scenarios
├── test_grid_1_chrome_non_parallel.py      # Parametrized pytest suite (Selenium Grid)
└── verify_selenium.py                      # Local sanity check for Selenium + Chrome
```

| File | Purpose |
|------|---------|
| `Dockerfile` | Extends `jenkins/jenkins:lts`, installs the Docker CLI, adds the `jenkins` user to the `root` group, and marks all Git directories as safe. This lets Jenkins launch Docker containers as build agents. |
| `Jenkinsfile` | Runs the tests inside the `my-selenium-python:latest` container, attached to `automation-network`, and publishes JUnit results. |
| `Login_Parameter.py` | Holds `LOGIN_SCENARIOS`, a list of dictionaries (`username`, `password`, `expected`, `desc`) that drive the parametrized test. |
| `test_grid_1_chrome_non_parallel.py` | The pytest test. Connects to the Selenium Hub with `webdriver.Remote`, runs each scenario sequentially, and asserts on the flash message. |
| `verify_selenium.py` | Standalone script that launches a local Chrome via `webdriver-manager` and opens Google, to confirm your Selenium setup works before involving the Grid. |

---

## Architecture

```
┌──────────────────┐   docker run    ┌──────────────────────────┐
│  Jenkins         │ ───────────────▶│  my-selenium-python      │
│  (custom image)  │                 │  (pytest + selenium)     │
└──────────────────┘                 └────────────┬─────────────┘
                                                  │ WebDriver (HTTP :4444)
                                                  ▼
                                     ┌──────────────────────────┐
                                     │  selenium-hub            │
                                     │  + Chrome node(s)        │
                                     └────────────┬─────────────┘
                                                  │
                                                  ▼
                                     the-internet.herokuapp.com/login
```

All containers share the Docker network **`automation-network`**, which is how the test container resolves the hub by the hostname `selenium-hub`.

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (with access to the Docker socket for Jenkins)
- A Selenium Grid (hub + at least one Chrome node) reachable at `http://selenium-hub:4444`
- A Docker image named `my-selenium-python:latest` containing:
  - Python 3
  - `pytest`
  - `selenium`
- Jenkins plugins: **Pipeline**, **Docker Pipeline**, **JUnit**, **Git**
- *(Optional, for local sanity check)* Python 3, `selenium`, `webdriver-manager`, and Google Chrome

---

## Test Scenarios

Defined in `Login_Parameter.py`:

| # | Description | Username | Password | Expected |
|---|-------------|----------|----------|----------|
| 1 | Valid Login | `tomsmith` | `SuperSecretPassword!` | success |
| 2 | Invalid Username | `wronguser` | `SuperSecretPassword!` | fail |
| 3 | Invalid Password | `tomsmith` | `WrongPassword!` | fail |
| 4 | Empty Username | *(empty)* | `SuperSecretPassword!` | fail |
| 5 | Empty Password | `tomsmith` | *(empty)* | fail |
| 6 | Admin Defaults | `admin` | `admin` | fail |
| 7 | Trailing Space User | `tomsmith␣` | `SuperSecretPassword!` | fail |
| 8 | Case Sensitivity | `TOMSMITH` | `SuperSecretPassword!` | fail |
| 9 | Special Characters | `!@#$%^` | `SuperSecretPassword!` | fail |
| 10 | Leading Space Pass | `tomsmith` | `␣SuperSecretPassword!` | fail |

**Validation logic:** after clicking **Login**, the test reads the `#flash` banner.
- `success` → expects the text *"You logged into a secure area!"*
- `fail` → expects the text *"is invalid"* (e.g. "Your username is invalid!" / "Your password is invalid!")

---

## Getting Started

### 1. Create the shared Docker network

```bash
docker network create automation-network
```

### 2. Start the Selenium Grid

Example using the official Selenium images:

```bash
docker run -d --name selenium-hub \
  --network automation-network \
  -p 4444:4444 \
  selenium/hub:latest

docker run -d --name chrome-node \
  --network automation-network \
  -e SE_EVENT_BUS_HOST=selenium-hub \
  -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
  -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
  -p 7900:7900 \
  --shm-size="2g" \
  selenium/node-chrome:latest
```

Open the Grid UI at <http://localhost:4444> and watch the browser live via noVNC at <http://localhost:7900> (default password: `secret`).

### 3. Build the Jenkins image

```bash
docker build -t my-jenkins .
```

### 4. Run Jenkins

```bash
docker run -d --name jenkins \
  --network automation-network \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  my-jenkins
```

Mounting the Docker socket lets Jenkins start the `my-selenium-python` agent container.

### 5. Build the test-runner image

Create a small image (`my-selenium-python:latest`) with your Python dependencies, for example:

```dockerfile
FROM python:3.12-slim
RUN pip install --no-cache-dir pytest selenium
```

```bash
docker build -t my-selenium-python:latest .
```

> Note: this is a separate Dockerfile from the Jenkins one in this repo. Keep them in different folders or give them distinct filenames.

---

## Running the Tests

### Locally against the Grid

```bash
pip install pytest selenium
export SELENIUM_HUB_URL=http://localhost:4444
python3 -m pytest -v test_grid_1_chrome_non_parallel.py
```

> When running outside Docker, use `http://localhost:4444` instead of the default `http://selenium-hub:4444`.

### Sanity-check your local Selenium setup (no Grid)

```bash
pip install selenium webdriver-manager
python3 verify_selenium.py
```

This opens a local Chrome window, loads Google, prints the page title, and closes the browser.

### Inside the test-runner container

```bash
docker run --rm \
  --network automation-network \
  -v "$(pwd)":/app -w /app \
  my-selenium-python:latest \
  python3 -m pytest -v test_grid_1_chrome_non_parallel.py --junitxml=results.xml
```

---

## Jenkins Pipeline

The `Jenkinsfile` defines a declarative pipeline:

1. **Agent**: runs in the `my-selenium-python:latest` Docker image with `--network automation-network` so it can reach `selenium-hub`.
2. **Environment**: sets `SELENIUM_HUB_URL=http://selenium-hub:4444`.
3. **Stages**
   - **Checkout**: `checkout scm`
   - **Test**: runs `pytest -v test_grid_1_chrome_non_parallel.py --junitxml=results.xml`
4. **Post actions**
   - `always`: publishes `results.xml` via the JUnit plugin
   - `success` / `failure`: echo a status message

### Setting up the job

1. In Jenkins, create a new **Pipeline** job.
2. Under *Pipeline*, choose **Pipeline script from SCM** and point it at your repository.
3. Set the script path to `Jenkinsfile`.
4. Click **Build Now**.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SELENIUM_HUB_URL` | `http://selenium-hub:4444` | Base URL of the Selenium Grid hub. The test appends `/wd/hub`. |

Browser options set in the test fixture:

| Option | Reason |
|--------|--------|
| `--no-sandbox` | Required when Chrome runs inside a container |
| `--disable-dev-shm-usage` | Avoids crashes caused by the small default `/dev/shm` in Docker |
| `--headless` *(commented out)* | Left off so you can watch tests live through noVNC |



## License

Add your preferred license here (e.g. MIT).
