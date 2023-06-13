# Python Starter Project

This repository is a generic skeleton project for python development.
It uses Conda inside a docker container (instead of PIP + virtualenv) for package management in multiple environments.

Included also is an example which shows how to do basic testing with Pytest, logging with the builtin module, and generate documentation with Sphinx.

## Quick start

Make sure you have `docker` and `make` installed (@windows users: please visit this [page](https://bainco.atlassian.net/wiki/spaces/AAG/pages/15163031577/How+to+set+up+a+starter+project+on+Windows) if you need help to properly set your environment).
From the root folder, build the image:
```
make build
```
Start a jupyter lab server:
```
make notebook
```
You're done, happy coding!


You can also take look at the advanced usage section below if you're interested in the additional starter project features, i.e.
- executing bash commands in the project container
- logging and testing
- building the documentation automatically
- etc...



## Advanced usage
### Getting Setup

To build locally you will need the commands `make` and `docker` working on your machine.
`make` allows us to automate building commands and `docker` will provide a standard environment so that we guarantee the same behavior on Windows, MacOS, or running in the cloud.

The `make` command is available by default on unix-like systems but Windows users have to manually install it (see [here](http://gnuwin32.sourceforge.net/packages/make.htm) for example). Please also note that Windows users need to manually enable file sharing in order to have the volumes properly mounted (docker-desktop -> settings -> resources -> files sharing, see [here](https://docs.docker.com/docker-for-windows/) for more information). If you're not yet very familiar with those concepts, you can rely on this steps by steps [tutorial](https://bainco.atlassian.net/wiki/spaces/AAG/pages/15163031577/How+to+set+up+a+starter+project+on+Windows) on how to set up the starter project on Windows.

If you are on a windows machine and cannot run docker because of a virtualization lock at the BIOS level by default, you can either ask TSG for help enabling it or you can use the webapp version instead of the CLI version of the starter automation tools.

**General tips:** In the starter projects, the `make` commands generally alias for longer docker commands. Hence `make` commands shall be executed from your local terminal while other commands (like `python` or `pytest`) shall be executed in your container.

### Starting Development

First, install the githooks by running the command (MacOS/Linux)

```
source ops/install-githooks
```
On Windows, you can use `git config core.hooksPath ops`.

These git hooks will use the tool black to scan and change any formatting errors when you are trying to checkin new code.

Next, inside the newly created folder you can run

```
make build
```

This will run through the build process and create a new docker with our base project inside.

We can test that everything worked correctly by running the following command to get into the python REPL

```
docker run -it tch-test-tandoor-ds-app python
```

If you see an interactive python shell which reports its version, then everything is working.  
You can play around with basic python commands and finish by typing `exit()`

If you need to install specific dependencies you should be able to modify the requirements.txt file following the pattern already in that file.
It is good form to include a specific library version number for build consistency.


### Coding, Logging, and Testing
When you update configurations you must rerun the `make build` command but when you update code it will be immediate because the docker mounts the folder so all code is shared in realtime.

The example-project which is included has a file/module called `compute_recurrences.py` which computes some stats about Fibonnaci numbers using a helper packarge called recurrence_calculators.
To see code changes updated in realtime first run

```
make exec
```

and you should be given a shell inside the docker in the directory /var/dev.  If you `ls` you should see the files which are part of the project. Next run

```
python src/compute_recurrences.py
```

You should see it print the first Fibonacci numbers with other stats. Now with the terminal still open, go and change something in the code and run the command in the shell again.

In this way, changes to the source code are instantly testable inside the docker with the much more consistent and complex internal enviroment.

Also notice that the information being shown is not printed but logged.  Logging in python comes in different levels and the code shows and example of how we can use environment variables to determine which level.
By default it will show all logs of info or above in severity but run either

```
export LOGLEVEL=DEBUG
python src/compute_recurrences.py

export LOGLEVEL=WARNING
python src/compute_recurrences.py
```

The first will now show some internal logs of what is being computed at each step. The second will only show if there is an error/warning.

Next to run all through all tests and generate a coverage report for all python in the src folder

```
pytest --cov tests
```

You should see all tests are currently passing and that the code is close to 100%   
Also, as demonstrated in the `pytest.ini` file, tests can be given names or 'marks' so run just the tests related to the cache with

```
pytest --cov -k cache_tests tests
```

This will only run two tests so we expect not every code path will be taken thus lower coverage.

One additional tool called `black` is a code formatter. From inside the docker run `black src` to automatically give consistent spacing, capitalization, etc. across all code in the src folder.


### Auto-Documentation
Documentation can also automatically be generated from classes and methods using docstrings in the codebase where available. We rely on the sphinx library to do this.
Start by using
```
make doc-update USERNAME=<your-name> 
``` 
to create the `docs/` folder and populate it with the required files. The value assigned to `USERNAME` will be used as the author name in the doc.

The command
```
make doc-publish
``` 
will create a html version of the documentation.  The main file is `docs/_build/html/index.html` so open this in a browser to see the results.

Sphinx can only show useful documentation automatically if you include structured comments while you program in the numpy friendly format demonstrated in the examples.  
It is good form to include the input and outputs type hint information as well so that method signatures are clear from the documentation alone.

After changing your code, you may want to update your documentation. We recommend to first purge the existing doc with
```
make doc-clean
```
and then recreate it with the commands described above.

## Explore Data
The purpose of a data proof of concept (POC) is to understand and document the dataset and build and measure the accuracy of a model.

Flat files with json or CSV data for example can be dropped into the data folder to be worked on using the tools in this repo.

```
make build
make notebook
```

These commands will create a container with the popular JupyterLab tool running which you can access in a browser with the provided link to interactively code python.

## Display Data
The purpose of the MVP maturity level is to combine all the pieces and have something working end to end.
In the case of data products this means data cleaning, model building, and displaying results back to the user. The MVP app provided in this repo is a simple data dashboard which loads data, cleans it, fits a model, and visualizes the results using the Dash framework.
The computation steps are split into a separate Python module called 'src/model.py' while the controller and view aspects
are in 'src/app.py', 'src/flask_app.py', and 'src/dash_app.py'.

To start a Docker container with the dashboard app, run

```
make build
make dashboard
```
Now you should be able to see the dashboard in a browser at `localhost:8050`


The Dash framework automatically includes css style sheets in the assets folder to further modify the frontend appearance.
- Each method in model.py is like a unit-testable step in a small data pipeline
- Each method in model.py has a unit test in /src/tests/unit/test_model.py
- Each function in app.py is an event-driven handler to update the frontend when a user changes an input.

There is also a file at the base of the repo called `pytest.ini` which defines "marks" which can be used to run only certain relevant groups of tests.
For example, perhaps fitting a model is very slow and when you make a change to the data preparation you could run only the preparation tests with the "prepare_tests" mark

```pytest --cov -k prepare_tests tests```

For more info on best practices [see the data product playbook](https://github.com/Bain/playbooks/blob/master/data-analytics-product-playbook.md#methodologies-for-building-apps)
