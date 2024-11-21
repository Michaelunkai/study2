#!/bin/bash

# Alias for getsnap
getsnap() {
  sudo apt install snapd -y && sudo apt-get update && sudo systemctl enable --now snapd.apparmor && sudo systemctl start snapd
}

# Running ranch alias commands
getsnap
curl -s https://raw.githubusercontent.com/kubernetes-sigs/kustomize/master/hack/install_kustomize.sh | bash
sudo mv kustomize /usr/local/bin/
sudo git clone https://github.com/ahmetb/kubectx /opt/kubectx
sudo ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx
sudo ln -s /opt/kubectx/kubens /usr/local/bin/kubens
curl -sS https://webinstall.dev/k9s | bash
source ~/.config/envman/PATH.env
curl -sfL https://get.k3s.io | sh -
sudo apt-get update
sudo apt-get install -y apt-transport-https curl gnupg2 software-properties-common ca-certificates lsb-release
curl -LO https://dl.k8s.io/release/v1.31.1/bin/linux/amd64/kubectl
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Download and install Kubeval
curl -LO https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
tar -xzf kubeval-linux-amd64.tar.gz
sudo mv kubeval /usr/local/bin
kubeval --version

# Download and install Velero
wget https://github.com/vmware-tanzu/velero/releases/download/v1.10.1/velero-v1.10.1-linux-amd64.tar.gz
tar -xvf velero-v1.10.1-linux-amd64.tar.gz
sudo mv velero-v1.10.1-linux-amd64/velero /usr/local/bin/
velero version

sudo snap install helm --classic
curl -Lo kind https://kind.sigs.k8s.io/dl/v0.18.0/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/
kind version
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube /usr/local/bin/
minikube start --driver=docker --force
docker run -d --privileged --restart=unless-stopped -p 9000:80 -p 9443:443 rancher/rancher:latest
sleep 30
gcl 9000

# Apply Weave Scope
kubectl apply -f https://github.com/weaveworks/scope/releases/download/v1.13.2/k8s-scope.yaml

# Apply Calico for networking
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# Download and install Helmfile
curl -sSL https://github.com/roboll/helmfile/releases/latest/download/helmfile_linux_amd64 -o /usr/local/bin/helmfile
chmod +x /usr/local/bin/helmfile

# Download and install K9s
curl -sSL https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz | tar xz
sudo mv k9s /usr/local/bin/

# Final command to open Chrome and show the Rancher Bootstrap Password
cmd.exe /c start chrome http://localhost:9000
docker logs --tail 50 2>&1 | grep 'Bootstrap Password'
