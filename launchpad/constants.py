import os
import enum


# -- Define the environment variable we will use when looking
# -- for plugin paths
LAUNCHPAD_PLUGIN_ENVVAR = 'LAUNCHPAD_PLUGIN_PATHS'

# -- This is a default location we always look in for user placed
# -- actions
LAUNCHPAD_USER_PLUGIN_DIR = os.path.join(
    os.path.expanduser('~'),
    '.launchpad',
)


# --------------------------------------------------------------------------------------
class PluginStates(enum.Flag):
    INVALID = enum.auto()
    DISABLED = enum.auto()
    VALID = enum.auto()
    BETA = enum.auto()
