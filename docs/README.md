## Building the documentation

The internal API reference documentation gets built by [Sphinx](https://www.sphinx-doc.org/).
Here are the main commands to know about.

```sh
uv sync --group=doc  # install sphinx and other doc dependencies

sphinx-autobuild docs/source docs/build/html --watch src  # build the documentation, automatically reload on changes

sphinx-build -M html docs/source/ docs/build/  # build the documentation
```

## Sphinx cheatsheet

To generate docs for `module.name` using [sphinx-autodoc](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
put the following in a `.rst` file included by `docs/source/index.rst`

```rst
module.name
-----------

.. automodule:: module.name
   :members:
```

This will grab `module.name.__doc__` as well as the docstrings of
the (public) classes and functions living under `module.name`.
