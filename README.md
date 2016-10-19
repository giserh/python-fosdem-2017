# Description

This script is just a tool for the generation of the website of http://python-fosdem.org 2017

# Installation

There is no packaging for this script, but if you want to create one, you can.

Firstly, you need to create a virtualenv or just install the libraries in your `$HOME` directory.

```bash
pip install -r requirements.txt
```

# How to use it

Just install the libraries and you call the script

```bash
./generator.py
```

See the result in your browser, just use `python -m http.server` and you have to connect to http://localhost:8000 .
