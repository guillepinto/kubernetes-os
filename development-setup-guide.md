# Development Environment Setup Guide

The following guide is based on the video you can find in the link below. Currently it has been tested on Linux (Ubuntu 22.04) and (in the video) macOS.

[https://www.youtube.com/watch?v=dSOS-7SZ_BA&list=PLrMP04WSdCjrkNYSFvFeiHrfpsSVDFMDR&index=3](https://www.youtube.com/watch?v=dSOS-7SZ_BA&list=PLrMP04WSdCjrkNYSFvFeiHrfpsSVDFMDR&index=3)

## Available Options

<table>
<tr>
  <td align="center">
    <img src="https://raw.githubusercontent.com/kubernetes/minikube/master/images/logo/logo.png" alt="Minikube logo" width="200"/><br/>
    <b>Minikube</b>
  </td>
  <td align="center">
    <img src="https://kind.sigs.k8s.io/logo/logo.png" alt="Kind logo" width="200"/><br/>
    <b>Kind</b>
  </td>
</tr>
<tr>
  <td align="center">
    <img src="https://camo.githubusercontent.com/e6a1dedfda4afeadebcf725403b6ce66cbf091c662f36fa4aa615b0fd437fe60/68747470733a2f2f6b33732e696f2f696d672f6b33732d6c6f676f2d6c696768742e737667" alt="K3S logo" width="200"/><br/>
    <b>K3s</b>
  </td>
  <td align="center">
    <img src="https://global.discourse-cdn.com/flex016/uploads/kubernetes/original/2X/6/695eef32dc60d41b604de0dd734ea73f80fb1c69.png" alt="Kubeadm logo" width="200"/><br/>
    <b>Kubeadm</b>
  </td>
</tr>
</table>

1. **Minikube**: A container platform that allows you to create a multi-node cluster.
2. **Kind (Kubernetes in Docker)**: A tool that enables you to run Kubernetes clusters in Docker using simple YAML files for quick configurations.
3. **K3s**: A lightweight Kubernetes distribution developed by Rancher Labs, with a binary of only 50 MB, perfect for resource-constrained environments. Uses SQLite instead of etcd.
4. **kubeadm**: A tool that facilitates Kubernetes cluster creation by joining nodes, ideal for environments like EC2 instances or bare-metal servers.

We'll use **Minikube** with **Kubectl**. Kubectl serves as the command-line tool for Kubernetes. It allows you to run commands in Kubernetes clusters, deploy applications, inspect and manage cluster resources, and view logs. More information at https://kubernetes.io/docs/tasks/tools/.

### Prerequisites https://minikube.sigs.k8s.io/docs/start/

- 2 CPUs or more
- 2 GB of free memory
- 20 GB of free disk space
- Internet connection
- Container or virtual machine manager such as: Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation

We'll use Docker as our container manager since it's one of the recommended options for Linux https://minikube.sigs.k8s.io/docs/drivers/. We'll assume Docker is already installed. For installation instructions:
- Ubuntu: https://docs.docker.com/desktop/install/linux/ubuntu/#install-docker-desktop
- Windows: https://docs.docker.com/desktop/install/windows-install/

## Installing kubectl and minikube

1. Go to https://kubernetes.io/docs/tasks/tools/, select your operating system, and follow the instructions.
2. Go to https://minikube.sigs.k8s.io/docs/start/, select your operating system, and follow the instructions.

Verify each installation with these commands:

```bash
kubectl version --client

minikube version
```

## Creating Your First Cluster

1. After installing both tools, create your first cluster with:

```bash
minikube start --nodes 2 -p local-cluster --driver=docker
```

This command creates a new cluster with two nodes (one master and one worker). The `-p` flag sets the cluster name, while `--driver=docker` specifies that we'll create containers (or VMs) using Docker.

Note: In the output, you'll see that the first node is marked as **control-plane node** (master node) and the second as **worker node**.

Verify the cluster status with:

```bash
minikube status -p local-cluster
```

2. To add another worker node to your cluster:

```bash
minikube node add --worker -p local-cluster
```

Verify that you have 3 nodes in your cluster:

```bash
kubectl get nodes
```

3. To delete a node:

```bash
minikube node delete <node-name> -p local-cluster
```

4. To view additional information through a web interface:

```bash
minikube dashboard --url -p local-cluster
```

This will provide a URL to access the Kubernetes dashboard where you can view cluster information, including nodes under Cluster > Nodes.

5. To stop the cluster:

```bash
minikube stop -p local-cluster
```

6. To delete the cluster:

```bash
minikube delete -p local-cluster
```

## Notes
- For production deployments, it's recommended to use **kubeadm**
- For local development on a laptop, **minikube** is the better choice
