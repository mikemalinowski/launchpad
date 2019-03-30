"""
Launchpad represents a small factory and a distinct abstract for defining
actionable items. This is particularly useful when creating libraries of
tools or processes which need to be exposed and invokable.

Each action contains general details such as name, description etc as well
as some richer functionality to invoke the action or for the action to expose
further sub-actions or properties.

As the LaunchPad class is just a factory its population is dynamic based
upon the paths your feed it (or expose through the LAUNCHPAD_PLUGIN_PATHS
variable).

An example of use might be...

```python
import launchpad

# -- Instance launchpad, this gives access to all the
# -- actions
lp = launchpad.LaunchPad('/usr/my_actions')

# -- We can cycle over all the actions
for action in lp.identifiers():
    print(action)

    # -- We can get an action and run it
    lp.request(action).run()

# -- We can access actions direclty too
action = lp.request('My Action Name')
action.run()
```


# Compatibility

Launchpad has been tested under Python 2.7 and Python 3.7 on Windows and Ubuntu.
"""
from .core import LaunchPad
from .core import LaunchAction
from .core import LAUNCHPAD_PLUGIN_ENVVAR
from .core import LAUNCHPAD_USER_PLUGIN_DIR
