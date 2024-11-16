# How to do the HPA demonstration

The following guide is based on the video you can find in the link below. Currently it has been tested in a Droplet with Linux (Ubuntu 22.04) on DigitalOcean.

https://www.youtube.com/watch?v=jyBDbm1FHiM

<details>
<summary>(Optional) Creating and connecting to a Droplet in DigitalOcean</summary>

  The GitHub Education program offers several benefits, including **$200 in credits** to explore and experiment with virtual machines on DigitalOcean (though GPU support is not available). You can apply to the program here: [GitHub Education](https://education.github.com/discount_requests/application).
  
  For a complete list of benefits: [GitHub Education Pack](https://education.github.com/pack)
  
  Once you've received the credits and accessed DigitalOcean, follow these steps to create and connect to a Droplet.
  
  ---
  
  #### **Step 1: Create a Droplet**
  
  1. Log in to your DigitalOcean account: [DigitalOcean](https://www.digitalocean.com/).
  2. Click on **Create** > **Droplets**.
  3. Configure your Droplet:
    - **Distribution:** Choose an image like Ubuntu 22.04 LTS.
    - **Plan:** Select the most basic one ($4/month or $0.007/hour).
    - **Datacenter Region:** Choose a region near you.
    - **Authentication:** Select *SSH Key* and add your public key.
      - If you don't have an SSH key, generate one by running:
        
        ```bash
          ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
        ```
        
        The public key can be found at `~/.ssh/id_rsa.pub`.
  
  4. Click on **Create Droplet** and wait for it to initialize.

---

#### **Step 2: Connect to the Droplet**

Once your Droplet is ready, note its **public IP address**.

From your terminal, use the following command:

```bash
ssh -i ~/.ssh/id_rsa root@DROPLET_IP_ADDRESS
```

- Replace `~/.ssh/id_rsa` with the path to your private key if you used a different one for the Droplet.
- Replace `DROPLET_IP_ADDRESS` with the public IP address of your Droplet.

##### If you see a host unknown warning:

Type `yes` to confirm the authenticity of the host.

---

#### **Step 3: Troubleshooting**

- If you encounter this error:
 
 ```
 WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!
 ```
 
 Run the following command to clear the old key:
 
 ```bash
 ssh-keygen -f "~/.ssh/known_hosts" -R "DROPLET_IP_ADDRESS"
 ```
 
- If you have trouble connecting, ensure that:
 - You are using the correct private key.
 - Port `22` is open (check firewall rules in DigitalOcean).

---

</details>

**Note:** All the steps are performed on a DigitalOcean Droplet. By default, the Droplet starts as root, but running Docker as root can cause several issues. Therefore, it's recommended to create a non-root user.

<details>
<summary>(Mandatory if you decided to use a Droplet or any other VM service in the cloud) Setting up a non-root user </summary>

### **Setting Up a Non-Root User and SSH**

In the following example, replace `guille` with your desired username.

#### 1. Create a Non-Root User and Configure SSH

```bash
# Create the non-root user and set the home directory
sudo adduser guille --home /home/guille --gecos "Non-root user"

# Add the user to the sudo group
sudo usermod -aG sudo guille

# Create the .ssh directory and set permissions
sudo mkdir -p /home/guille/.ssh
sudo chmod 700 /home/guille/.ssh
sudo touch /home/guille/.ssh/authorized_keys
sudo chmod 600 /home/guille/.ssh/authorized_keys
sudo chown -R guille:guille /home/guille/.ssh
```

#### 2. Configure the Public Key on the Droplet

On your **local machine**, generate SSH keys and copy the public key to the Droplet:

```bash
# Generate SSH keys
ssh-keygen -t rsa -b 4096 -C "guille@droplet" -f ~/.ssh/id_rsa_ocean

# Copy the public key to the Droplet (replace <your_droplet_ip>)
ssh-copy-id -i ~/.ssh/id_rsa_ocean.pub guille@<your_droplet_ip>
```

**If the `ssh-copy-id` command does not work properly:**

1. On your local machine, display the public key:
  
  ```bash
  cat ~/.ssh/id_rsa_ocean.pub
  ```
  
2. On the Droplet, as `root`, edit the `authorized_keys` file of the `guille` user and paste the public key:
  
  ```bash
  sudo nano /home/guille/.ssh/authorized_keys
  ```
  
Ensure the permissions are correct:

```bash
sudo chmod 700 /home/guille/.ssh
sudo chmod 600 /home/guille/.ssh/authorized_keys
sudo chown -R guille:guille /home/guille/.ssh
```

#### 3. Connect to the Droplet with the Non-Root User

Test the connection from your local machine:

```bash
ssh -i ~/.ssh/id_rsa_ocean guille@<your_droplet_ip>
```
</details>


## **Install Necessary Packages and Tools**

1. **Update Packages**
  
  ```bash
  sudo apt-get update && sudo apt-get dist-upgrade -y
  ```
  
2. **Install Java and Maven**
  
  ```bash
  sudo apt install -y openjdk-17-jdk maven
  ```
  
3. **Install Docker Engine**
  
  Follow the step-by-step instructions on the official Docker documentation: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).
  
4. **Add User to Docker Group**
  
  ```bash
  sudo usermod -aG docker guille
  # Activate the new group without logging out
  newgrp docker
  
  # Verify the installation
  docker run hello-world
  ```
  
5. **Install kubectl and Minikube**
  
  - Install `kubectl`: [Install and Set Up kubectl on Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
  - Install Minikube: [Install Minikube](https://minikube.sigs.k8s.io/docs/start/)
  
  Start Minikube:
  
  ```bash
  minikube start
  ```

## **Set Up the Project**

1. **Clone the Project Repository**
  
  ```bash
  git clone https://github.com/guillepinto/kubernetes-os.git
  cd kubernetes-os
  git checkout feat/autoscaling
  cd k8s-demo
  ```
  
2. **Build the Docker Image**
  
  ```bash
  # Build the JAR file
  mvn clean package
  
  # Build the Docker image
  docker build -t springboot-app .
  ```
  
3. **Load the Image into Minikube**
  
  ```bash
  minikube image load springboot-app
  ```
  
4. **Deploy the Application**
  
  - Apply the deployment:

    <details>
    <summary>deployment.yaml</summary>
    
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: springboot-app
    spec:
      replicas: 2  # Initial number of replicas
      selector:
        matchLabels:
          app: springboot-app
      template:
        metadata:
          labels:
            app: springboot-app
        spec:
          containers:
          - name: springboot-app
            image: springboot-app  # Name of the image created
            imagePullPolicy: IfNotPresent
            ports:
            - containerPort: 8080  # Port exposed by your application
            resources:
              requests:
                memory: "64Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "1"
    ```
    </details>
    
    ```bash
    kubectl apply -f deployment.yaml
    ```
    
5. **Expose the Application with a Service**
  
  - Apply the service:
    
    <details>
    <summary>service.yaml</summary>
      
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: springboot-service
    spec:
      type: NodePort
      selector:
        app: springboot-app
      ports:
        - protocol: TCP
          port: 80
          targetPort: 8080
    ```
    </details>
    
    ```bash
    kubectl apply -f service.yaml
    ```
    
## **Configure Autoscaling**

1. **Install Metrics Server**
  
  - Install and Apply the Metrics Server manifest:

    <details>
    <summary>metrics-server-deployment.yaml</summary>

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: metrics-server
      namespace: kube-system
    spec:
      replicas: 1
      selector:
        matchLabels:
          k8s-app: metrics-server
      template:
        metadata:
          labels:
            k8s-app: metrics-server
        spec:
          containers:
            - name: metrics-server
              image: registry.k8s.io/metrics-server/metrics-server:v0.7.2
              args:
                - --cert-dir=/tmp
                - --secure-port=10250
                - --kubelet-use-node-status-port
                - --metric-resolution=15s
                - --kubelet-preferred-address-types=InternalIP,Hostname,InternalDNS,ExternalDNS,ExternalIP
                - --kubelet-insecure-tls
              ports:
                - containerPort: 10250
                  name: https
                  protocol: TCP
              readinessProbe:
                httpGet:
                  path: /readyz
                  port: https
                  scheme: HTTPS
              livenessProbe:
                httpGet:
                  path: /livez
                  port: https
                  scheme: HTTPS
              resources:
                requests:
                  cpu: 100m
                  memory: 200Mi
          serviceAccountName: metrics-server
    ```
    </details>
    
    ```bash
    kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

    # Apply the modified metrics service to run locally
    kubectl apply -f metrics-server-deployment.yaml
    ```
    
  - Verify the installation:
    
    ```bash
    kubectl get pods -n kube-system
    ```
    
    You should see a pod named `metrics-server` in the `kube-system` namespace. After doing this, the Metrics Server should be able to collect metrics without certificate validation problems. Check again the Metrics Server status and metrics with the commands `kubectl top nodes` and `kubectl top pods`.
  
2. **Apply the HPA**
    
  - Apply the HPA:
    
    <details>
    <summary>hpa.yaml</summary>
      
    ```yaml
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: springboot-app-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: springboot-app
      minReplicas: 1  # Minimum number of replicas
      maxReplicas: 5  # Maximum number of replicas
      metrics:
        - type: Resource
          resource:
            name: cpu
            target:
              type: Utilization
              averageUtilization: 70
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 5  # Time to wait before scaling down
        scaleUp:
          stabilizationWindowSeconds: 5  # Time to wait before scaling up
    ```
    </details>

    ```bash
    kubectl apply -f hpa.yaml
    ```
  
## **Generate Traffic to Test Autoscaling**

1. **Deploy a Traffic Generator Pod**
  
  - Apply the manifest:

    <details>
    <summary>traffic-generator.yaml</summary>
      
    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: traffic-generator
    spec:
      containers:
      - name: alpine
        image: alpine
        args:
        - sleep
        - "100000000"
    ```
    </details>
    
    ```bash
    kubectl apply -f traffic-generator.yaml
    ```
    
2. **Access the Pod and Generate Traffic**
  
  ```bash
  # Access the pod
  kubectl exec -it traffic-generator -- sh
  
  # Install wrk inside the pod
  apk add wrk
  
  # Generate load (5 connections with 5 threads for 300 seconds)
  wrk -t 5 -c 5 -d 300s http://springboot-service/congruencial/lineal
  ```
  
3. **Monitor the Application**
  
  - In another terminal, watch the HPA:
    
    ```bash
    kubectl get hpa
    ```
    
  - Monitor the pods:
    
    ```bash
    kubectl top pods
    ```

---

By following these steps, you'll set up an environment to demonstrate the Horizontal Pod Autoscaler (HPA) on Kubernetes. The application will scale based on CPU utilization, and you can observe the scaling behavior by generating traffic.
