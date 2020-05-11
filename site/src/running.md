# Deploying and Monitoring

Two preliminary steps to run ∂anake are:

* setup a [Docker Swarm](https://docs.docker.com/swarm/) clustering environment,
* obtain *SSL/TLS Certificates* for the front facing web site — for example
  using [Let's Encrypt](https://letsencrypt.org/).

Such steps are quite standard (albeit complex), so are not described in detail
here. The [testing setup](testing.md) suggests a simple way to prepare a local
environment to experiment before installing the clustering environment on
dedicated servers.

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

* the `danake` *stack* managing the **router** and **auth** services, plus
  [Portainer](https://www.portainer.io/) monitoring service and it *agents*;
* a set of separate services providing an instance of the **editor** module per
  student.

To configure such services, first you need to setup some docker
[secrets](https://docs.docker.com/engine/swarm/secrets/) and
[configs](https://docs.docker.com/engine/swarm/configs/):

* the SSL/TLS Certificates (in the `certs` subdirecotry);
* an `auth-config.py` file defining the following variables:
    * `SECRET_KEY`, a random string that **must be kept secret** used by
      [itsdangerous](https://itsdangerous.palletsprojects.com) to sign tokens,
    * `TOKEN_DURATION` and `COOKIE_DURATION` the expiration time for the token and cookie (in seconds);
* a `uid2info.tsv`
  (in [tab separated](https://en.wikipedia.org/wiki/Tab-separated_values) format)
  containing a two-field line per student, the first field being the student ID
  number and the second any string useful to identify the student (for instance
  her first and last name);
* the `cookie2uid.map` containing the association between cookies and student
  IDs.

The last file is generated from `uid2info.tsv` and **must be kept secret**; to
generate it and  and setup all the required configurations, just run

    danake config remove
    danake config create

Once the setup has been completed, it is possible to run the *stack* with

    danake start danake

and, once it is running, the command

    danake utils monitor

can be run to open the monitoring service; the first connection will require to set
a username and password that **must be kept secret**.

If everything looks fine, the editor services can be deployed issuing

    danake start editor

To tear down the system, the correct sequence is

    danake stop editor
    danake stop danake
