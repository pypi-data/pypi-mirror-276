"""Handle /history."""


# shows chat history
def handle_history(
    temp_file,
    messages,
    given="",
    temp_is_temp=False,
    silent=False
):
    """Handle /history.

    Command description:
        Prints the conversation history.

    Usage:
        /history
    """
    # removes linter warning about unused arguments
    if temp_file:
        pass
    if given:
        pass
    if temp_is_temp:
        pass
    if not silent:
        messages.print_history()
    return messages


item_history = {
    "fun": handle_history,
    "help": "prints the conversation history",
    "commands": ["history"],
}
