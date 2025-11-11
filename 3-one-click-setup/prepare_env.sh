#!/bin/bash

if [[ -f /etc/debian_release || -f /etc/debian_version ]]; then
    pkg_manager=apt
elif [[ -f /etc/redhat-release || -f /etc/centos-release ]]; then
    pkg_manager=yum
fi

is_update_done=0

update_cache() {
    if [[ $pkg_manager == "apt" ]]; then
        sudo $pkg_manager update -y
    elif [[ $pkg_manager == "yum " ]]; then
        sudo $pkg_manager makecache
    fi
    is_update_done=1
}

install_make() {
    sudo $pkg_manager install -y make
}

install_pip() {
    sudo $pkg_manager install -y python3
    sudo $pkg_manager install -y python3-pip
}

install_docker() {
    if [[ $pkg_manager == "apt" ]]; then
        sudo $pkg_manager install -y apt-transport-https ca-certificates curl gpg software-properties-common gnupg
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
        sudo add-apt-repository -y "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        sudo $pkg_manager update
        sudo $pkg_manager install -y docker-ce
        sudo usermod -aG docker $(logname)
        sudo chmod 666 /var/run/docker.sock
    elif [[ $pkg_manager == "yum" ]]; then
        sudo $pkg_manager install -y yum-utils device-mapper-persistent-data lvm2
        sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        sudo $pkg_manager install -y docker
    fi
    
}

install_docker_compose() {
    if [[ $pkg_manager == "apt" ]]; then
        sudo $pkg_manager -y install docker-compose-plugin
    elif [[ $pkg_manager == "yum" ]]; then
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
}

check_make() {
    if ! command -v make >/dev/null 2>&1; then
        echo "make is not installed!"
        if [[ $is_update_done -eq 0 ]]; then
            update_cache
        fi
        install_make
    else
        echo "make is installed!"
    fi
}

check_pip() {
    if ! command -v pip3 >/dev/null 2>&1; then
        echo "pip3 is not installed!"
        if [[ $is_update_done -eq 0 ]]; then
            update_cache
        fi
        install_pip
    else
        echo "pip3 is installed!"
    fi
}

check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        echo "Docker is not installed!"
        if [[ $is_update_done -eq 0 ]]; then
            update_cache
        fi
        install_docker
    else
        echo "Docker is installed!"
    fi
}

check_compose() {
    if [[ $pkg_manager == "apt" ]]; then
        docker compose &>/dev/null
    elif [[ $pkg_manager == "yum" ]]; then
        docker-compose &>/dev/null
    fi
    if [ $? -ne 0 ]; then
        echo "Docker compose plugin is not installed!"
        check_docker
        install_docker_compose
    else
        echo "Docker compose plugin is installed!"
    fi
}

main_function() {
    check_make
    check_pip
    check_docker
    check_compose
}

main_function