================================================================================
CODE2KT
AI-Powered Knowledge Transfer Generator
================================================================================

Turn an unfamiliar codebase into structured, developer-friendly documentation.

Code2KT accepts a software project ZIP file, analyzes its structure,
technologies, source code and dependencies, and generates a technical
Knowledge Transfer (KT) document using static analysis + AI.

--------------------------------------------------------------------------------
OVERVIEW
--------------------------------------------------------------------------------

Code2KT is an AI-powered developer tool designed to help developers
understand unfamiliar software projects faster.

Instead of manually exploring a large repository, Code2KT analyzes the
codebase and generates documentation covering things such as:

- Project overview
- Technology stack
- Architecture
- Directory structure
- Application flow
- Modules
- API endpoints
- Database information
- Authentication
- Configuration
- Deployment
- Troubleshooting
- Important files
- Classes and functions
- Dependency relationships
- Evidence / source files


--------------------------------------------------------------------------------
KEY FEATURES
--------------------------------------------------------------------------------

1. PROJECT ZIP UPLOAD
   - Upload a complete software project as a ZIP archive.
   - ZIP validation
   - Safe extraction
   - Project root detection
   - File inventory
   - Directory analysis

2. STATIC PROJECT ANALYSIS
   Code2KT performs deterministic analysis before relying on AI.

   - Manifest detection
   - Configuration detection
   - Source-code signatures
   - File structure analysis
   - Programming language detection
   - Technology detection

3. TECHNOLOGY DETECTION
   Detect frameworks, libraries and development tools from project evidence.

   Examples:
   - Python
   - JavaScript
   - React
   - Vite
   - Terraform
   - GitHub Actions
   - Docker

4. DEPENDENCY ANALYSIS
   Analyze relationships between files and modules.

   - Imports
   - Module relationships
   - Dependency resolution
   - Unresolved dependencies
   - Project dependency graph

5. AI-POWERED KT GENERATION
   Code2KT supports an AI provider fallback chain:

       Gemini
          |
          v
        Groq
          |
          v
      OpenRouter

   If a provider temporarily fails, the next configured provider can be used.

6. MARKDOWN OUTPUT
   Generated KT documentation can be:
   - Viewed in the browser
   - Copied
   - Downloaded as a Markdown file
   - Committed to a Git repository


--------------------------------------------------------------------------------
ARCHITECTURE
--------------------------------------------------------------------------------

User
  |
  v
Code2KT Web UI
  |
  v
FastAPI
  |
  v
ZIP Service
  |
  v
Project Root Detector
  |
  v
Project Intelligence
  |
  +----------------------+----------------------+
  |                      |                      |
  v                      v                      v
Technology Detection   Code Analysis      Dependency Resolver
  |                      |                      |
  +----------------------+----------------------+
                         |
                         v
                   Project Graph
                         |
                         v
                Evidence / Confidence
                         |
                +--------+--------+
                |                 |
                v                 v
         Enough Evidence    Insufficient Evidence
                |                 |
                |                 v
                |            AI Fallback
                |                 |
                +--------+--------+
                         |
                         v
                    KT Generator
                         |
                         v
                   AI Provider Chain
                         |
              +----------+----------+
              |          |          |
              v          v          v
           Gemini      Groq      OpenRouter
                         |
                         v
              Knowledge Transfer Markdown


--------------------------------------------------------------------------------
APPLICATION WORKFLOW
--------------------------------------------------------------------------------

1. Upload Project ZIP
2. Safely extract the project
3. Detect the project root
4. Inspect manifests and configuration files
5. Detect programming languages and technologies
6. Analyze source code
7. Resolve dependencies
8. Build project relationships
9. Collect evidence and confidence information
10. Use AI fallback when static evidence is insufficient
11. Generate the Knowledge Transfer document
12. Display / copy / download the result


--------------------------------------------------------------------------------
KNOWLEDGE TRANSFER OUTPUT
--------------------------------------------------------------------------------

The generated document is designed around the questions developers normally
ask when joining or maintaining an unfamiliar codebase.

Typical sections:

- Project Overview
- Technology Stack
- Architecture
- Directory Structure
- Application Flow
- Modules
- API Endpoints
- Database
- Authentication
- Configuration
- Deployment
- Troubleshooting
- Important Files
- Classes
- Functions
- Dependency Relationships
- Evidence / Source Files


--------------------------------------------------------------------------------
AI PROVIDER ARCHITECTURE
--------------------------------------------------------------------------------

Primary provider:
    Gemini

Fallback providers:
    Groq
    OpenRouter

Provider flow:

    Gemini
      |
      | temporary failure
      v
    Groq
      |
      | failure
      v
    OpenRouter


--------------------------------------------------------------------------------
AWS CLOUD ARCHITECTURE
--------------------------------------------------------------------------------

                         GitHub
                            |
                            | push to main
                            v
                  +--------------------+
                  |   GitHub Actions   |
                  |                    |
                  | - Install deps     |
                  | - Run tests        |
                  | - Docker build     |
                  | - Push image       |
                  +----------+---------+
                             |
                            OIDC
                             |
                             v
                  +--------------------+
                  |       AWS IAM      |
                  +----------+---------+
                             |
                             v
                  +--------------------+
                  |    Amazon ECR      |
                  |      code2kt       |
                  +----------+---------+
                             |
                        Docker Pull
                             |
                             v
                  +--------------------+
                  |       EC2          |
                  |    Ubuntu 24.04    |
                  |                    |
                  |      Docker        |
                  |      Nginx         |
                  |      FastAPI       |
                  +----------+---------+
                             |
                             | runtime secrets
                             v
                  +--------------------+
                  | AWS Secrets        |
                  | Manager            |
                  | code2kt/production |
                  +--------------------+


--------------------------------------------------------------------------------
CI/CD PIPELINE
--------------------------------------------------------------------------------

Every push to the main branch triggers the deployment workflow.

Git Push
   |
   v
GitHub Actions
   |
   v
Install Python dependencies
   |
   v
Run pytest
   |
   v
Authenticate with AWS using OIDC
   |
   v
Build Docker image
   |
   v
Push image to Amazon ECR
   |
   v
AWS Systems Manager
   |
   v
EC2
   |
   +--> Pull new image
   +--> Stop old container
   +--> Start new container
   +--> Run health check


CI/CD components:

GitHub Actions
    CI/CD automation

GitHub OIDC
    Keyless AWS authentication

AWS IAM
    Access control

Amazon ECR
    Docker image registry

AWS Systems Manager
    Remote EC2 deployment

EC2
    Application hosting

Docker
    Containerization

Nginx
    Reverse proxy


--------------------------------------------------------------------------------
SECURITY
--------------------------------------------------------------------------------

Production AI credentials should not be stored directly inside the Git
repository or Docker image.

GITHUB TO AWS AUTHENTICATION

GitHub Actions
      |
      | OIDC token
      v
AWS IAM
      |
      | AssumeRole
      v
Code2KT-GitHubActions-Role


APPLICATION SECRETS

Production credentials are stored in AWS Secrets Manager.

Production configuration:

    CODE2KT_SECRET_NAME=code2kt/production
    AWS_REGION=us-west-2

The production secret contains:

    GEMINI_API_KEY
    GEMINI_MODEL

    GROQ_API_KEY
    GROQ_MODEL

    OPENROUTER_API_KEY
    OPENROUTER_MODEL

Never commit API keys or secret values to Git.


================================================================================
HOW TO USE CODE2KT
================================================================================

Code2KT can be used in two ways:

1. Local Environment
2. Cloud Environment


################################################################################
1. LOCAL ENVIRONMENT
################################################################################

PREREQUISITES
-------------

Install:

- Python 3.12+
- Git
- pip
- virtual environment support
- An AI provider API key


STEP 1 - CLONE THE REPOSITORY
----------------------------

    git clone https://github.com/Jai-This-Side/Code2KT.git
    cd Code2KT


STEP 2 - CREATE A VIRTUAL ENVIRONMENT
-------------------------------------

Linux / macOS:

    python3 -m venv .venv
    source .venv/bin/activate

Windows:

    python -m venv .venv
    .venv\Scripts\activate


STEP 3 - INSTALL DEPENDENCIES
-----------------------------

    pip install -r requirements.txt


STEP 4 - CONFIGURE ENVIRONMENT VARIABLES
-----------------------------------------

Create a file named:

    .env

Example:

    GEMINI_API_KEY=your_gemini_api_key
    GEMINI_MODEL=gemini-3.6-flash

    GROQ_API_KEY=your_groq_api_key
    GROQ_MODEL=openai/gpt-oss-20b

    OPENROUTER_API_KEY=your_openrouter_api_key
    OPENROUTER_MODEL=openrouter/free

Do not commit .env to Git.


STEP 5 - START THE APPLICATION
------------------------------

    uvicorn app.main:app --reload

The application will run at:

    http://127.0.0.1:8000


STEP 6 - OPEN THE APPLICATION
-----------------------------

Open the following address in a browser:

    http://127.0.0.1:8000


--------------------------------------------------------------------------------
LOCAL USAGE WORKFLOW
--------------------------------------------------------------------------------

STEP 1 - Upload a Project

Drag and drop a .zip project into the upload area, or browse for a ZIP file.

Example:

    my-project.zip


STEP 2 - Analyze the Project

Click:

    Analyze Project

Code2KT will analyze:

    Project root
    File count
    Directory count
    Programming languages
    Technologies
    Source files
    Dependencies
    Project relationships


STEP 3 - Review Analysis

Review the detected project information in the analysis screen.


STEP 4 - Generate Knowledge Transfer

Click:

    Generate Knowledge Transfer

The configured AI provider chain generates the documentation.


STEP 5 - View the KT Document

The generated Markdown document will be displayed in the application.


STEP 6 - Copy or Download

Use:

    Copy
    Download

Example output file:

    my-project-knowledge-transfer.md


################################################################################
2. CLOUD ENVIRONMENT
################################################################################

The production version of Code2KT runs on AWS EC2 inside a Docker container
behind Nginx.

Users do not need Python, Docker, AWS CLI, Terraform or the source repository
to use the deployed cloud application.

They only need a web browser.


--------------------------------------------------------------------------------
CLOUD USAGE
--------------------------------------------------------------------------------

Open the public EC2 address:

    http://YOUR_EC2_PUBLIC_IP

Replace YOUR_EC2_PUBLIC_IP with the current public IP or domain of the
deployed application.


CLOUD WORKFLOW
--------------

    Open Code2KT
         |
         v
    Upload ZIP
         |
         v
    Click Analyze Project
         |
         v
    Review Analysis
         |
         v
    Generate Knowledge Transfer
         |
         v
    AI Generation
         |
         v
    View KT Document
         |
         v
    Copy / Download


--------------------------------------------------------------------------------
DEPLOYING CHANGES TO THE CLOUD
--------------------------------------------------------------------------------

After modifying the project locally:

    git add .
    git commit -m "Update Code2KT"
    git push origin main

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


--------------------------------------------------------------------------------
DOCKER
--------------------------------------------------------------------------------

Docker is used to package Code2KT consistently for development and production.


BUILD IMAGE
-----------

    docker build -t code2kt .


RUN LOCALLY
-----------

    docker run \
      --rm \
      --env-file .env \
      -p 8000:8000 \
      code2kt

Open:

    http://127.0.0.1:8000


--------------------------------------------------------------------------------
HEALTH CHECK
--------------------------------------------------------------------------------

Code2KT exposes:

    GET /health

Local:

    curl http://127.0.0.1:8000/health

Expected response:

    {
      "status": "healthy"
    }

This endpoint is also used as a basic deployment health check.


--------------------------------------------------------------------------------
API
--------------------------------------------------------------------------------

UPLOAD PROJECT
--------------

Endpoint:

    POST /projects/upload

Example:

    curl -X POST \
      http://127.0.0.1:8000/projects/upload \
      -F "file=@project.zip"

The response contains a project ID and analysis result.


GENERATE KNOWLEDGE TRANSFER
---------------------------

Endpoint:

    POST /projects/{project_id}/generate-knowledge-transfer

Example:

    curl -X POST \
      http://127.0.0.1:8000/projects/PROJECT_ID/generate-knowledge-transfer

Replace PROJECT_ID with the ID returned by the upload endpoint.


--------------------------------------------------------------------------------
PROJECT ANALYSIS PIPELINE
--------------------------------------------------------------------------------

Code2KT follows an evidence-first approach.

    Project
       |
       v
    Manifest Detection
       |
       v
    Configuration Detection
       |
       v
    Source Detection
       |
       v
    File Structure Detection
       |
       v
    Code Analysis
       |
       v
    Dependency Analysis
       |
       v
    Evidence Collection
       |
       v
    Confidence Assessment
       |
       +-----------------------------+
       |                             |
       v                             v
    Enough Evidence             Not Enough Evidence
       |                             |
       |                             v
       |                        AI Fallback
       |                             |
       +-------------+---------------+
                     |
                     v
                KT Generation


--------------------------------------------------------------------------------
PROJECT STRUCTURE
--------------------------------------------------------------------------------

Code2KT/
|
├── app/
│   ├── __init__.py
│   ├── main.py
│   |
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── projects.py
│   |
│   ├── models/
│   │   ├── __init__.py
│   │   └── project.py
│   |
│   └── services/
│       ├── __init__.py
│       ├── zip_service.py
│       ├── project_analyzer.py
│       ├── project_root_detector.py
│       ├── project_intelligence.py
│       ├── project_graph.py
│       ├── aws_secrets.py
│       |
│       ├── ai/
│       │   ├── __init__.py
│       │   ├── gemini_service.py
│       │   ├── kt_generator.py
│       │   └── fallback_detector.py
│       |
│       ├── detection/
│       │   ├── __init__.py
│       │   ├── detector.py
│       │   ├── manifest_detector.py
│       │   ├── config_detector.py
│       │   ├── source_detector.py
│       │   └── file_detector.py
│       |
│       └── code_analysis/
│           ├── __init__.py
│           ├── code_analyzer.py
│           ├── python_analyzer.py
│           ├── javascript_analyzer.py
│           └── dependency_resolver.py
|
├── tests/
│   ├── test_health.py
│   ├── test_project_root_detector.py
│   └── test_zip_service.py
|
├── storage/
│   ├── uploads/
│   └── extracted/
|
├── .github/
│   └── workflows/
│       └── deploy.yml
|
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md


--------------------------------------------------------------------------------
TECHNOLOGY STACK
--------------------------------------------------------------------------------

BACKEND
-------

- Python
- FastAPI
- Uvicorn


STATIC ANALYSIS
---------------

- Python AST
- File system analysis
- Manifest detection
- Configuration detection
- Source signatures
- Dependency resolution


AI
--

- Google Gemini
- Groq
- OpenRouter


DEVOPS / CLOUD
--------------

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


--------------------------------------------------------------------------------
LOCAL VS CLOUD
--------------------------------------------------------------------------------

Feature                  Local                    Cloud
---------------------------------------------------------------------------
Application              Local machine            AWS EC2
URL                      127.0.0.1:8000           Public EC2 URL
Python setup             Required                 Not required for users
Docker                   Optional                 Used on server
AI credentials           .env                     AWS Secrets Manager
Deployment               Manual                   GitHub Actions
Image registry           Not required             Amazon ECR
AWS                      Not required             Required
Reverse proxy            Optional                 Nginx
Primary use              Development/testing      Remote/production usage


--------------------------------------------------------------------------------
ENVIRONMENT VARIABLES
--------------------------------------------------------------------------------

LOCAL
-----

    GEMINI_API_KEY=
    GEMINI_MODEL=gemini-3.6-flash

    GROQ_API_KEY=
    GROQ_MODEL=openai/gpt-oss-20b

    OPENROUTER_API_KEY=
    OPENROUTER_MODEL=openrouter/free


PRODUCTION
----------

    CODE2KT_SECRET_NAME=code2kt/production
    AWS_REGION=us-west-2


--------------------------------------------------------------------------------
LARGE UPLOADS
--------------------------------------------------------------------------------

The cloud application is served through Nginx.

For large project ZIP files, Nginx must allow a sufficiently large request
body.

Example:

    client_max_body_size 400M;
    client_body_timeout 300s;

After modifying Nginx:

    sudo nginx -t
    sudo systemctl reload nginx


--------------------------------------------------------------------------------
TESTING
--------------------------------------------------------------------------------

Run the test suite:

    pytest -v

Tests currently include:

    tests/
    ├── test_health.py
    ├── test_project_root_detector.py
    └── test_zip_service.py

Tests also run automatically during the GitHub Actions deployment pipeline.


--------------------------------------------------------------------------------
GIT SAFETY
--------------------------------------------------------------------------------

Never commit:

    .env
    .venv/
    __pycache__/
    *.pyc
    .pytest_cache/
    storage/uploads/
    storage/extracted/

Never commit:

    API keys
    AWS credentials
    Secrets Manager values
    private credentials
    uploaded project files


--------------------------------------------------------------------------------
ROADMAP
--------------------------------------------------------------------------------

COMPLETED

[x] ZIP project upload
[x] Safe extraction
[x] Project root detection
[x] File analysis
[x] Directory analysis
[x] Language detection
[x] Technology detection
[x] Static source analysis
[x] Dependency analysis
[x] Project graph
[x] AI generation
[x] Gemini fallback
[x] Groq fallback
[x] OpenRouter fallback
[x] Docker containerization
[x] Automated tests
[x] AWS ECR deployment
[x] EC2 deployment
[x] GitHub Actions CI/CD
[x] GitHub OIDC authentication
[x] AWS Secrets Manager integration
[x] Nginx reverse proxy


PLANNED

[ ] Persistent object storage
[ ] Asynchronous project analysis
[ ] Large-project optimization
[ ] Knowledge Transfer Q&A
[ ] More language analyzers
[ ] Architecture visualization
[ ] Project history
[ ] User authentication


--------------------------------------------------------------------------------
AUTHOR
--------------------------------------------------------------------------------

Jai Singh Bisht

BCA Undergraduate
DevOps & Cloud Engineering

GitHub:
https://github.com/Jai-This-Side

LinkedIn:
https://www.linkedin.com/in/jai-singh-bisht-b28b29289/


--------------------------------------------------------------------------------
LICENSE
--------------------------------------------------------------------------------

This project is licensed under the MIT License.

See the LICENSE file for details.


================================================================================
CODE2KT
Understand the codebase before touching the codebase.
================================================================================
