
# Overview


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

# Installation

If you use pip, you can simply run ```pip install launchpad```. That will 
pull down the required dependencies (scribble & factories) automatically.

Note: If you install ```launchpanel``` this module will be pulled down
automatically as a dependency. Therefore you only need to pull down this
module explicitly if you do not plan to utilise the launchpanel ui.

# The Abstract

To define an action you must implement a Launch Action. The process of 
implementing an action is just a case of creating a python file and inheriting
from the LaunchAction object, like this:

```python
import launchpad

# ------------------------------------------------------------------------------
class MyAction(launchpad):
    Name = ''
    Description = __doc__
    Icon = ''
    Groups = []

    @classmethod
    def run(cls):
        pass

    @classmethod
    def actions(cls):
        return dict()

    @classmethod
    def properties(cls):
        return dict()

    @classmethod
    def viability(cls):
        return cls.VALID

```

The properties are very much about giving descriptive information about your
action. Description, Icon and Groups are all optional and can be left out
entirely if desired - but Name must always be filled in.

__run()__ is where you perform the default action for this action.

__actions()__ allows you to return a dictionary of key value pairs where the
key is the action label and the value is the function/callable. This allows
you to give your action variations or extended behaviour which is accessible
in a consistent way.

__viability()__ is the mechanism to give an indiciation as to whether your 
action is valid within the current environment. For example, if your action
relies on paths existing, or environment variables being set, you can run those
tests there are return the Action Viability (VALID, INVALID, DISABLED).

__properties()__ is a mechanism for storing blind data. It should always return
a dictionary but there is not formal structure for that dictionary. This is
implemented to give you the oppotunity to store tool specific data within the 
action depending upon your needs.


# Credits & Collaboration

This module was inspired by some excellent collaborative projects with a 
fantastic tech-artist called __Toby Harrison-Banfield__.

I am always open to collaboration, so if you spot bugs lets me know, or if
you would like to contribute or get involved just shout!


# Compatibility

Launchpad has been tested under Python 2.7 and Python 3.7 on Windows and Ubuntu.
