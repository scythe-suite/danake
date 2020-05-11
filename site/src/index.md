# Introduction

<img align="right" style="margin-left: 1em;" src="img/logo.png">

The *∂anake* component is part of the
[scythe-suite](https://github.com/scythe-suite/) and allows remote,
authenticated, and isolated execution of a development environment.

From the student point of view, *∂anake* is a **just web application**:

* the authentication requires the student to upload a picture of her face, taken
  beside a photo ID; such picture will be obtained by using the widely supported
  [MediaDevices](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices)
  Web API;

* the development environment is based on
  [code-server](https://github.com/cdr/code-server), a "version" of [Visual
  Studio Code](https://code.visualstudio.com/) that runs in the browser.

The **backend** consists of a novel application handling the authentication
(similar to [𝜏](https://github.com/mapio/tau)) and a
[Docker](https://www.docker.com/) *swarm* running a set of micro-services,
accessible through a front facing [Nginx](https://www.nginx.com/) reverse proxy.
