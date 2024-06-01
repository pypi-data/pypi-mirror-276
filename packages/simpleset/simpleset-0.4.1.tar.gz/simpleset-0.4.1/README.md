\[ [Documentation](https://simpleset.readthedocs.io/en/latest/) | [Cheatsheet](https://simpleset.readthedocs.io/en/latest/cheatsheet/) | [Changelog](https://github.com/odigity/simpleset/blob/master/CHANGELOG.md) \]

### Disclaimer!

tl;dr — Expect breaking changes in the future, and pin the version to protect yourself.

This package is very new and has only been used by me as far as I know.

When others start using it in different contexts, providing useful feedback on the quality of the API, and guiding its evolution to a mature 1.0 release, I will then offer API stability guarantees and adhere to SemVer.

In the meantime, I see no harm in using it in production given how simple it is.  However, _**please make sure to pin your package dependency to an exact version**_ so your code doesn't break if and when I decide to change something.

### Synopsis

I dislike Python [Enums](https://docs.python.org/3/library/enum.html).  They behave strangely and are difficult to build on top of or extend.  This package provides a Python class named `Constant` which facilitates the creation and usage of immutable enumerated value sets.  This plain old Python class is both simpler to understand and more powerful/flexible then native enums.

Even a Python beginner should be able to understand *most* of the source code.  The exceptions are discussed in the [docs](https://simpleset.readthedocs.io/en/latest/internals/).

### Preview

```python
from simpleset import Constant

# simplest form

Color = Constant.define_set( "Color", "RED", "GREEN", "BLUE" )

Color.RED == "RED"          # -> True  (equality to strings)
Color.RED.cname             # -> "RED"
Color.all                   # -> [ Color.RED, Color.GREEN, Color.BLUE ]
Color.max_length            # -> 5  (useful for a VARCHAR db column)

# more complex

Color = Constant.define_set(
    "Color",
    RED   = dict( hex="ff0000", like=True  ),
    GREEN = dict( hex="00ff00", like=True  ),
    BLUE  = dict( hex="0000ff", like=False ),
)

Color.RED.hex               # -> "ff0000"
Color.select( like=True  )  # -> [ Color.RED, Color.GREEN ]
Color.get(    like=False )  # -> Color.BLUE
```

[Learn more.](https://simpleset.readthedocs.io/en/latest/)

---

Historical Note:  This package was originally named [py-objects](https://pypi.org/projects/py-objects/).
