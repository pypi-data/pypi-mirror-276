# osstrack-action

GitHub action to upload your project dependencies to osstrack.io.

## Overview

This action allows you to upload your project dependencies to osstrack.io. It is a simple way to keep track of the dependencies of your project and to have various metrics about them like freshness, security, and licensing.

## Enabling the action

### Declare dependencies

To declare the dependencies of your project, you need to create a file named `.osstrack.conf` in the root of your repository. This file is managed by the osstrack utility and should not be modified manually.

```shellsession
$ cd <workspace>
$ pip install osstrack
$ osstrack add poetry.lock
$ # add a virtualenv where to capture the dependencies with pip freeze
$ osstrack add .tox/functional
$ # remove a dependency
$ osstrack del .tox/functional
```

### Sample Configuration

Defining Github Actions requires creating a directory `.github/workflows` inside your repository. Inside this directory, you create files processed when various events occur.

The simplest example of using this action would be to create the file `.github/workflows/push.yml` with the following contents:

```yaml
---
name: Push
on:
  push:
    branches:
      - main
jobs:
  osstrack:
    runs-on: ubuntu-latest
    steps:

      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Create the virtualenv
        run: |
          sudo pip install tox
          tox -e functional --notest

      - name: Upload dependencies to osstrack.io
        uses: osstrack/osstrack-action@0.1
        with:
          token: ${{ secrets.OSSTRACK_TOKEN }}
...
```

You need to store the `OSSTRACK_TOKEN` in the repository secrets. You can create a token in the osstrack.io website.

## Usage outside of a GitHub action

If you want to use the same dependency management in other CI pipelines or in a local test, you can install the python package:

```shellsession
$ pip install osstrack
```

Then you can use the `osstrack` command to upload the dependencies of a change:

```shellsession
$ cd <workspace>
$ export OSSTRACK_TOKEN=<your token>
$ # extract the dependencies of the current branch using tox
$ # or whatever you use to create the virtualenv
$ tox -e functional --notest
$ # Upload the dependencies of the current branch
$ osstrack upload
```

## Roadmap

- [ ] [](https://github.com/osstrack/osstrack-action/issues/)
