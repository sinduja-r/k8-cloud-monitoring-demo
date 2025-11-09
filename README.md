# k8-cloud-monitoring-demo

## Aim
This project demonstrates the deployment of a Flask web application on a local Kubernetes cluster using Docker and Minikube.  
The goal is to understand how containerized applications are managed using Kubernetes objects such as Deployments, Services, and ConfigMaps, while implementing health checks and configuration management.

---

## Features Used
- Containerized Python Flask application
- Kubernetes Deployment, Service, and ConfigMap
- Liveness and readiness probes for health monitoring
- NodePort service for external access
- Local Kubernetes setup using Minikube and kubectl

---

## Setup and Commands

### 1. Start Minikube
```bash
minikube start --driver=docker
````

### 2. Build and Load Docker Image

```bash
cd app
docker build -t flask-app .
minikube image load flask-app:latest
```

---

## Kubernetes Resources

### Deployment and ConfigMap

The `app-deployment.yaml` file contains:

* A **ConfigMap** that defines runtime variables (`APP_MESSAGE`, `READY_DELAY_SECONDS`).
* A **Deployment** with 3 replicas, using the ConfigMap for environment variables.
* **Liveness and readiness probes** to check container health and readiness.

### Service

The same YAML defines a **NodePort Service** to expose the application on port 8080 for external access.

Apply all Kubernetes resources:

```bash
kubectl apply -f k8s/app-deployment.yaml
kubectl rollout status deployment/flask-deploy
kubectl get all
```

---

## Port Forwarding

Port forwarding is used to access the Kubernetes service from the local machine without relying on an external ingress controller.

```bash
kubectl port-forward service/flask-svc 8080:8080
```

Access the app in a browser or via curl:

```
http://localhost:8080/
http://localhost:8080/health
http://localhost:8080/ready
```

---

## Output Check

| Endpoint  | Description                    | Expected Output                         |
| --------- | ------------------------------ | --------------------------------------- |
| `/`       | Returns message from ConfigMap | `{"message":"Hello from ConfigMap 👋"}` |
| `/health` | Liveness check                 | `ok`                                    |
| `/ready`  | Readiness check                | `ready` (after short delay)             |

---

## Learnings

* Building and running containerized applications using Docker.
* Managing configuration with Kubernetes ConfigMaps.
* Using liveness and readiness probes for application health.
* Exposing applications with NodePort services.
* Testing Kubernetes deployments locally with Minikube.

---

## Next to Implement

* Integrate Prometheus and Grafana for monitoring.
* Add PersistentVolume and PersistentVolumeClaim for log storage.
* Automate CI/CD using Jenkins or GitHub Actions.
* Extend the setup to a managed Kubernetes service (EKS/GKE/AKS).


