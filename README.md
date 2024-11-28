



<div align="center">
  
# Kubernetes OS Project

Educational project developed for the Operating Systems course, focused on exploring Kubernetes fundamentals and container orchestration.

[Guillermo Pinto](https://github.com/guillepinto), [Miguel Pimiento](https://github.com/pimientoyolo125), [Juan D. Roa](https://github.com/JuanRoa785), [Juan D. García](https://github.com/JdgH957)

</div> 

## Overview
This repository explores Kubernetes fundamentals and container orchestration through five main objectives:
1. Research on Kubernetes container management principles
2. Documentation of deployment and administration processes
3. Kubernetes cluster implementation and configuration
4. Autoscaling evaluation and setup
5. Development of practical educational use cases

## Project Structure
```bash
.
├── docs/                    # Documentation and research
└── k8s-demo/          # Cluster setup and configuration files
```

## Getting Started
To begin working with this project, follow these steps:

1. **Set up your development environment**: 
   - Follow our comprehensive [Development Environment Setup Guide](docs/setup-guide.md)
   - This guide includes:
     - Comparing different Kubernetes tools (Minikube, Kind, K3s, Kubeadm)
     - Step-by-step Minikube and kubectl installation
     - Creating and managing your first cluster
     - Basic cluster operations

2. **Set up Horizontal Pod Autoscaler (HPA)**:  
   - Follow our detailed [HPA Demonstration Guide](docs/hpa-guide.md)
   - Key steps include:
     - Installing necessary tools and packages
     - Deploying the application on Minikube
     - Installing and configuring the Kubernetes Metrics Server
     - Applying the Horizontal Pod Autoscaler configuration
     - Generating traffic to test autoscaling

3. **Demonstration with a Full-stack Application**  
   - Dive into a practical example with our [Use Case: Deploying a Full-Stack Application with Kubernetes](docs/fullstack-demo.md).
   - This section walks you through:  
     - Deploying a backend API service and frontend client on Kubernetes.  
     - Scaling the application with both Horizontal Pod Autoscaler (HPA) for performance optimization.    

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/guillepinto/kubernetes-os/blob/main/LICENSE) file for details.

## Acknowledgments
We would like to thank the playlist [Master Kubernetes](https://www.youtube.com/playlist?list=PLrMP04WSdCjrkNYSFvFeiHrfpsSVDFMDR) made by [Pavan Elthepu](https://www.youtube.com/@PavanElthepu)
