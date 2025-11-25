# -*- mode: ruby -*-
# vi: set ft=ruby :

# This vm is for testing purposes. You can use your own computer to install minikube on.

Vagrant.configure("2") do |config|

  config.vm.box = "gusztavvargadr/xubuntu-desktop-2404-lts"
  config.vm.box_version = "2509.0.0"
  config.vm.hostname = "sre-bootcamp"
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 8192
    vb.cpus = 4
  end
  config.vm.network "private_network", ip: "192.168.60.5"
  config.vm.network "forwarded_port", guest: 22, host: 2200, id: "ssh"
  # config.vm.network "forwarded_port", guest: 30000, host: 30000
  config.ssh.forward_agent = true
  config.vm.provision "file", source: "minikube.service", destination: "/tmp/minikube.service"
  config.vm.provision "shell", inline: <<-SHELL
    mv /tmp/minikube.service /usr/lib/systemd/system/minikube.service
    chown root:root /usr/lib/systemd/system/minikube.service
    chmod 644 /usr/lib/systemd/system/minikube.service
    apt-get update
    sudo apt remove -y docker docker.io
    sudo apt install -y apt-transport-https ca-certificates curl gpg software-properties-common gnupg
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install -y docker-ce
    sudo usermod -aG docker vagrant
    sudo chmod 666 /var/run/docker.sock
    sudo apt-get install -y docker-compose-plugin
    curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-linux-amd64
    sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    echo "alias k='kubectl'" >> /home/vagrant/.bashrc
    sudo -u vagrant minikube config set driver docker
    sudo systemctl daemon-reload
    sudo systemctl enable minikube
    sudo systemctl start minikube
    sudo -u vagrant minikube addons enable ingress
    curl -fsSL https://packages.buildkite.com/helm-linux/helm-debian/gpgkey | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    echo "deb [signed-by=/usr/share/keyrings/helm.gpg] https://packages.buildkite.com/helm-linux/helm-debian/any/ any main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    sudo apt-get update
    sudo apt-get install -y helm
    sudo snap install postman
  SHELL
end