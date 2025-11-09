# Kubernetes Deployment Demo for a Flask Application

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


