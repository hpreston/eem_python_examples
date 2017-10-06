# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "iosxe/16.6.1"

  config.vm.network :private_network, virtualbox__intnet: "link1", auto_config: false
  config.vm.network :private_network, virtualbox__intnet: "link2", auto_config: false

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible_provision.yaml"
    ansible.inventory_path = "./hosts"
  end

end
