# Injector Collections

This package adds collections to the
[Injector](https://github.com/python-injector/injector) python package. A
collection is an injectable class containing several other classes, which were
tagged using the `@CollectionItem` keyword and a designated `Collection`-class.

## Installation

```
pip install injector_collections
```

## Setup

To be able to use this package, You must create a new module-directory inside
your python project. The name of this module-directory does not matter, let's
name it `my_collections` here. Inside this module-directory You must create a
file (module) named `stubs.py` (and of course an `__init__.py`).

Provided your root-directory is named `src`, the following file-tree will be the
result:
```
src
└── my_collections
    ├── __init__.py
    └── stubs.py
```

All files can be initially empty.

## Usage / Example

Be sure to have done everything described in [Setup](#setup).

Let's say You have an application and want to add several plugins which are all
used in the app afterwards, but of course this list of plugins must be easily
extensible. You already use injector to instantiate your App:

```python
# app.py

from injector import inject

class App:
    @inject
     def __init__(self, '''plugins shall be injected here''', '''some other injected classes'''):
         # here comes some code

         def run(self):
             # plugins should be executed here
             # runs the app

from injector import Injector

injector = Injector()
outer = injector.get(App)
```

Now the first step is to create a stub collection for your plugins:
``` python
# my_collections/stub.py

from injector_collections import Collection

class PluginCollection(Collection):
    pass
```
**Note:** The collection class (here `PluginCollection`) should not have any
implementation. Currently any implementation will just be ignored and cannot be
used after the actual class was generated from the stub.

Next add some Plugins as an example. And Tag them with `@PluginCollection` and
your previously defined `PluginCollection` as argument:
```python
# plugins.py

from injector_collections import CollectionItem
# The @CollectionItem decorator needs those stubs as argument
from my_collections.stubs import PluginCollection

@CollectionItem(PluginCollection)
class HelloPlugin:
    def run(self):
        print("Hello Friends!")

@CollectionItem(PluginCollection)
class GoodbyPlugin:
    def run(self):
        print("Goodby Friends!")
```

**Important:** Currently you need to import `CollectionItem` literally, as the
code will be scanned for files containing the `@CollectionItem` string, which
will then be imported to generate the collections!

Now we're almost done. The last thing to do, before we can use our actual
collections is to generate them, of course! Create a small script under your
projects root-directory:

```python
# generate.py
from injector import inject
from injector_collections import generateCollections
# First argument of generateCollections is your my_collections-module name, the
# second a list of modules containing any collection items (in this case your
# plugins-module).
generateCollections(inject, "my_collections", ['plugins'])
```

And execute it:
```
python ./generate.py
```

Now you just need to import the `PluginCollection` to your `App` and use it:

```python
# app.py

# mark that this time, we import from the generated collections, not the stubs!
from my_collections.generated import PluginCollection

from plugins import HelloPlugin

from injector import inject

class App:
    @inject
     def __init__(self, plugins: PluginCollection, '''some other injected classes'''):
         # here comes some code
         self.plugins = plugins

         def run(self):
             # plugins.items contains a dict containing the plugins:
             for plugin in self.plugins.items.values():
                 plugin.run() # prints "Hello Friends!" and "Goodby Friends!"
             # Or just call a single plugin from the collection:
             self.plugins[HelloPlugin].run()
             # also getting plugins simply by class name (if unambigous in this
             # collection) is possible
             self.plugins.byClassname['HelloPlugin'].run()
...
```

### Type Hinting for Items in Collection

If all items in a collection e.g. implement a common Interface, the generated
Collections may make use of type-Hinting. Simply implement a
`getItemType`-Method in your stubs like that:
``` python
# my_collections/stub.py

from plugins import PluginInterface
from injector_collections import Collection

class PluginCollection(Collection):
    @classmethod
    def getItemType(cls):
        return PluginInterface
```

After that the `PluginCollection.items`, `PluginCollection.__get__`,
`PluginCollection.__set__` und `PluginCollection.byClassname` attributes/methods
have proper type hints on `PluginItemInterface`.
