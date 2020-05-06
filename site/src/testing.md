# Testing environment setup

The easiest way prepare the environment is using [Docker Machine](https://docs.docker.com/machine/) to setup a testing environment. Once installed the tool and the dependencies (most notably [VirtualBox](https://www.virtualbox.org/)), just issue

    ./admin dm-create-vms
    ./admin dm-setup-swarm

This step (unless the hosts are not rebooted) must not be repeated. Once the vms are ready, to use them issue

    eval $(./admin dm-env)

to setup the environment variables needed to the local docker installation to
connect to the daemon running in the manager vm.

