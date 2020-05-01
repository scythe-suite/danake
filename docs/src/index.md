# Introduction

The *∂anake* component will become a part of the [scythe-suite](https://github.com/scythe-suite/) allowing remote authenticated and isolated execution of a development environment.

From the user point of view, *∂anake* will be a web application:

* the authentication will require the student to upload a snapshot of her face taken beside a photo ID; the picture will be obtained using the widely supported [MediaDevices](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices) Web API;

* the development environment will be based on [code-server](https://github.com/cdr/code-server), a "version" of [Visual Studio Code](https://code.visualstudio.com/) that runs in the browser.


The backend will be based on a new application handling the authentication (similar to [𝜏](https://github.com/mapio/tau)) and [Docker](https://www.docker.com/) running a set of micro-services, accessible through a front facing [Nginx](https://www.nginx.com/) reverse proxy.