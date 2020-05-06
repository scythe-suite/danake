# Deploying and Monitoring

Two preliminary steps to run ∂anake are:

* setup a [Docker Swarm](https://docs.docker.com/swarm/) clustering environment,
* obtain *SSL/TLS Certificates* for the front facing web site — for example
  using [Let's Encrypt](https://letsencrypt.org/).

Such steps are quite standard (albeit complex), so are not described in detail
here. The [testing setup](testing.md) suggests a simple way to prepare a local
environment to experiment before installing on dedicated servers.

To run the ∂anake system, several *services* need to be deployed:

* the `base` *stack* providing the [Portainer](https://www.portainer.io/)
  monitoring service, and a local [Docker  Registry](https://docs.docker.com/registry/)
  required to provide the *images* to all the other involved services;
* a `danake` stack providing the **router** and **auth** modules;
* a set of separate services providing an instance of the **editor** module per
  student.

The first stack can be deployed without any further configuration issuing the command

    ./admin start-base

(and possibly removed, at the end of the session, with `./admin stop-base`).

To run the rest of the services, the *auth* module needs two configuration
files, both placed in the `confs` directory:

* an `auth-config.py` file defining the following variables:
    * `SECRET_KEY`, a random string that **must be kept secret** used by
      [itsdangerous](https://itsdangerous.palletsprojects.com) to sign tokens,
    * `TOKEN_DURATION` and `COOKIE_DURATION` the expiration time for the token and cookie (in seconds).
* a `uid2info.tsv`
  (in [tab separated](https://en.wikipedia.org/wiki/Tab-separated_values) format)
  containing a two-field line per student, the first field being the student ID
  number and the second any string useful to identify the student (for instance
  her first and last name).

Before deploying other services, cookies need to be generated. The command

    ./admin generate-cookies

starting from the list in `uid2info.tsv` will generate the `cookie2uid.map` file
(saved in the `confs` directory, that **must be kept secret**) containing the
association between cookies and student IDs used both by the *auth* module and
the *router* one.

Now the second stack and editor services can be deployed issuing

    ./admin start-base
    ./admin start-editor

(such services can be removed using respectively `./admin stop-base` and
`./admin stop-editor`).
