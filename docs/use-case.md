# **Use Case: Deploying a Full-Stack Application with Kubernetes**

This guide provides step-by-step instructions for setting up, deploying, and scaling a full-stack application (backend in Spring Boot and frontend in Angular) application on Kubernetes, setting up Horizontal Pod Autoscalers (HPA), and exposing the services for external access.

## Prerequisites

For a simple example with a Spring Boot application and HPA, refer to the [HPA Guide](https://github.com/guillepinto/kubernetes-os/blob/main/docs/hpa-guide.md). Ensure the necessary packages are installed as a root user. Also, adjust permissions or create a non-root user for production environments.

### Install Docker

```bash
# Update package lists
sudo apt update

# Install dependencies
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker's GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker's repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt update
sudo apt install docker-ce

# Verify installation
sudo systemctl status docker
```

### Install Minikube

```bash
# Install VirtualBox and dependencies
sudo apt install -y curl apt-transport-https virtualbox virtualbox-ext-pack

# Download Minikube binary
curl -Lo minikube https://github.com/kubernetes/minikube/releases/download/v1.30.0/minikube-linux-amd64

# Move and set permissions
sudo mv minikube /usr/local/bin/
sudo chmod +x /usr/local/bin/minikube

# Verify installation
minikube version
```

### Install kubectl

```bash
# Download kubectl binary
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

# Move and set permissions
sudo mv kubectl /usr/local/bin/
sudo chmod +x /usr/local/bin/kubectl

# Verify installation
kubectl version --client
```

### Install Git and Java

```bash
# Install Git
sudo apt install git

# Verify git
git --version

sudo apt install -y openjdk-17-jdk maven
```

## Creating Docker Images

### Backend: Spring Boot with Java 17

First, compile the backend project to generate the JAR file:

```bash
# Inside the backend project directory
mvn clean install
```

Create a `Dockerfile` for the backend:

```dockerfile
FROM openjdk:17-jdk-alpine
VOLUME /tmp
COPY target/backend-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app.jar"]
```

Build the Docker image:

```bash
docker build -t backend .
```

### Frontend: Angular Application

Create a `Dockerfile` for the frontend:

```dockerfile
FROM node:20

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 4200

CMD ["npm", "start"]
```

Build the Docker image:

```bash
docker build -t frontend .
```

## Setting Up the Kubernetes Cluster

### Starting Minikube

Start Minikube with Docker as the driver:

```bash
minikube start --driver=docker --cpus=4 --memory=6000
```

Verify Minikube status:

```bash
minikube status
```

### Building and Loading Docker Images into Minikube

Switch the Docker environment to Minikube:

```bash
eval $(minikube docker-env)
```

Build the images inside Minikube:

```bash
# Build backend image
docker build -t backend .

# Build frontend image
docker build -t frontend .
```

Switch back to the host Docker environment:

```bash
eval $(minikube docker-env -u)
```

## Deploying the Metrics Server

Check if the Metrics Server is running:

```bash
kubectl get deployment -n kube-system | grep metrics-server
kubectl get pods -n kube-system | grep metrics-server
```

If not, deploy it:

```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

Edit the Metrics Server deployment to resolve certificate issues:

```bash
kubectl edit deployment metrics-server -n kube-system
```

Add the following line under `spec.template.spec.containers.args`:

```yaml
- --kubelet-insecure-tls
```

Restart the Metrics Server:

```bash
kubectl rollout restart deployment metrics-server -n kube-system
```

_It may take a few minutes for the Metrics Server to become fully operational._

## Deploying the Backend Application

### Deployment Configuration

<details>
<summary>Create backend-deployment.yaml</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend-app
  template:
    metadata:
      labels:
        app: backend-app
    spec:
      containers:
      - name: backend-app
        image: backend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: 250m 
            memory: 512Mi 
          limits:
            cpu: 500m 
            memory: 512Mi
```
</details>

Deploy the backend:

```bash
kubectl apply -f backend-deployment.yaml
```

Verify the pods:

```bash
kubectl get pods
kubectl top pods
```

### Service Configuration

<details>
<summary>Create backend-service.yaml</summary>

```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
spec:
  type: NodePort
  selector:
    app: backend-app
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30080
```
</details>

Deploy the service:

```bash
kubectl apply -f backend-service.yaml
```

Verify the service:

```bash
kubectl get services
```

## Configuring Horizontal Pod Autoscaler for the Backend

<details>
<summary>Create backend-hpa.yaml</summary>

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend-app
  minReplicas: 2
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 5
    scaleUp:
      stabilizationWindowSeconds: 5
```
</details>

Apply the HPA:

```bash
kubectl apply -f backend-hpa.yaml
```

Check the HPA status:

```bash
kubectl get hpa
```

_Note: It may take some time for the HPA to connect with the Metrics Server and the deployment._

## Deploying the Frontend Application

### Deployment Configuration

<details>
<summary>Create frontend-deployment.yaml</summary>
  
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: frontend-app
  template:
    metadata:
      labels:
        app: frontend-app
    spec:
      containers:
      - name: frontend-app
        image: frontend:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 4200
        resources:
          requests:
            cpu: 250m 
            memory: 512Mi
          limits:
            cpu: 500m 
            memory: 1.5Gi
```
</details>

Deploy the frontend:

```bash
kubectl apply -f frontend-deployment.yaml
```

### Service Configuration

<details>
<summary>Create frontend-service.yaml</summary>
  
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  type: NodePort
  selector:
    app: frontend-app
  ports:
    - protocol: TCP
      port: 4200
      targetPort: 4200
      nodePort: 30420
```
</details>

Deploy the service:

```bash
kubectl apply -f frontend-service.yaml
```

## Configuring Horizontal Pod Autoscaler for the Frontend

<details>
<summary>Create frontend-hpa.yaml</summary>
  
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: frontend-app
  minReplicas: 1
  maxReplicas: 2
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 5
    scaleUp:
      stabilizationWindowSeconds: 5
```
</details>

Apply the HPA:

```bash
kubectl apply -f frontend-hpa.yaml
```

## Exposing Services Using UFW Firewall

Set up UFW to allow external access to the application ports:

```bash
# Allow traffic on ports 8080 and 4200
sudo ufw allow 8080/tcp
sudo ufw allow 4200/tcp

# Check UFW status
sudo ufw status
```

## Mapping Service Ports

Use `kubectl port-forward` to map the services to external ports:

```bash
# Forward frontend service
kubectl port-forward svc/frontend-service 4200:4200 --address 0.0.0.0

# Forward backend service
kubectl port-forward svc/backend-service 8080:8080 --address 0.0.0.0
```

_Note: These commands will occupy the terminal. You may need to run them in separate terminals or create background services._

---

By following this guide, you’ll deploy a full-stack application using Kubernetes. The applications are accessible externally using the server's public IP address and the specified ports. Ensure you monitor the cluster and autoscaling behaviors after deployment.
