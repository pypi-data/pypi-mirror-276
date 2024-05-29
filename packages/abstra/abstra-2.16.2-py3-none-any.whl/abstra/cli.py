import tkinter as tk
from tkinter.filedialog import askdirectory
from typing import Optional

import fire

from abstra_internals.interface.cli.deploy import deploy
from abstra_internals.interface.cli.editor import editor
from abstra_internals.interface.cli.version import check_latest_version
from abstra_internals.settings import SettingsController


def is_headless():
    """
    Check if the application is running in a headless environment.
    """
    try:
        # Attempt to create a Tkinter window to see if it fails
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        root.update_idletasks()
        root.destroy()  # Clean up
        return False
    except tk.TclError:
        return True


def select_dir(selected_dir: Optional[str]) -> str:
    if selected_dir:
        return selected_dir
    elif is_headless():
        return "."
    else:
        selected_dir = askdirectory(initialdir=".")
        if selected_dir == "":
            print("No directory selected. Please, select a directory.")
            exit(0)
        return selected_dir


class CLI(object):
    """
    A CLI to manage your Abstra Cloud project environment.

    usage: abstra <command> <resource> [<argument> ...] [parameters]
    """

    def deploy(self, root_dir: Optional[str] = None):
        SettingsController.set_root_path(select_dir(root_dir))
        deploy()

    def version(self):
        check_latest_version()

    def editor(
        self,
        root_dir: Optional[str] = None,
        port: int = 3000,
        debug=False,
        load_dotenv=True,
        reloading=False,
    ):
        SettingsController.set_root_path(select_dir(root_dir))
        SettingsController.set_server_port(port)
        editor(
            debug=debug,
            load_dotenv=load_dotenv,
            reloading=reloading,
        )

    def serve(
        self,
        root_dir: Optional[str] = None,
        port: int = 3000,
        debug=False,
        load_dotenv=True,
        reloading=False,
    ):
        print("This command is deprecated. Please use 'abstra editor' instead.")
        self.editor(
            root_dir=root_dir,
            port=port,
            debug=debug,
            load_dotenv=load_dotenv,
            reloading=reloading,
        )


def _SeparateFlagArgs(args):
    try:
        index = args.index("--help")
        args = args[:index]
        return args, ["--help"]
    except ValueError:
        return args, []


def main():
    fire.core.parser.SeparateFlagArgs = _SeparateFlagArgs  # type: ignore
    fire.Fire(CLI)


if __name__ == "__main__":
    main()
