<div align="center">

# `</>` Code2KT

### AI-Powered Knowledge Transfer Generator

**Turn an unfamiliar codebase into structured, developer-friendly documentation.**

Upload a project ZIP, analyze its structure and dependencies, and generate a technical Knowledge Transfer document using static analysis + AI.

<br>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub_Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

<br>

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-Passing-success?style=flat-square)

</div>

---

## 📌 Overview

**Code2KT** is an AI-powered developer tool that converts software projects into structured **Knowledge Transfer (KT)** documentation.

The application accepts a project ZIP file and performs static analysis before using AI where additional interpretation is required.

Instead of manually exploring a large repository, Code2KT helps answer questions such as:

- What technologies are used?
- Where is the application entry point?
- How is the project structured?
- What are the important modules?
- How do files depend on each other?
- What APIs or routes exist?
- How is authentication handled?
- What configuration is required?
- How is the application deployed?
- What should a new developer know before working on the project?

---

# ✨ Features

## 📦 Project ZIP Upload

Upload a complete software project as a ZIP archive.

- ZIP validation
- Safe extraction
- Project root detection
- File inventory
- Directory analysis

## 🔍 Static Project Analysis

Code2KT performs deterministic analysis before relying on AI.

- Manifest detection
- Configuration detection
- Source-code signatures
- File structure analysis
- Programming language detection
- Technology detection

## 🧠 Technology Detection

Detect frameworks, libraries and development tools from actual project evidence.

Examples:

```text
Python
JavaScript
React
Vite
Terraform
GitHub Actions
Docker
```

## 🕸 Dependency Analysis

Analyze relationships between files and modules.

- Imports
- Module relationships
- Dependency resolution
- Unresolved dependencies
- Project dependency graph

## 🤖 AI-Powered KT Generation

Code2KT supports an AI provider fallback chain:

```text
Gemini
   ↓
Groq
   ↓
OpenRouter
```

If a provider temporarily fails, the next configured provider can be used.

## 📄 Markdown Output

Generated KT documentation can be:

- Viewed in the browser
- Copied
- Downloaded as a Markdown file
- Committed to a Git repository

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        User         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Code2KT Web UI    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    ZIP Service      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Project Root       │
                         │  Detector           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Project Intelligence│
                         └──────────┬──────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
      ┌────────────────┐   ┌────────────────┐   ┌─────────────────┐
      │ Technology     │   │ Code Analysis  │   │ Dependency      │
      │ Detection      │   │                │   │ Resolver        │
      └────────┬───────┘   └───────┬────────┘   └────────┬────────┘
               │                   │                     │
               └───────────────────┼─────────────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │    Project Graph    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Evidence /          │
                         │ Confidence          │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
              ┌───────────────────┐  ┌──────────────────┐
              │ Enough Evidence   │  │ Insufficient     │
              │                   │  │ Evidence         │
              └─────────┬─────────┘  └────────┬─────────┘
                        │                     │
                        │                     ▼
                        │            ┌─────────────────┐
                        │            │   AI Fallback   │
                        │            └────────┬────────┘
                        │                     │
                        └──────────┬──────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │    KT Generator     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   AI Provider Chain │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┼────────────┐
                       │            │            │
                       ▼            ▼            ▼
                    Gemini        Groq      OpenRouter
                       │            │            │
                       └────────────┼────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Knowledge Transfer  │
                         │ Markdown Document   │
                         └─────────────────────┘
```

---

# 🔄 Application Workflow

```text
1. Upload Project ZIP
        ↓
2. Safely extract the project
        ↓
3. Detect the project root
        ↓
4. Inspect manifests and configuration
        ↓
5. Detect programming languages
        ↓
6. Detect technologies
        ↓
7. Analyze source code
        ↓
8. Resolve dependencies
        ↓
9. Build project relationships
        ↓
10. Collect evidence and confidence
        ↓
11. Use AI fallback when required
        ↓
12. Generate Knowledge Transfer
        ↓
13. Display / Copy / Download
```

---

# 📑 Knowledge Transfer Output

The generated document is designed around the questions developers normally ask when joining or maintaining an unfamiliar codebase.

Typical sections include:

```text
Project Overview
Technology Stack
Architecture
Directory Structure
Application Flow
Modules
API Endpoints
Database
Authentication
Configuration
Deployment
Troubleshooting
Important Files
Classes
Functions
Dependency Relationships
Evidence / Source Files
```

The final document is generated in Markdown format.

---

# 🧠 AI Provider Architecture

## Provider Chain

```text
                 ┌───────────────┐
                 │    Gemini     │
                 │    Primary    │
                 └───────┬───────┘
                         │
                  Temporary Failure
                         │
                         ▼
                 ┌───────────────┐
                 │     Groq      │
                 │   Fallback    │
                 └───────┬───────┘
                         │
                       Failure
                         │
                         ▼
                 ┌───────────────┐
                 │  OpenRouter   │
                 │   Fallback    │
                 └───────────────┘
```

| Provider | Purpose |
|---|---|
| Gemini | Primary generation provider |
| Groq | Secondary fallback |
| OpenRouter | Final fallback |

---

# ☁️ AWS Cloud Architecture

```text
                           GitHub
                              │
                              │ Push to main
                              ▼
                   ┌──────────────────────┐
                   │    GitHub Actions    │
                   │                      │
                   │  • Install deps      │
                   │  • Run tests         │
                   │  • Docker build      │
                   │  • Push image        │
                   └──────────┬───────────┘
                              │
                             OIDC
                              │
                              ▼
                   ┌──────────────────────┐
                   │       AWS IAM        │
                   │   GitHub Actions     │
                   │        Role          │
                   └──────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │      Amazon ECR      │
                   │       code2kt        │
                   └──────────┬───────────┘
                              │
                         Docker Pull
                              │
                              ▼
                   ┌──────────────────────┐
                   │         EC2          │
                   │      Ubuntu 24.04    │
                   │                      │
                   │        Docker        │
                   │        Nginx          │
                   │        FastAPI        │
                   └──────────┬───────────┘
                              │
                              │ Runtime Secrets
                              ▼
                   ┌──────────────────────┐
                   │ AWS Secrets Manager  │
                   │                      │
                   │ code2kt/production   │
                   └──────────────────────┘
```

---

# 🔁 CI/CD Pipeline

Every push to the `main` branch triggers the deployment workflow.

```text
Git Push
   ↓
GitHub Actions
   ↓
Install Python Dependencies
   ↓
Run pytest
   ↓
Authenticate with AWS using OIDC
   ↓
Build Docker Image
   ↓
Push Image to Amazon ECR
   ↓
AWS Systems Manager
   ↓
EC2
   ↓
Pull New Image
   ↓
Stop Old Container
   ↓
Start New Container
   ↓
Run Health Check
```

## CI/CD Components

| Component | Purpose |
|---|---|
| GitHub Actions | CI/CD automation |
| GitHub OIDC | Keyless AWS authentication |
| AWS IAM | Access control |
| Amazon ECR | Docker image registry |
| AWS Systems Manager | Remote EC2 deployment |
| EC2 | Application hosting |
| Docker | Containerization |
| Nginx | Reverse proxy |

---

# 🔐 Security

Production AI credentials should never be stored directly inside the Git repository or Docker image.

## GitHub → AWS Authentication

```text
GitHub Actions
      │
      │ OIDC Token
      ▼
AWS IAM
      │
      │ AssumeRole
      ▼
Code2KT-GitHubActions-Role
```

## Application Secrets

Production credentials are stored in:

```text
AWS Secrets Manager
```

Production configuration:

```env
CODE2KT_SECRET_NAME=code2kt/production
AWS_REGION=us-west-2
```

The secret contains:

```text
GEMINI_API_KEY
GEMINI_MODEL

GROQ_API_KEY
GROQ_MODEL

OPENROUTER_API_KEY
OPENROUTER_MODEL
```

Never commit API keys or secret values to Git.

---

# 💻 Local Environment

## Prerequisites

Install:

- Python 3.12+
- Git
- pip
- Python virtual environment support
- An API key for at least one configured AI provider

---

## 1. Clone the Repository

```bash
git clone https://github.com/Jai-This-Side/Code2KT.git
cd Code2KT
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=openrouter/free
```

Do not commit `.env` to Git.

---

## 5. Start the Application

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

## 6. Open Code2KT

Open:

```text
http://127.0.0.1:8000
```

---

# 🧭 How to Use Code2KT Locally

## Step 1 — Upload a Project

Drag and drop a `.zip` project into the upload area, or click the upload area and select a ZIP file.

Example:

```text
my-project.zip
```

---

## Step 2 — Analyze the Project

Click:

```text
Analyze Project
```

Code2KT will analyze:

```text
Project Root
File Count
Directory Count
Programming Languages
Technologies
Source Files
Dependencies
Project Relationships
```

---

## Step 3 — Review Analysis

Review the detected project information displayed by the application.

---

## Step 4 — Generate Knowledge Transfer

Click:

```text
Generate Knowledge Transfer
```

Code2KT sends the project analysis through the configured AI provider chain.

---

## Step 5 — View the KT Document

The generated Knowledge Transfer Markdown document will be displayed in the application.

---

## Step 6 — Copy or Download

Use:

```text
Copy
Download
```

Example output:

```text
my-project-knowledge-transfer.md
```

---

# ☁️ Cloud Environment

The production version of Code2KT runs on AWS EC2 inside a Docker container behind Nginx.

Users do not need to install:

```text
Python
Docker
AWS CLI
Terraform
FastAPI
```

to use the deployed application.

They only need a web browser.

---

# 🌐 How to Use Code2KT in the Cloud

Open the public EC2 address:

```text
http://YOUR_EC2_PUBLIC_IP
```

Replace `YOUR_EC2_PUBLIC_IP` with the current public IP address or domain name of the deployed application.

---

## Cloud Usage Workflow

```text
Open Code2KT
      ↓
Upload ZIP
      ↓
Click Analyze Project
      ↓
Review Analysis
      ↓
Generate Knowledge Transfer
      ↓
AI Generation
      ↓
View KT Document
      ↓
Copy / Download
```

The cloud application follows the same upload → analysis → generation workflow as the local environment.

---

# 🚀 Deploying Changes to the Cloud

After making changes locally:

```bash
git add .
git commit -m "Update Code2KT"
git push origin main
```

GitHub Actions automatically:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs pytest
5. Authenticates with AWS using OIDC
6. Builds the Docker image
7. Pushes the image to Amazon ECR
8. Sends a deployment command to EC2 using AWS Systems Manager
9. Pulls the new image
10. Replaces the running container
11. Performs a health check

---

# 🐳 Docker

Docker is used to package Code2KT consistently for development and production.

## Build Image

```bash
docker build -t code2kt .
```

## Run Locally

```bash
docker run \
  --rm \
  --env-file .env \
  -p 8000:8000 \
  code2kt
```

Open:

```text
http://127.0.0.1:8000
```

---

# 🏥 Health Check

Code2KT exposes:

```http
GET /health
```

Local:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

This endpoint is also used as a basic deployment health check.

---

# 📡 API

## Upload Project

### Endpoint

```http
POST /projects/upload
```

### Example

```bash
curl -X POST \
  http://127.0.0.1:8000/projects/upload \
  -F "file=@project.zip"
```

The response contains a project ID and the static analysis result.

---

## Generate Knowledge Transfer

### Endpoint

```http
POST /projects/{project_id}/generate-knowledge-transfer
```

### Example

```bash
curl -X POST \
  http://127.0.0.1:8000/projects/PROJECT_ID/generate-knowledge-transfer
```

Replace:

```text
PROJECT_ID
```

with the ID returned by the upload endpoint.

---

# 🔎 Project Analysis Pipeline

Code2KT follows an evidence-first approach.

```text
Project
   ↓
Manifest Detection
   ↓
Configuration Detection
   ↓
Source Detection
   ↓
File Structure Detection
   ↓
Code Analysis
   ↓
Dependency Analysis
   ↓
Evidence Collection
   ↓
Confidence Assessment
   ↓
┌───────────────────────────────┐
│                               │
▼                               ▼
Enough Evidence           Not Enough Evidence
│                               │
│                               ▼
│                         AI Fallback
│                               │
└───────────────┬───────────────┘
                ↓
          KT Generation
```

---

# 📂 Project Structure

```text
Code2KT/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── projects.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── project.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── zip_service.py
│       ├── project_analyzer.py
│       ├── project_root_detector.py
│       ├── project_intelligence.py
│       ├── project_graph.py
│       ├── aws_secrets.py
│       │
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── gemini_service.py
│       │   ├── kt_generator.py
│       │   └── fallback_detector.py
│       │
│       ├── detection/
│       │   ├── __init__.py
│       │   ├── detector.py
│       │   ├── manifest_detector.py
│       │   ├── config_detector.py
│       │   ├── source_detector.py
│       │   └── file_detector.py
│       │
│       └── code_analysis/
│           ├── __init__.py
│           ├── code_analyzer.py
│           ├── python_analyzer.py
│           ├── javascript_analyzer.py
│           └── dependency_resolver.py
│
├── tests/
│   ├── test_health.py
│   ├── test_project_root_detector.py
│   └── test_zip_service.py
│
├── storage/
│   ├── uploads/
│   └── extracted/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

## Backend

- Python
- FastAPI
- Uvicorn

## Static Analysis

- Python AST
- File system analysis
- Manifest detection
- Configuration detection
- Source signatures
- Dependency resolution

## AI

- Google Gemini
- Groq
- OpenRouter

## DevOps / Cloud

- Docker
- GitHub Actions
- AWS EC2
- Amazon ECR
- AWS IAM
- AWS Systems Manager
- AWS Secrets Manager
- Terraform
- Nginx
- Linux

---

# 📊 Local vs Cloud

| Feature | Local | Cloud |
|---|---|---|
| Application | Local machine | AWS EC2 |
| URL | `127.0.0.1:8000` | Public EC2 URL |
| Python setup | Required | Not required for users |
| Docker | Optional | Used on server |
| AI credentials | `.env` | AWS Secrets Manager |
| Deployment | Manual | GitHub Actions |
| Image registry | Not required | Amazon ECR |
| AWS | Not required | Required |
| Reverse proxy | Optional | Nginx |
| Primary use | Development / Testing | Remote / Production |

---

# ⚙️ Environment Variables

## Local

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.6-flash

GROQ_API_KEY=
GROQ_MODEL=openai/gpt-oss-20b

OPENROUTER_API_KEY=
OPENROUTER_MODEL=openrouter/free
```

## Production

```env
CODE2KT_SECRET_NAME=code2kt/production
AWS_REGION=us-west-2
```

Production AI credentials are retrieved through AWS Secrets Manager.

---

# 📦 Large Uploads

The cloud application is served through Nginx.

For large project ZIP files, Nginx must allow a sufficiently large request body.

Example:

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 400M;
    client_body_timeout 300s;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

After modifying Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

# 🧪 Testing

Run the test suite:

```bash
pytest -v
```

Tests currently include:

```text
tests/
├── test_health.py
├── test_project_root_detector.py
└── test_zip_service.py
```

Tests are also executed automatically during the GitHub Actions deployment pipeline.

---

# 🔒 Git Safety

Never commit:

```text
.env
.venv/
__pycache__/
*.pyc
.pytest_cache/
storage/uploads/
storage/extracted/
```

Never commit:

```text
API keys
AWS credentials
Secrets Manager values
Private credentials
Uploaded project files
```

---

# 🗺️ Roadmap

## Completed

- [x] ZIP project upload
- [x] Safe extraction
- [x] Project root detection
- [x] File analysis
- [x] Directory analysis
- [x] Language detection
- [x] Technology detection
- [x] Static source analysis
- [x] Dependency analysis
- [x] Project graph
- [x] AI generation
- [x] Gemini fallback
- [x] Groq fallback
- [x] OpenRouter fallback
- [x] Docker containerization
- [x] Automated tests
- [x] AWS ECR deployment
- [x] EC2 deployment
- [x] GitHub Actions CI/CD
- [x] GitHub OIDC authentication
- [x] AWS Secrets Manager integration
- [x] Nginx reverse proxy

## Planned

- [ ] Persistent object storage
- [ ] Asynchronous project analysis
- [ ] Large-project optimization
- [ ] Knowledge Transfer Q&A
- [ ] More language analyzers
- [ ] Architecture visualization
- [ ] Project history
- [ ] User authentication

---

# 📸 Screenshots

Add screenshots to the repository under:

```text
docs/
└── assets/
    ├── code2kt-home.png
    ├── code2kt-analysis.png
    └── code2kt-result.png
```

Then add them to this section.

### Home

```html
<p align="center">
    <img
        src="docs/assets/code2kt-home.png"
        width="900"
        alt="Code2KT Home"
    />
</p>
```

### Analysis

```html
<p align="center">
    <img
        src="docs/assets/code2kt-analysis.png"
        width="900"
        alt="Code2KT Analysis"
    />
</p>
```

### Generated KT Document

```html
<p align="center">
    <img
        src="docs/assets/code2kt-result.png"
        width="900"
        alt="Code2KT Generated Knowledge Transfer"
    />
</p>
```

---

# 👨‍💻 Author

## Jai Singh Bisht

BCA Graduate  
DevOps & Cloud Engineering

**GitHub**

https://github.com/Jai-This-Side

**LinkedIn**

https://www.linkedin.com/in/jai-singh-bisht-b28b29289/

---

# 📜 License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

<div align="center">

### `</>` Code2KT

**Understand the codebase before touching the codebase.**

Built with Python, FastAPI, Docker and AWS.

</div>