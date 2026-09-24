<div align="center">

# `</>` Code2KT

### AI-Powered Knowledge Transfer Generator

**Turn an unfamiliar codebase into structured, developer-friendly documentation.**

Upload a project ZIP → analyze its architecture and dependencies → generate a Knowledge Transfer document.

<br>

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

<br>

![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/Jai-This-Side/Code2KT?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/Jai-This-Side/Code2KT?style=flat-square)

</div>

---

## What is Code2KT?

**Code2KT** is an AI-powered developer tool that analyzes an uploaded software project and converts the codebase into a structured **Knowledge Transfer (KT) document**.

The goal is simple:

> **Give a developer a codebase they have never seen before and quickly explain how it works.**

Instead of manually exploring hundreds of files, Code2KT performs static analysis first and uses AI when additional interpretation is required.

---

## Why Code2KT?

Understanding an unfamiliar project usually means going through:

- directory structures
- configuration files
- package manifests
- source files
- dependencies
- APIs
- database connections
- authentication logic
- deployment configuration

Code2KT automates much of this discovery process.

### The workflow

```text
                ┌────────────────────┐
                │    Project ZIP     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │  Safe Extraction   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Project Root       │
                │ Detection          │
                └─────────┬──────────┘
                          │
                          ▼
             ┌─────────────────────────────┐
             │     Static Analysis         │
             │                             │
             │ • Manifests                 │
             │ • Configurations            │
             │ • Source files               │
             │ • File structure             │
             │ • AST analysis               │
             │ • Dependencies               │
             └──────────────┬──────────────┘
                            │
                            ▼
                ┌────────────────────┐
                │ Technology & Code  │
                │ Intelligence       │
                └─────────┬──────────┘
                          │
                 ┌────────┴────────┐
                 │                 │
                 ▼                 ▼
        ┌────────────────┐  ┌─────────────────┐
        │ Enough Evidence│  │ Insufficient    │
        │                │  │ Evidence        │
        └───────┬────────┘  └────────┬────────┘
                │                    │
                │                    ▼
                │             ┌──────────────┐
                │             │ AI Fallback  │
                │             └──────┬───────┘
                │                    │
                └──────────┬─────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Knowledge Transfer  │
                 │ Document            │
                 └─────────────────────┘