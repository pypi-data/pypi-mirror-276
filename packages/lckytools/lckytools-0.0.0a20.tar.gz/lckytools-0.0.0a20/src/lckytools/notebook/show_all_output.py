from IPython.core.interactiveshell import InteractiveShell


def show_all_output():
    """
    Display the output of all expressions in a Jupyter notebook cell.

    This function sets the `ast_node_interactivity` attribute of the `InteractiveShell`
    to "all", causing all expressions in a cell to be executed and their outputs displayed.

    Example:
        >>> show_all_output()
        >>> x = 10
        >>> y = 20
        >>> x + y
        30
        >>> x * y
        200
    """
    InteractiveShell.ast_node_interactivity = "all"


def show_last_output():
    """
    Display only the output of the last expression in a Jupyter notebook cell.

    This function sets the `ast_node_interactivity` attribute of the `InteractiveShell`
    to "last", causing only the last expression in a cell to be executed and its output displayed.

    Example:
        >>> show_last_output()
        >>> a = [1, 2, 3]
        >>> b = [4, 5, 6]
        >>> a
        >>> b
        >>> a + b
        [1, 2, 3, 4, 5, 6]
    """
    InteractiveShell.ast_node_interactivity = "last"
