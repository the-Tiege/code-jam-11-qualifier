"""
qualifier.py

This module contains my solution to code-jam-11-qualifier.

"""

from enum import auto, StrEnum
import re
import warnings

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    """
    Enum containing different quote modes
    """
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""

# Implement the class and function below


class Quote:
    """
    Quote class is used to create quotes and modify them based on 
    entered commands.

    Attributes:
        quote (str): A string containing the entered quote
        mode (Variant): An enum used to dictate quote formatt.
    """
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        """
        Initializes Quote with specified transformation.
        """
        self.mode = mode
        self.quote = quote
        self.quote = self._create_variant()

    def __str__(self) -> str:
        """
        String representation of quote
        """
        return self.quote

    def _quote_to_piglatin(self) -> str:
        """
        Transforms quote to piglatin formatt
        """
        piglatin_list = []
        for word in self.quote.split(" "):
            piglatin_list.append(self._word_to_piglatin(word))

        piglatin_quote = " ".join(piglatin_list)

        if len(piglatin_quote) > MAX_QUOTE_LENGTH:
            raise ValueError("Quote was not modified")

        return piglatin_quote

    def _word_to_piglatin(self, word) -> str:
        """
        Transforms word to piglatin.
        """
        vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']

        upper_case = word[0].isupper()

        if word[0] in vowels:
            word = word + "way"
        else:
            cluster = ""
            index = 0
            for letter in word:
                if letter in vowels:
                    break
                cluster += letter
                index += 1
            word = word[index:] + cluster.lower() + "ay"

        if upper_case:
            word = word[0].upper() + word[1:]

        return word

    def _quote_to_uwu(self) -> str:
        """
        Transforms quote to uwu formatt
        """
        uwu_quote = ""

        if re.search('[lLrRuU]', self.quote):

            uwu_quote = re.sub(r'[lr]', 'w', self.quote)
            uwu_quote = re.sub(r'[LR]', 'W', uwu_quote)

            temp_quote = ""
            words = []
            for word in uwu_quote.split(" "):
                words.append(self._word_starts_with_u(word))

            temp_quote = " ".join(words)

            if len(temp_quote) < MAX_QUOTE_LENGTH:
                uwu_quote = temp_quote
            else:
                warnings.warn("Quote too long, only partially transformed")

        else:
            raise ValueError("Quote was not modified")

        return uwu_quote

    def _word_starts_with_u(self, word: str) -> str:
        """
        Handles case where word starts with a u 
        in uwu transform.
        """
        if word[0] in ['u', 'U']:
            word = f"{word[0]}-{word}"
        return word

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant 
        indicated by `self.mode` and returns the result
        """
        if self.mode == VariantMode.NORMAL:
            return self.quote
        if self.mode == VariantMode.PIGLATIN:
            return self._quote_to_piglatin()
        if self.mode == VariantMode.UWU:
            return self._quote_to_uwu()
        raise ValueError("Unknown Variant")

def get_commands(command:str) -> list[str]:
    """
    Gets commands from input command string.

    Arguments:
        command (str): string containing commands

    Returns:
        list[str]: list of commands extracted from input
    """
    if "uwu" in command or "piglatin" in command:
        return command.split(" ", maxsplit=2)
    return command.split(" ", maxsplit=1)

def list_quotes() -> None:
    """
    Lists quotes stored in Database
    """
    quote_list = []
    for quote_db in Database.get_quotes():
        quote_list.append(f"- {quote_db}")
    quotes = "\n".join(quote_list)
    print(quotes)

def get_quote_and_mode(commands:list[str]) -> tuple[str, VariantMode]:
    """
    Gets quote and mode commands list.

    Arguments:
        commands (list[str]): list of commands

    Returns:
        tuple[str, VariantMode]: tuple of extracted quote and mode
    """
    if len(commands) == 2 and (commands[1].startswith('"') or commands[1].startswith('“')):
        return commands[1], VariantMode.NORMAL
    if commands[1] == "uwu":
        return commands[2], VariantMode.UWU
    if commands[1] == "piglatin":
        return commands[2], VariantMode.PIGLATIN

    raise ValueError("Invalid command")


def add_quote(commands:list[str]) -> None:
    """
    Adds quote to Database

    Arguments:
        commands (list[str]): list of commands
    """
    quote, mode = get_quote_and_mode(commands)

    quote = quote.strip('"').strip('“').strip('”')

    if len(quote) > MAX_QUOTE_LENGTH:
        raise ValueError("Quote is too long")

    try:
        new_quote = Quote(quote=quote, mode=mode)
        Database.add_quote(new_quote)
    except DuplicateError:
        print("Quote has already been added previously")


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """
    commands = get_commands(command)

    if commands[0] != "quote" or len(commands) < 2 or len(commands) > 3:
        raise ValueError("Invalid command")

    if commands[1] == "list":
        list_quotes()
    else:
        add_quote(commands)

# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    """
    Database to contain quotes
    """
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
