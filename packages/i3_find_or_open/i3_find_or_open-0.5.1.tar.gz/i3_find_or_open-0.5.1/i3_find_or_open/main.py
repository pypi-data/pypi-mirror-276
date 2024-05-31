"""A module that helps you bind keys to find and display, or open a window in i3wm."""

import argparse
import importlib.metadata
import re
import subprocess as sp

import i3ipc


def find_window(title: str, tree: i3ipc.con.Con, match_class=False) -> str | None:
    """Finds a window by title regex in an i3 tree.

    Args:
        title (str): A regex that describes the title of the window you are trying to
            find.
        tree (i3ipc.con.Con): A tree as returned by i3ipc.Connection().get_tree().

    Kwargs:
        match_class (bool): Find by class regex instead. Defaults to False.

    Returns:
        window (str): The workspace the window has been found on, or 'scratchpad' if the
            window is hidden. None if it doesn't exist.
    """
    for leaf in tree.scratchpad().leaves():
        if re.compile(title).match(
            leaf.window_class if match_class else leaf.window_title  # type: ignore
        ):
            return "scratchpad"
    for workspace in tree.workspaces():
        for leaf in workspace.leaves():
            if re.compile(title).match(
                leaf.window_class if match_class else leaf.window_title  # type: ignore
            ):
                return workspace.name  # type: ignore
    return None


def main():
    """Main function for binary."""
    # parse arguments
    parser = argparse.ArgumentParser(
        prog="i3-find-or-open",
        description="A command-line utility that helps you bind keys to find and display a window, or open it if there is no instance running in i3wm.",  # noqa: E501
    )
    parser.add_argument(
        "title",
        type=str,
        help="a regex that will match the window title that you are trying to find.",
    )
    parser.add_argument(
        "command",
        type=str,
        help="the command that will be run if the window is not open.",
    )
    parser.add_argument(
        "-c",
        "--match-class",
        action="store_true",
        dest="_class",
        help="match a window's class instead of its title.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=importlib.metadata.version("i3_find_or_open"),
    )
    args = parser.parse_args()

    i3 = i3ipc.Connection()

    ws = find_window(
        args.title,
        i3.get_tree(),
        match_class=args._class,
    )
    if ws is None:
        sp.run(args.command, shell=True)
    elif ws == "scratchpad":
        i3.command(
            f"[{'class' if args._class else 'title'}=\"{args.title}\"] scratchpad show"
        )
    else:
        i3.command(f"workspace {ws}")
