# Testing the Environment Setup

The easiest way to prepare the environment is using
[Docker Machine](https://docs.docker.com/machine/) to setup a testing
environment. Once installed the tool and the dependencies (most notably
[VirtualBox](https://www.virtualbox.org/)), just issue

    ./admin dm-create-vms
    ./admin dm-setup-swarm

This step (unless the hosts are rebooted) must not be repeated.
Once the VMs are ready, to use them issue

    eval $(./admin dm-env)

This is used to set up the environment variables needed to the local docker
installation to connect to the daemon running in the manager VM.
