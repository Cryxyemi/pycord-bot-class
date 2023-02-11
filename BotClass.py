import os

import discord
from colorama import Fore

from .exceptions import LoadError, PathError


class Bot(discord.Bot):

    def __init__(
        self, 
        token: str,
        ready_event: bool,
        debug_logs: bool = False,
        *args, 
        **options
    ) -> None:
        description: str = options.get("description", None)
        super().__init__(description, *args, **options)

        self._cogs = []
        self.token = token
        self._debug = debug_logs

        # Idk if these works
        self.string_check = lambda x: isinstance(x, str)
        self.list_check = lambda x: isinstance(x, list)
        self.type_check = lambda type, x: isinstance(x, type)
        
        if ready_event:
            self.add_listener(self.connect_event, "on_connect")
            self.add_listener(self.ready_event, "on_ready")
        
    async def connect_event(self) -> None:
        print(f"Connected to discord API")
        
    async def ready_event(self) -> None:
        infos = [
            f"Pycord version: {discord.__version__}"
            f"User: {self.user.name}#{self.user.discriminator}",
            f"ID: {self.user.id}",
            f"Commands: {len(self.commands)}",
            f"Guilds: {len(self.guilds)}",
            f"Latency: {round(self.latency * 1000)}ms",
            f"Debug: {self._debug}"
        ]
        
        longest = max([str(i) for i in infos], key=len)
        longest_len = len(longest)
        print_length = 4 + longest_len
        
        print("\n")
        print(f"╔{(print_length - 2) * '═'}╗")
        
        for value in infos:
            print(f"║ {self.format_string(value, longest_len)} ║")
            
        print(f"╚{(print_length - 2) * '═'}╝")
        
        
    def registered_cogs(self) -> list:
        return self._cogs

    def exec(self) -> None:
        self._register_cogs()

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

    def _register_cogs(self) -> None:
        try:
            for cog in self._cogs:
                if self._debug:
                    print(f"{Fore.LIGHTCYAN_EX}[DEBUG] Registered cog: {cog}{Fore.RESET}")
                self.load_extension(cog)

        except Exception as e:
            raise LoadError(e)

    def format_string(self, string: str, longest: int) -> str:
        if type(string) == int:
            string = str(string)
            
        if len(string) > longest:
            return string

        return f"{string}{(longest - len(string)) * ' '}"
