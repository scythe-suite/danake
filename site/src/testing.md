# The development and testing environment

To test and develop ∂anake, the easiest way is to use [Docker
Machine](https://docs.docker.com/machine/) to setup an environment based on a
set of virtual machines. Once installed the tool and the dependencies (most
notably [VirtualBox](https://www.virtualbox.org/)), just issue

    danake machine create
    danake machine setup

to create the virtual machines and setup the swarm running on them; this step
(unless the hosts are rebooted) need not be repeated; a very convenient way to
use different setup is to use [Docker
Context](https://docs.docker.com/engine/context/working-with-contexts/).

It is possible to create a `danake-test` *context* for this testing setup using

    danake machine context

and switch to it as

    docker context use danake-test

## The local registry

In production mode, ∂anake pulls the images needed for the *router*, *auth*,
*editor* and *cli* services from [Docker Hub](https://hub.docker.com/); such
images can be modified just by the project owner.

Beside the permission issues, it will be very time consuming in any case to
upload modified development images on a public registry; for this reason, the
*base* stack runs a local registry that can be used to distribute development
images to cluster members participating in the swarm.

To use such registry, just set the global variable `DANAKE_DEBUG` to a non empty
value in the `danake-config.sh` file as

    export DANAKE_DEBUG=1

and run the registry with

    danake start registry

Now, whenever some code or configuration in the `modules` directory is modified,
just run

    danake images build
    danake images push

to build the new images and upload them to the local registry; on the other
hand, you can get the images with

    danake images pull

Of course *pushing* to the official registry is restricted to the project owner.

At the end of the development cycle, just unset `DANAKE_DEBUG` and stop the
registry with

    danake stop registry
