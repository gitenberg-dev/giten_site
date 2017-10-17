# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "ubuntu/trusty64"

  # Expose on the network
  config.vm.hostname = "gitensitedev.local"
  config.vm.network "forwarded_port", guest: 5001, host: 5001 # Dev site

  # Stolen from:
  # https://github.com/DSpace/vagrant-dspace/blob/master/Vagrantfile#L146 Turn
  # on SSH forwarding (so that 'vagrant ssh' has access to your local SSH keys,
  # and you can use your local SSH keys to access GitHub, etc.)
  config.ssh.forward_agent = true
  
  # provision the rest with ansible
  config.vm.provision "ansible" do |ansible|
    ansible.verbose = "v"
    ansible.playbook = "ansible/playbook.yml"
    ansible.galaxy_role_file = "ansible/roles.yml"
  end

  config.vm.provider "virtualbox" do |v|
    v.name = "gitensitedev"
    v.memory = 1024
  end

end
