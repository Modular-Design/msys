# Documentation

## The big Documentation
The Documentation is based on the following [tutorial](https://realpython.com/documenting-python-code/).

Currently the Documentation has to be hosted locally:
````shell
pip install mkdocs
mkdocs serve
````

In the future the documentation will be hosted over [ReadtheDocs](https://readthedocs.org/) with the help of the this 
[tutorial](https://www.mkdocs.org/user-guide/deploying-your-docs/)

## Guidelines for SorceCode Documentation
To document source code please use [Docstrings](https://realpython.com/documenting-python-code/) and 
in particular use the [Google docstring](https://mkdocstrings.github.io/handlers/python/#google-style) -Format:
```python
 """This is an example of a module level function.

    Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    If \*args or \*\*kwargs are accepted,
    they should be listed as ``*args`` and ``**kwargs``.

    The format for a parameter is::

        name (type): description
            The description may span multiple lines. Following
            lines should be indented. The "(type)" is optional.

            Multiple paragraphs are supported in parameter
            descriptions.

    Args:
        param1 (int): The first parameter.
        param2 (:obj:`str`, optional): The second parameter. Defaults to None.
            Second line of description should be indented.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.

    """
```
The complete example can be found [here](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).

To see the source code documentation while coding, see the following example: 
````python
from reporting.core import *
help(Input)
````