from IPython.core.interactiveshell import InteractiveShell


def show_all_output():
    InteractiveShell.ast_node_interactivity = "all"
