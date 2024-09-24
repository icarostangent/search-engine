# -*- mode: ruby -*-
# vi: set ft=ruby :

# vagrant plugin install dotenv
require 'dotenv/load'

USERNAME = ENV['VAGRANT_USERNAME']
PASSWORD = ENV['VAGRANT_PASSWORD']
HOMEDIR = "/home/#{USERNAME}"
PROJECT = "search-engine"
GIT_EMAIL = ENV['VAGRANT_GIT_EMAIL']
GIT_USER = ENV['VAGRANT_GIT_USER']

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/jammy64"

  # config.vm.box_check_update = false

  # config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 80, host: 80, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 443, host: 443, host_ip: "127.0.0.1"

  # config.vm.network "private_network", ip: "192.168.33.10"
  # config.vm.network "public_network"

  # config.vm.synced_folder "../data", "/vagrant_data"
  # config.vm.synced_folder ".", "/vagrant", disabled: true

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.cpus = 8
    vb.memory = "8192"
  end

  config.vm.provision "file", source: "#{ENV['USERPROFILE']}\\.ssh\\id_rsa", destination: "/vagrant/id_rsa"
  config.vm.provision "file", source: "#{ENV['USERPROFILE']}\\.ssh\\id_rsa.pub", destination: "/vagrant/id_rsa.pub"

  config.vm.provision "shell", inline: <<-SHELL
    DEBIAN_FRONTEND=noninteractive
    USERNAME=#{USERNAME}
    PASSWORD=#{PASSWORD}
    HOMEDIR=#{HOMEDIR}
    PROJECT=#{PROJECT}
    GIT_EMAIL=#{GIT_EMAIL}
    GIT_USER=#{GIT_USER}

    hostnamectl set-hostname search-engine
    sed -i 's/ubuntu-jammy/search-engine/g' /etc/hosts

    apt-get -y update && apt-get -y upgrade
    apt-get -y install docker.io docker-compose git wget curl net-tools bzip2 gcc make perl

    useradd -m -d $HOMEDIR -s /bin/bash $USERNAME
    echo $USERNAME:$PASSWORD | chpasswd
    cp -r /etc/skel $HOMEDIR 

    echo "alias dc='docker-compose -f docker-compose.development.yml'" >> $HOMEDIR/.bashrc
    echo "alias dc up -d='docker-compose -f docker-compose.development.yml up -d --remove-orphans'" >> $HOMEDIR/.bashrc

    usermod -aG sudo,docker $USERNAME

    mkdir -p $HOMEDIR/.ssh
    mv /vagrant/id_rsa $HOMEDIR/.ssh
    mv /vagrant/id_rsa.pub $HOMEDIR/.ssh

    chmod 700 $HOMEDIR/.ssh
    chmod 600 $HOMEDIR/.ssh/id_rsa
    chmod 644 $HOMEDIR/.ssh/id_rsa.pub
    
    cat $HOMEDIR/.ssh/id_rsa.pub >> $HOMEDIR/.ssh/authorized_keys
    chmod 600 $HOMEDIR/.ssh/authorized_keys

    mkdir $HOMEDIR/workspace
    cp -r /vagrant $HOMEDIR/workspace/$PROJECT

    su $USERNAME && git config --global user.email $GIT_EMAIL
    su $USERNAME && git config --global user.name $GIT_USER

    chown -R $USERNAME:$USERNAME $HOMEDIR

  SHELL
end
