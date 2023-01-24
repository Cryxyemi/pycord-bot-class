import os
import discord
from colorama import Fore

from .exceptions import LoadError, PathError


class Bot(discord.Bot):

    def __init__(
        self, 
        token: str,
        debug_logs: bool = False,
        description = None, 
        *args, 
        **options
    ) -> None:
        super().__init__(description, *args, **options)

        self._cogs = []
        self.token = token
        self._debug = debug_logs

        self.string_check = lambda x: isinstance(x, str)
        self.list_check = lambda x: isinstance(x, list)
        self.type_check = lambda type, x: isinstance(x, type)

    def registered_cogs(self) -> list:
        return self._cogs

    def exec(self) -> None:
        self._register_cogs(self._cogs)

        self.run(self.token)

    def load_dir(self, dir: str) -> None:
        if not self.string_check(dir):
            raise TypeError(f"{Fore.LIGHTRED_EX}[ERROR] dir is not a string (str){Fore.RESET}")

        try:
            for item in os.scandir(dir):
                if item.is_dir():
                    if self._debug:
                        print(f"{Fore.LIGHTCYAN_EX}[DEBUG] skipped {item.name} due its a folder{Fore.LIGHTCYAN_EX}")
                    else:
                        pass

                if item.is_file():
                    if item.name.endswith('.py'):
                        if self._debug:
                            print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Found cog: {item.name}{Fore.RESET}")

                        self._cogs.append(item.path)
        except FileNotFoundError:
            raise PathError(f"{Fore.LIGHTRED_EX}[ERROR] Your entered path is not valid, check if the directory exists{Fore.RESET}")

    def load_subdir(self, root_dir: str) -> None:
        if not self.string_check(root_dir):
            raise TypeError(f"{Fore.LIGHTRED_EX}[ERROR] root_dir is not a string (str){Fore.RESET}")

        try:
            for sub in os.scandir(root_dir):
                if sub.is_dir():
                    for item in os.scandir(sub.path):
                        if item.is_file():           
                            if item.name.endswith('.py'):
                                if self._debug:
                                    print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Found cog: {root_dir}.{sub.name}.{item.name[:-3]}{Fore.RESET}")

                                self._cogs.append(f"{root_dir}.{sub.name}.{item.name[:-3]}")
        except FileNotFoundError:
            raise PathError(f"{Fore.LIGHTRED_EX}[ERROR] Your entered path is not valid, check if the directory exists{Fore.RESET}")

    def add_static_cogs(self, cogs: list) -> None:
        if not self.list_check(cogs):
            raise TypeError(f"{Fore.LIGHTRED_EX}[ERROR] cogs: {cogs} are not a or in an Array (List){Fore.RESET}")

        for i in cogs:
            if self._debug:
                print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Added cog: {i}{Fore.RESET}")

            self._cogs.append(i)

    def unload_cog(self, name: str) -> None:
        try:
            if self._debug:
                print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Unloaded cog: {name}{Fore.RESET}")

            index = self._cogs.index(name)
            self._cogs.pop(index)

        except ValueError:
            raise ValueError(f"{Fore.LIGHTRED_EX}[ERROR] {name} not found{Fore.RESET}")

    def unload_cogs(self) -> None:
        if self._debug:
            print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Cleared cogs{Fore.RESET}")

        self._cogs.clear()

    def _register_cogs(self, cogs: list) -> None:
        try:
            for cog in self._cogs:
                if self._debug:
                    print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Registered cog: {cog}{Fore.RESET}")
                self.load_extension(cog)

        except Exception as e:
            raise LoadError(e)
