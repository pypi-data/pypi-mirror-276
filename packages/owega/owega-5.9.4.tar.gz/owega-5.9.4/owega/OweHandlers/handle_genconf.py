"""Handle /genconf."""
from ..utils import genconfig
from ..conversation import Conversation


# generates config file
def handle_genconf(
    temp_file: str,
    messages: Conversation,
    given: str = "",
    temp_is_temp: bool = False,
    silent: bool = False
) -> Conversation:
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
