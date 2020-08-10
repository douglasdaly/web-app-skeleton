# Modern Web Application

*A modern web application skeleton.*

## About

I found myself wanting to create new web apps and modern websites on a
fairly regular basis - but not frequently enough to remember all the
ins-and-outs of connecting the backend to the frontend and getting
everything to work well together.  I'm primarily a Python guy (though
I've dabbled in countless languages and frameworks over the years), but
I kept struggling to get the basics working each time I would spin-up a
new project (frontend/backend communication, user authentication, etc.).
The goal of this project is to have a working bare-bones skeleton for a
modern web application which has most of the required functionality
built-in so that you can hit the ground running on building out your
vision for your application and use-case.

This project is a skeleton for creating your own modern web application.
It draws heavily from many other examples and projects (see the
[thanks section below](#Thanks)).  It consists of two inter-related apps
in one:

- **Backend API**: this is the workhorse of the application.  The API is
    what does the heavy-lifting and data storage & transport.  It's
    written entirely in [Python](https://www.python.org/) with
    [typing](https://docs.python.org/3/library/typing.html).  It relies
    on the (*amazing*) [FastAPI framework](https://fastapi.tiangolo.com/)
    for delivering high-performance, scalable, validated, and easy
    (*and fast*) to build APIs.

- **Frontend UI**: this is the interface of the application.  It's built
    upon [Vue.js](https://vuejs.org/) which is an excellent, easy-to-use
    reactive UI/UX framework.  The frontend is written entirely in
    [TypeScript](https://www.typescriptlang.org/).

## Features

Beyond the traditional features a web app skeleton should provide, there
are a few unique features included which allow for even more flexibility
(should you need it).  Some of the general features include:

- Designed to adhere to the [12-Factor App](https://12factor.net/)
    principles.
- [JWT](https://jwt.io/)-based authentication and role-based
    permissioning for restricting functionality to specific groups of
    users.

### Backend Features

The backend is highly-documented and customization to almost any use
case is possible (and relatively simple).  Some of the core
characteristics of it include:

- The [unit of work](https://martinfowler.com/eaaCatalog/unitOfWork.html)
    and [repository](https://martinfowler.com/eaaCatalog/registry.html)
    patterns for all interactions with the objects in the storage
    system.
- Support for multiple storage systems.  [SQLAlchemy](https://www.sqlalchemy.org/)
    is built-in for the typical SQL-based database use case, but the
    [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete)-based
    storage system can be implemented for any type of storage backend
    you're using (you'll just need to write the "driver" code to
    implement it).  The storage system is dynamically-loaded, so
    changing the storage system won't effect any other code (so long as
    it adheres to/implements the required functionality).
- A [click](https://click.palletsprojects.com/en/7.x/)-based CLI tool to
    more easily manage common tasks and functions.

### Frontend Features

The frontend is (more-or-less) a standard [VueCLI](https://cli.vuejs.org/)-based
project, written entirely in [TypeScript] and using the more-modern
(and familiar) [Class-Based Component](https://class-component.vuejs.org/)
style.

- It relies upon [Vuetify](https://vuetifyjs.com/en/) for UI design,
    providing a full-featured and easy-to-use system for creating the
    look and feel you want.
- A layout system for enabling multiple page layouts (and centralizing
    them) allowing you to focus on designing the views and components.
- A cookie-based storage of authentication tokens for login persistence
    between sessions using [js-cookie](https://github.com/js-cookie/js-cookie).
- [Axios](https://github.com/axios/axios) for communication with the
    backend API at the core with a built-in wrapper which (using the set
    environment variables) automatically configures itself to point to
    the backend API and include the user's token in requests requiring
    authentication.
- [Vue Router](https://router.vuejs.org/) for configuring and managing
    routing (and route permisssions).  Additionally, there's the ability
    to create dynamic routes which are automatically added based on the
    current user's role(s).
- [Vuex](https://vuex.vuejs.org/) for application state management using
    [vuex-module-decorators](https://github.com/championswimmer/vuex-module-decorators)
    to simplify the creation of modules and keep with the class-based
    component style of the project.

## Thanks

I feel compelled to do is thank the *many* other excellent projects,
examples, and work of others (if not already mentioned) - which I drew
(*heavily*) upon to create this web app skeleton.

- [Sebastián Ramírez's](https://github.com/tiangolo) (he's also the
    author of the FastAPI package) full-stack, FastAPI
    [cookiecutter template](https://github.com/tiangolo/full-stack-fastapi-postgresql).
- [Chong Guo's](https://github.com/Armour) example Vue & TypeScript
    admin [template](https://github.com/Armour/vue-typescript-admin-template).

## License

&copy; Copyright 2020, Douglas Daly (unless otherwise noted).  All
rights reserved.  This project is licensed under the MIT License, see
the [`LICENSE`](./LICENSE) "License File") for more details.
