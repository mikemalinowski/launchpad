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
"""
import os
import sys
import factories


# -- Define the environment variable we will use when looking
# -- for plugin paths
LAUNCHPAD_PLUGIN_ENVVAR = 'LAUNCHPAD_PLUGIN_PATHS'

# -- This is a default location we always look in for user placed
# -- actions
LAUNCHPAD_USER_PLUGIN_DIR = os.path.join(
    os.path.expanduser('~'),
    '.launchpad',
)


# ------------------------------------------------------------------------------
class LaunchPad(factories.Factory):

    # --------------------------------------------------------------------------
    def __init__(self, plugin_locations=None):

        # -- Define the variable we will use to pass all our
        # -- plugin paths to
        paths = [LAUNCHPAD_USER_PLUGIN_DIR]

        # -- Add any user defined plugin locations
        if plugin_locations:

            # -- Quick safety check to ensure we're passing a list
            # -- of locations rather than just a single string
            if not isinstance(plugin_locations, (list, tuple)):
                plugin_locations = [plugin_locations]

            paths.extend(plugin_locations)

        # -- Add any paths defined in the environment
        if LAUNCHPAD_PLUGIN_ENVVAR in os.environ:
            paths.extend(
                [
                    os.path.abspath(path)
                    for path in os.environ[LAUNCHPAD_PLUGIN_ENVVAR].split(';')
                    if path.strip()
                ]
            )

        # -- Initiate the factory
        super(LaunchPad, self).__init__(
            abstract=LaunchAction,
            plugin_identifier='Name',
            versioning_identifier='Version',
            paths=paths,
        )

    # --------------------------------------------------------------------------
    def identifiers(self):
        """
        We overload this function because we want to omit any invalid
        actions

        :return: list(str, str, ...)
        """
        filtered_actions = list()

        for action_name in sorted(super(LaunchPad, self).identifiers(), key=lambda t: t.lower()):
            action = self.request(action_name)

            if action.viability() != LaunchAction.INVALID:
                filtered_actions.append(
                    [
                        action_name,
                        action.Priority,
                    ],
                )

        final_results = list()

        for action, _ in sorted(filtered_actions, key=lambda t: t[1], reverse=True):
            final_results.append(action)

        return final_results

    # --------------------------------------------------------------------------
    def grouped_identifiers(self):
        """
        This will create a dictionary of groups, where the keys are the groups
        defined in the actions and the values are lists of identifiers.

        :return: dict(group_name: [name, name, name]
        """
        data = {'Uncategorised': list()}

        for action in self.plugins():

            # -- Ignore invalid actions
            if action.viability() == LaunchAction.INVALID:
                continue

            if action.Groups:
                for group in action.Groups:
                    if group not in data:
                        data[group] = list()

                    data[group].append(action.Name)

            else:
                data['Uncategorised'].append(action.Name)

        return data


# ------------------------------------------------------------------------------
class LaunchAction(object):
    """
    This is an action abstract for a launchable action
    """

    # -- These are generate attributes
    Name = ''
    Description = __doc__
    Icon = ''
    Groups = []

    # -- This allows you to re-implement the same plugin multiple
    # -- times and always get the highest priority plugin
    Version = 0
    Priority = 0

    # -- This is an enum of validity, which you should not
    # -- change, but one of these should be returned by the
    # -- viability method
    INVALID = 0
    DISABLED = 1
    VALID = 2

    STATUS_DELAY = 0

    # --------------------------------------------------------------------------
    @classmethod
    def run(cls):
        """
        This is used to initiate the default action for this plugin.
        """
        pass

    # --------------------------------------------------------------------------
    @classmethod
    def actions(cls):
        """
        This can return a dictionary of sub-actions for this plugin. The
        format of the dictionary is expected to be dict(label=callable)
        """
        return dict()

    # --------------------------------------------------------------------------
    @classmethod
    def properties(cls):
        """
        This allows plugins to utilise blind property data which may be
        utilised by different interfaces for your specific needs.

        This should return a dictionary of the form dict(prop_name=prop_value)
        """
        return dict()

    # --------------------------------------------------------------------------
    @classmethod
    def viability(cls):
        return cls.VALID

    # --------------------------------------------------------------------------
    @classmethod
    def status(cls):
        """
        This allows for important information to be passed up. Examples may be
        when a user is expected to update a tool etc.

        Returning None means the status is normal, any other value will be passed
        up to the user in whichever way is relevant for the view, therefore in most
        cases this should be a string if the status is anything other than normal.

        :return:
        """
        return None
