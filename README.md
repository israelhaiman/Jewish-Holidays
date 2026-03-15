# Jewish Holidays API

## Overview

This project implements a Python-based web service that retrieves Jewish holiday data for the upcoming quarter using the public Hebcal API and exposes it through a JSON HTTP endpoint.

The application is containerized with Docker and deployed to Kubernetes using Infrastructure as Code with **Pulumi**.

The project demonstrates a full DevOps workflow including containerization, Kubernetes deployment, ingress exposure, configuration management, and secret handling.

---

## Architecture

```bash
Client
│
▼
Ingress (NGINX)
│
▼
Kubernetes Service
│
▼
Pod (Python API Container)
│
▼
Hebcal Public API
```


Holiday data source:  
[Hebcal REST API](https://www.hebcal.com/home/195/jewish-calendar-rest-api)

---

## Project Structure
```bash
holidays-project
│
├── app/
│ ├── app.py
│ └── requirements.txt
│
├── Dockerfile
│
├── k8s/
│ ├── deployment.yaml
│ ├── service.yaml
│ └── ingress.yaml
│
├── infra/
│ ├── main.py
│ ├── Pulumi.yaml
│ └── requirements.txt
│
└── README.md
```

## Requirements

- Docker
- Kubernetes cluster (Minikube or managed cluster)
- Pulumi
- Python 3.9+

---

## Build the Application

Build the container image:

```bash
docker build -t holidays-api:1.0 .
cd infra
pulumi up
```
Pulumi will provision:

- Kubernetes Deployment
- Kubernetes Service
- Kubernetes Ingress

## Accessing the Application

The service is exposed via Kubernetes Ingress.

Example endpoint: http://holidays.local/holidays

```bash
curl http://holidays.local/holidays
```
Example response:

```json
{
  "holidays": [
    {
      "name": "Rosh Hashanah",
      "date": "2026-09-12"
    }
  ]
}
```
## Validation

Verify deployment:

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
pulumi stack output
```








