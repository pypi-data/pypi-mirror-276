"""Handle /genconf."""
from ..utils import genconfig


# generates config file
def handle_genconf(
    temp_file,
    messages,
    given="",
    temp_is_temp=False,
    silent=False
):
    """Handle /genconf.

    Command description:
        (Re)generates owega's config file.

    Usage:
        /genconf
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if given:
        pass
    if temp_is_temp:
        pass
    if silent:
        pass
    genconfig()
    return messages


item_genconf = {
    "fun": handle_genconf,
    "help": "generates a sample config file",
    "commands": ["genconf"],
}
