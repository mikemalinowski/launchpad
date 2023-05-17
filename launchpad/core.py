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
import typing
import factories

from . import constants as c


# ------------------------------------------------------------------------------
class LaunchPad(factories.Factory):

    # --------------------------------------------------------------------------
    def __init__(self, plugin_locations: typing.List[str] = None):

        # -- Define the variable we will use to pass all our
        # -- plugin paths to
        paths = [c.LAUNCHPAD_USER_PLUGIN_DIR]

        # -- Add any user defined plugin locations
        if plugin_locations:

            # -- Quick safety check to ensure we're passing a list
            # -- of locations rather than just a single string
            if not isinstance(plugin_locations, (list, tuple)):
                plugin_locations = [plugin_locations]

            paths.extend(plugin_locations)

        # -- Add any paths defined in the environment
        if c.LAUNCHPAD_PLUGIN_ENVVAR in os.environ:
            paths.extend(
                [
                    os.path.abspath(path)
                    for path in os.environ[c.LAUNCHPAD_PLUGIN_ENVVAR].split(';')
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
    def identifiers(self, show_beta=False) -> typing.List[str]:
        """
        We overload this function because we want to omit any invalid
        actions

        :return: list(str, str, ...)
        """
        filtered_actions = list()
        all_actions = sorted(
            super(
                LaunchPad,
                self,
            ).identifiers(),
            key=lambda t: t.lower(),
        )

        for action_name in all_actions:
            action = self.request(action_name)
            action_state = action.state()

            if not show_beta and c.PluginStates.BETA in action_state:
                continue

            if action.state() == c.PluginStates.INVALID:
                continue

            filtered_actions.append(action_name)

        return filtered_actions

    # --------------------------------------------------------------------------
    def grouped_identifiers(self, show_beta=False) -> typing.Dict[str, str]:
        """
        This will create a dictionary of groups, where the keys are the groups
        defined in the actions and the values are lists of identifiers.

        :return: dict(group_name: [name, name, name]
        """
        data = {'Uncategorised': list()}

        for action in self.plugins():

            action_state = action.state()

            if not show_beta and c.PluginStates.BETA in action_state:
                continue

            # -- Ignore invalid actions
            if action.state() != c.PluginStates.INVALID:
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

    # -- This property allows a plugin to override how often the status
    # -- should be pinged. This is additive on top of the value defined
    # -- by the user in the settings. For instance, if hte user has a
    # -- status wait time of five seconds, and this is set to 1000 then this
    # -- plugin would be checked every six seconds.
    STATUS_DELAY = 0

    # --------------------------------------------------------------------------
    @classmethod
    def run(cls) -> bool:
        """
        This is used to initiate the default action for this plugin.
        """
        pass

    # --------------------------------------------------------------------------
    @classmethod
    def actions(cls) -> typing.Dict[str, callable]:
        """
        This can return a dictionary of sub-actions for this plugin. The
        format of the dictionary is expected to be dict(label=callable)
        """
        return dict()

    # --------------------------------------------------------------------------
    @classmethod
    def state(cls) -> "launchpad.PluginStates":
        return c.PluginStates.VALID

    # --------------------------------------------------------------------------
    @classmethod
    def status_message(cls) -> str or None:
        """
        This allows for important information to be passed up. Examples may be
        when a user is expected to update a tool etc.

        Returning None means the status is normal, any other value will be passed
        up to the user in whichever way is relevant for the view, therefore in most
        cases this should be a string if the status is anything other than normal.

        :return:
        """
        return None
