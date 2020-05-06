# The development and testing environment

To test and develop ∂anake, the easiest way is to use [Docker
Machine](https://docs.docker.com/machine/) to setup an environment based on a
set of virtual machines. Once installed the tool and the dependencies (most
notably [VirtualBox](https://www.virtualbox.org/)), just issue

    ./admin dm-create-vms
    ./admin dm-setup-swarm

to create the virtual machines and setup the swarm running on them; this step
(unless the hosts are rebooted) need not be repeated.

Once the VMs are ready, to connect your local docker command with the remote
daemon on the master virtual machine, use

    eval $(./admin dm-env)

to setup the needed environment variables in any new shell you are about to use.

## The local registry

In production mode, ∂anake pulls the images needed for the *router*, *auth*,
*editor* and *cli* services from [Docker Hub](https://hub.docker.com/); such
images can be modified just by the project owner.

Beside the permission issues, it will be very time consuming in any case to
upload modified development images on a public registry; for this reason, the
*base* stack runs a local registry that can be used to distribute development
images to cluster members participating in the swarm.

To use such registry, just set the global variable `DANAKE_DEBUG` to a non empty
value, for instance as

    export DANAKE_DEBUG=1

Now, whenever some code or configuration in the `modules` directory is modified,
just run

    ./admin/build
    ./admin/push

to build the new images and upload them to the local registry.
