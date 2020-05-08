# Deploying and Monitoring

Two preliminary steps to run ∂anake are:

* setup a [Docker Swarm](https://docs.docker.com/swarm/) clustering environment,
* obtain *SSL/TLS Certificates* for the front facing web site — for example
  using [Let's Encrypt](https://letsencrypt.org/).

Such steps are quite standard (albeit complex), so are not described in detail
here. The [testing setup](testing.md) suggests a simple way to prepare a local
environment to experiment before installing on dedicated servers.

!!! Contexts

    Observe that [Docker Context](https://docs.docker.com/engine/context/working-with-contexts/)
    are a very convenient way to refer to different environements; in particular, once
    a docker swarm has been setup and the host running the manager node has ssh access configured,
    a context referring to such swarm can be setup as

        docker context create --docker "host=ssh://USER@HOST" CONTEXT

    where `USER` and `HOST` are the credential for the manager host, and `CONTEXT` the name of the context;
    issuing

        docker context use CONTEXT

    will make all future `docker` commands refer to the manager host.

To run the ∂anake system, several *services* need to be deployed:

* the `base` *stack* providing the [Portainer](https://www.portainer.io/)
  monitoring service, and a local [Docker
  Registry](https://docs.docker.com/registry/) required to provide, if needed,
  development *images* to all the other involved services;
* a `backend` stack providing the **router** and **auth** modules;
* a set of separate services providing an instance of the **editor** module per
  student.

Before running ∂anake, you need to setup some docker
[secrets](https://docs.docker.com/engine/swarm/secrets/) and
[configs](https://docs.docker.com/engine/swarm/configs/) needed by the services:
the `base` stack depends on the SSL/TLS Certificates, moreover, the *auth*
module depends on two configuration files, both placed in the `confs` directory:

* an `auth-config.py` file defining the following variables:
    * `SECRET_KEY`, a random string that **must be kept secret** used by
      [itsdangerous](https://itsdangerous.palletsprojects.com) to sign tokens,
    * `TOKEN_DURATION` and `COOKIE_DURATION` the expiration time for the token and cookie (in seconds).
* a `uid2info.tsv`
  (in [tab separated](https://en.wikipedia.org/wiki/Tab-separated_values) format)
  containing a two-field line per student, the first field being the student ID
  number and the second any string useful to identify the student (for instance
  her first and last name).

The *auth* and *router* module, moreover, depend on the `cookie2uid.map` file
containing the association between random generated cookies and student IDs. To
generate such file from `uid2info.tsv` and setup all the required
configurations, just run

    danake config remove
    danake config create

this will also saved in the `confs` directory the above mentioned cookie map,
that **must be kept secret**.

The first stack can now be deployed without any further configuration issuing
the command

    danake start base

Once this stack is running, the command

    danake utils monitor

can be run to open the monitoring site; the first connection will require to set
a username and password that **must be kept secret**.

Finally the second stack and editor services can be deployed issuing

    danake start backend
    danake start editor

To tear down the system, the correct sequence is

    danake stop editor
    danake stop backend
    danake stop base
