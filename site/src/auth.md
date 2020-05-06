# The Authentication Flow

This document describes the authentication flow.

The goal of the authentication in the context of the ∂anake component is to link
a student (identified by her email and a picture of her face, taken beside a
photo ID) to an instance of the development environment she will use for the
course of the exam; the purpose of the flow is to make as difficult as possible
for every other student to connect to the same development environment, once the
link is established.

The first actor in the flow is the **reverse proxy**, it intercepts HTTP
requests from the **student** and routes them according to various parameters to
the **authentication application** (that collects student pictures) or to one of
the instances of the **code server**. All these components live in a Docker
*swarm* and networking among them is segregated from the Internet, the swarm has a
single **entry point** (that is a URL).

The **reverse proxy** (sitting at the *entry point*) rules are:

* if the *path* starts with `/da/` followed by a *token* (an alphanumeric
  string), the request will be routed to the *authentication application*,
* if the *path* starts with `/cs/` (possibly followed by other parts), the
  request will be routed to one of the instances of the *code server*, according
  to the value of a *routing cookie* (if it corresponds to a known value);
* in every other case, an error page is returned.

Tokens and cookies are cryptographically signed (using for instance
[itsdangerous](https://itsdangerous.palletsprojects.com)) so that their
integrity can be checked and, moreover, they will be hard to guess.

Every **student** gets her personal *token* (as part of a link to the *∂anake*
entry point) by email before the beginning of the exam.

The **authentication application** performs the following steps:

* whatever the request method is (`GET` or `POST`):
    * if the *token* is invalid, it returns an error page;
    * the token is used to derive the student identity (such as her name, for
      instance);
    * if the student has already provided her picture, the application sends a
      redirect to the *code server* instance;
* if the request method is `GET`, the application sends a form requesting the
  student picture;
* if the request method is `POST` and the request contains a non-empty picture,
  the application tries to store atomically the picture. If it succeeds, it
  determines the *routing cookie* and sets it; in any case, it sends a redirect
  to itself.

The above process (if every steps is preformed in a valid way) can be
represented by the following diagram.

<div class="mermaid">
sequenceDiagram
  participant T as Teacher
  participant S as Student
  participant A as Auth app
  participant C as Code server
  Note over T, S: via email
  T ->> S: sends token
  Note over S, C: via https
  S ->> A: sends token
  A -->> S: asks photo & id
  S ->> A: sends photo & id
  A -->> S: set cookie and redirect
  S ->> C: sends cookie
</div>

It must be clear that,
since sharing the *routing cookie* among students and third parties is not impossible,
**the present flow is quite weak**:
any client with the same cookie will be routed to the same development environment.

As a form of mitigation, the *reverse proxy* requires a HTTPS connection and
keeps a timed log of *routing cookie* and *SSL Session ID* pairs it handles (see
[RFC 246](https://tools.ietf.org/html/rfc5246) for a description of the TLS
Handshake and Session ID); this means that it will be very hard to conceal
*routing cookie* sharing among different browsers. Another possible mitigation
would be to restrict access to the *code server* from a single IP (the one of
the first connection); given the instability of consumer networks (that moreover
are often NAT-ed), this alternative seems less viable, even if more secure.

The collected pictures will be used by a human verifier during the exam, or
shortly after its end, to identify the students; immediately after the
identification, the pictures can be discarded (for privacy compliance). Given
that the *routing cookie* can only be obtained legally in the instant the
picture is shot, the present flow ensures that, in case of cookie sharing, the
identified student can not repudiate to have illegally offered her own credentials
to a third person.
