# Phase 1: Kubernetes Deployment Demo for a Flask Application

## Overview
This project provides a hands-on demonstration of deploying a containerized Python Flask application onto a local Kubernetes cluster. Using Minikube, Docker, and kubectl, it illustrates core Kubernetes concepts for managing a web application.

The primary goal is to establish a foundational understanding of how Kubernetes resources like Deployments, Services, and ConfigMaps work together to run and expose an application, preparing for future integrations like monitoring and CI/CD.



## Key Features

- **Containerized Application:**  A Python Flask app packaged with Docker for portability and consistency.
- **Declarative Deployments:**  Manages application replicas and enables rolling updates using a Kubernetes Deployment.
- **External Configuration:**  Uses a ConfigMap to inject environment variables into the application, keeping configuration separate from code.
- **Service Discovery:**  A Kubernetes Service provides a stable internal IP and DNS name for the application pods, enabling seamless communication.
- **Health Checks:**  Implements liveness and readiness probes to ensure container health and automatic recovery of failed pods.
- **External Access:**  Uses Ingress (for Layer 7 routing) and NodePort (for Layer 4 access) to expose the application for testing and external traffic.
- **Local Cluster:**  Utilizes Minikube to simulate a complete, self-contained Kubernetes environment for local development and experimentation.



## Gettting Started

### 1. Start your local Cluster
Initialize your Minikube cluster using the Docker driver:
```bash
minikube start --driver=docker
````

### 2. Build and Load Docker Image
Build the Docker image and load it into Minikube's internal Docker registry.

```bash
cd app
docker build -t flask-app:latest .
minikube image load flask-app:latest
```

### 3. Deploy the application
Apply all the Kubernetes Manifests from the `k8resources/` directory. This will create all the resources defined below (ConfigMap, Deployment, Service, Ingress)

### 4. Verify the Deployment
Check the status of your deployment to ensure all replicas are up and running.
```bash
kubectl rollout status deployment/flask-deploy
```

To get overview of all the created resources
```bash
kubectl get all
```

<img width="1039" height="352" alt="image" src="https://github.com/user-attachments/assets/e07dc133-c1a5-4592-914d-7b327bd8c704" />



## Kubernetes Resources
This project uses several YAML manifests in the `k8resources/` directory to define the desired state of the application and its supporting components.

### configmap.yaml
**Purpose:** Decouples configuration from the application code.  
**Details:**  
    * Defines a ConfigMap resource that holds configuration data as key-value pairs (e.g., `APP_MESSAGE`, `READY_DELAY_SECONDS`).
    * These values are injected into the Flask application's containers as environment variables, allowing configuration changes without rebuilding the Docker image.

### deployment.yaml
**Purpose:** Manages the application's running instances (Pods).  
**Details:**  
    * Specifies how to run the `flask-app` Docker image, including the number of replicas, container ports, and health checks. 
    * Liveness and readiness probes ensure that Kubernetes automatically detects unhealthy containers and restarts them if needed.

### service.yaml
**Purpose:** Exposes the application pods to network traffic.  
**Details:**  
    * Provides a stable internal IP address and DNS name for the pods managed by the Deployment.  
    * The NodePort configuration allows access to the application from outside the cluster for local testing.

### ingress.yaml
**Purpose:**  Manages external access to the service, offering advanced routing and load balancing.
**Details:**  
    * Routes external HTTP/S traffic to the application based on rules (such as hostnames or paths).  
    * Requires an Ingress Controller (e.g., NGINX) to be running in the cluster.  
    * Optional for local testing but useful for production-like setups.



## Accessing the Application

**Port forwarding** is used to access the Kubernetes service from the local machine without relying on an external ingress controller.

```bash
kubectl port-forward service/flask-svc 8080:8080
```

Access the app in a browser or via curl:

```
http://localhost:8080/
http://localhost:8080/health
http://localhost:8080/ready
```
<img width="530" height="57" alt="image" src="https://github.com/user-attachments/assets/1904d43a-10ad-4c5e-821d-88dcab945df8" />
<img width="593" height="49" alt="image" src="https://github.com/user-attachments/assets/465c02f4-5545-4759-9bc4-ced012e5d5d2" />
<img width="573" height="46" alt="image" src="https://github.com/user-attachments/assets/811578eb-13e8-4e7d-8b86-c602c41e3c98" />



## Output Check

| Endpoint  | Description                    | Expected Output                         |
| --------- | ------------------------------ | --------------------------------------- |
| `/`       | Returns message from ConfigMap | `{"message":"Hello from ConfigMap"}`    |
| `/health` | Liveness check                 | `ok`                                    |
| `/ready`  | Readiness check                | `ready`                                 |



## Key Takeaways
This project demonstrates several core concepts of application management in Kubernetes:

- **Containerization:** Building a Docker image and running it within a Kubernetes Pod to ensure consistent application environments.
- **Decoupling Configuration:**  Using ConfigMaps to manage application settings externally, allowing updates without rebuilding the container image.
- **Application Resilience:**  Implementing liveness and readiness probes to maintain container health and enable zero-downtime rolling updates.
- **Service Abstraction:**  Understanding the roles of different Kubernetes objects;  
      *Deployment* defines what to run,  
      *Service* defines how to connect internally, and  
      *Ingress* defines how to expose applications externally.
- **Local Development:**  Leveraging Minikube to test, debug, and interact with a full Kubernetes cluster locally before moving to cloud-managed environments.
  


## What’s Next

* **Monitoring**: Integrate Prometheus and Grafana for metrics collection and visualization.
* **Persistent Storage**: Implement PersistentVolumes and PersistentVolumeClaims for durable log storage.
* **Automation**: Build a CI/CD pipeline using GitHub Actions or Jenkins to automate the build and deploy process.
* **Cloud Deployment**: Adapt the configuration to run on a managed Kubernetes service (e.g., GKE, EKS, or AKS).


---


# Phase 2: Monitoring Enhancement (Prometheus + Grafana)


### Objective
Extend the existing Kubernetes deployment to include real-time application and cluster-level monitoring using **Prometheus** and **Grafana**.


### New Components Added
- **Helm CLI** – installed and used to deploy the *kube-prometheus-stack* (Prometheus + Grafana).
- **ServiceMonitor** – defines how Prometheus discovers and scrapes the Flask service metrics.
- **Prometheus Client Library** – added to the Flask app to expose custom metrics under `/metrics`.
- **Grafana Dashboard** – visualizes both cluster and app-level metrics with real-time updates.



### Implementation Steps

1. **Update the application**
   - Added `prometheus_client` to `requirements.txt`.  
   - Modified `main.py` to expose a `/metrics` endpoint and a custom counter:
     ```python
     HOMEPAGE_HITS = Counter(
         "flask_homepage_requests_total",
         "Total homepage requests",
         ["method"]
     )
     ```

2. **Rebuild and redeploy the image**
   ```bash
   docker build -t flask-app:v3 .
   minikube image load flask-app:v3
   kubectl set image deployment/flask-deploy <container-name>=flask-app:v3
   kubectl rollout status deployment/flask-deploy
   ```
   
3. **Install Prometheus & Grafana via Helm**
   ```bash
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install kps prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
   ```
   
4. **Add ServiceMonitor manifest**
- k8resources/servicemonitor.yaml configures Prometheus to scrape the Flask service automatically.
- The Flask Service must have a matching label (e.g., release: kps) and a named port (http).

5. **Access dashboards**
   ```bash
   # Prometheus
   kubectl -n monitoring port-forward svc/kps-kube-prometheus-stack-prometheus 9091:9090

   # Grafana
   kubectl -n monitoring port-forward svc/kps-grafana 3000:80
   ```
   - Add a new panel → Data source = Prometheus
   - Query example: sum by (method) (rate(flask_homepage_requests_total[1m]))



### Cluster and Application-Level Metrics

Once Prometheus and Grafana were connected, both **Kubernetes cluster metrics** and **custom application metrics** became visible in the Grafana dashboards.

  - **Cluster Metrics (from kube-state-metrics):**  
     Provides real-time visibility into node CPU usage, pod restarts, memory consumption, and overall cluster health.  
     Example queries:
     ```promql
     node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
     kube_pod_status_phase
     ```
     <img width="1101" height="802" alt="pods up grafana" src="https://github.com/user-attachments/assets/f87680a8-7f25-4d6c-8137-04e98acb9b82" />

  - **Application Metrics (from Flask /metrics):**
   Captured runtime details directly from the app using the Prometheus client library.
   For example, the custom counter flask_homepage_requests_total tracks how many times users accessed the homepage.
   Example query for visualization:   
   ```promql
   sum by (method) (rate(flask_homepage_requests_total[1m]))
   ```
   <img width="1843" height="407" alt="Screenshot 2025-11-12 192912" src="https://github.com/user-attachments/assets/bb867176-571f-4d95-a27d-a074520b186b" />


Grafana dashboards were designed to visualize both cluster-wide health metrics and application-level performance data, delivering a unified observability view that connects infrastructure behavior with application activity.



### Key Takeaways

- **End-to-End Observability:** Implements a full monitoring stack using Prometheus and Grafana, providing visibility into both cluster infrastructure and application performance.
- **Custom Application Metrics:** Includes a sample Python (Flask) application instrumented to expose custom Prometheus metrics (e.g., `flask_homepage_requests_total`) via the `/metrics` endpoint.
- **Dynamic Target Discovery:** Uses a Kubernetes `ServiceMonitor` to configure Prometheus to automatically discover and scrape the application's metrics.
- **Infrastructure & App Monitoring:** Demonstrates how to monitor live Kubernetes events, such as pod scaling, restarts, and node resource utilization.
- **Custom Dashboarding:** Features a custom-built Grafana dashboard that visualizes and correlates both application-specific metrics and Kubernetes cluster metrics for deep, actionable insights.

### Architecture Overview

The following diagram summarizes the flow of the Kubernetes-based Flask application and the integrated monitoring stack using Prometheus and Grafana.

<img width="1024" height="683" alt="image" src="https://github.com/user-attachments/assets/e8d36775-e4bf-42bf-9908-9be45cfd4257" />


---

### Project Completion

With Phase 2 complete, this project now demonstrates a full DevOps lifecycle, deploying a cloud-native Flask application on Kubernetes and monitoring it in real time with Prometheus and Grafana. 
It brings together containerization, declarative infrastructure, and observability into one cohesive, production-style implementation.
