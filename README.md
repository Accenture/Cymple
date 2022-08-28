# Cymple - Cypher Modular Pythonic Language Extension

A productivity tool for creating Cypher queries in Python.

[![Documentation Status](https://readthedocs.org/projects/cymple/badge/?version=latest)](https://cymple.readthedocs.io/en/latest/?badge=latest)
[![Python package](https://github.com/Accenture/Cymple/actions/workflows/python-test.yml/badge.svg)](https://github.com/Accenture/Cymple/actions/workflows/python-test.yml)

## About the project

Cymple is a lightweight Python package for creating queries in Cypher, Neo4j's graph database query language. 
Give it a try, it's 'Cymple'!

Consider using Cymple if you want:
* auto-completion for writing Cypher
* to write compound Cypher queries without getting involved with strings
* to write Cypher queries in a scalable and extensible manner
* to be able to easily reuse Cypher queries across your code

![image](https://user-images.githubusercontent.com/97434370/162214862-2cd00d28-0565-4838-af41-9e0c0f49b090.png)


## Getting Started

### Setup
```shell
pip install cymple
```

### Examples

#### Simple Example
Let's take a look at the following snippet. 
```python
from cymple import QueryBuilder

qb = QueryBuilder()
query = qb.match().node(labels='Person', ref_name='p')
query = query.where('p.name', '=', '"Michelle"').return_single('p')
print(query)
```
This snippet will output the following Cypher query:
```cypher
MATCH (p: Person) WHERE p.name = "Michelle" RETURN p
```

See the `samples` directory for examples. 

##### Cymple is intended for creating Cypher queries in Python, rather than executing queries on an actual DB. 
##### For executing queries, see [Neo4j's Bolt driver for Python](https://github.com/neo4j/neo4j-python-driver). See also `neo4j_e2e.py` in the `samples` directory. 


#### Autocompletion
Cymple is designed to provide autocompletion on IDEs that support autocompletion. This feature is context aware with respect to the current query being written. 


![gif1](https://user-images.githubusercontent.com/97434370/162214796-cd1eeb70-9875-4a3c-9008-6bcda7fb4896.gif)


#### Reusing Queries
Two queries can be combined to a create a new one. 
```python
qb = QueryBuilder()
query1 = qb.match().node(labels='Person', ref_name='p').with_('p')
query2 = qb.match().node(labels='Person', ref_name='q').related_to('friend_of').node('p')
query = query1 + query2
print(query)
```
This snippet will output the following Cypher query:
```cypher
MATCH (p: Person) WITH p MATCH (q: Person)-[: friend_of]->(: p)
```

### Prerequisites

* Python 3.8+

## Contributing

### Intro
We encourage you to help us to improve this package! 
These instructions will give you a copy of the project up and running on your local machine for development and testing purposes.

### Installing a Development Environment

```shell

# Set virtual environment.
python -m venv .venv
source .venv/bin/activate

# Upgrade pip

# Install development dependencies.
# Tools needed for deployment and packaging will be installed now.

pip install -r requirements-dev.txt
```

### Development tools configurations

* `setuptools` is configured in `setup.cfg`

* `pycodestyle` is configured in `setup.cfg`

* `coverage.py` is configured in `pyproject.toml` 


### Testing

`pytest` is used as a test runner.

`pytest` configurations reside in `pyproject.toml`

`pytest` `fixtures` are stored in `tests/conftest.py` file.

How-to run tests:

```shell
# Install test requirements.

pip install -r requirements-test.txt

# Run tests.
# All the tests under tests/ directory will be run.

pytest --cov=cymple

```

### Adding a new Cypher clause
Adding a new Cypher clause to Cymple consists of few simple steps:
1. Go to `src/cymple/internal/declarations/`. This directory contains all supported clause declarations. 
2. Add a json file describing the clause and the method(s) interfaces(s) of the new clause that you would like to add to the builder. If you do it for the first time, take a look at existing json files of currently supported Cypher clauses.
3. Run `python src/cymple/internal/internal_renderer.py`. This script generates a new `builder.py` file with all clauses that were declared in `src/cymple/internal/declarations/`. 
4. By default, by adding a declaration json file, the `internal_builder.py` script takes the declared clause and generates a method that simply concatenates your new clause to the builder's current query. However, if you need anything more complex than that, you can write your own implementation by creating a new method with your clause's name at `src/cymple/internal/overloads/`. Don't forget to run `python src/cymple/internal/internal_renderer.py` again :)
5. If you're satisfied with the new clause, add a unit test in `test_clauses.py` and make sure it generates the expected Cypher string. 

### Generating Documentation
To generate a new HTML documentation, run:
```
cd docs
make clean html
make html
```

### Versioning

[Semantic Versioning](http://semver.org/) is used for versioning. 

For the versions available, see the tags on the repository.

Current version is stored in `src/cymple/version.py`.


### Project structure

```shell
cymple/
├── docs/   # Project documentation
├── pyproject.toml  # Development and packaging tools configurations
├── README.md  # Project general information
├── requirements-dev.txt  # Development dependencies, such as packaging tools, etc.
├── requirements-test.txt  # Test dependencies
├── requirements.txt       # Pinned versions of all the end-user dependency tree
├── setup.cfg  # packaging tool configurations
├── setup.py   # Packaging script
├── src/  # All source code
│   └── cymple/  # Cymple source code
│       ├── internal/  # Cypher builder internal renderer
│       │   ├── declarations/        # clause declarations
│       │   ├── overloads/           # custom clause implementations
│       │   ├── finale.py            # A part of the rendered code that comes last
│       │   ├── internal_renderer.py # Internal renderer implementation for creating Cymple's user-facing code
│       │   └── preface.py           # A part of the rendered code that comes first
│       ├── __init__.py  # Package initialization
│       ├── __main__.py  # Main script when run as a command line tool
│       ├── builder.py   # Query Builder implementation
│       ├── typedefs.py  # Query Builder typedefs to be used in Cymple's API
│       └── version.py   # Package version
└── tests/  # Tests
    ├── conftest.py  # Fixtures
    ├── data/  # Tests data files, such as input/output files, mocks, etc.
    ├── e2e/   # End-to-End functional tests
    ├── integration  # Integration tests
    └── unit  # Unit tests
        ├── __init__.py
        └── test_real_use_cases.py  # Test project startup


```
