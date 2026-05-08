# Banking Web Application - DevOps Project

## Project Overview

This project is a Banking Web Application built using Flask and deployed using DevOps practices.  
The application supports deposit, money transfer, and transaction history tracking.

## Features

- Deposit Money
- Transfer Money
- View Transaction History

## Tech Stack

- Python
- Flask
- HTML
- CSS
- Docker
- GitHub Actions
- Render

## DevOps Workflow

Developer → GitHub → GitHub Actions → Docker Build → Render Deployment → Live Application

## Project Structure

```bash
devops-flask-app/
│── app.py
│── requirements.txt
│── Dockerfile
│── templates/
│   └── index.html
│── static/
│   └── style.css
│── .github/workflows/
│   └── pipeline.yaml
```

## CI/CD Pipeline

Implemented CI pipeline using GitHub Actions for:

- Code validation
- Dependency installation
- Docker image build

## Deployment

Application deployed on Render with automatic deployment from GitHub.

## Live Project

https://banking-devops-app.onrender.com/

## GitHub Repository

https://github.com/Sunpoornarajan/devops-flask-app.git

## Key DevOps Concepts Used

- Version Control
- CI/CD
- Docker Containerization
- Cloud Deployment
- Automated Deployment
