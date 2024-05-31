import os
from pathlib import Path
from configparser import ConfigParser

DATA_PATH = Path.home().joinpath(".deary")
CONFIG_PATH = DATA_PATH.joinpath("settings.ini")

config = ConfigParser()

try:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
except OSError as e:
    print(f"Error creating directory: {e}")
else:
    try:
        with open(CONFIG_PATH, 'r') as f:
            config.read_file(f)
    except FileNotFoundError:
        try:
            CONFIG_PATH.touch()
        except OSError as e:
            print(f"Error creating file: {e}")
        else:
            config.setdefault("directory", {})
            config["directory"]["journal_directory"] = str(DATA_PATH.joinpath(""))

            with open(CONFIG_PATH, 'w') as f:
                config.write(f)

JOURNAL_DIRECTORY = Path(config.get("directory", "journal_directory"))

PASSWORD_KEY_PATH = DATA_PATH.joinpath("psk.key")

PASSWORD_MESSAGE = "LOREM IPSUM or anything I want to put here because nobody can do anything ig?\
                            but whatever this sentence need not make sense to anyone or anything."

# Define constants for password hashing
DEFAULT_ITERATIONS = 150000
PWD_ITERATIONS = 750000
PWD_MIN_LENGTH = 8

def log_action(action):
    with open(DATA_PATH.joinpath("user_actions.log"), "a") as log_file:
        log_file.write(f"{action}\n")

# log_action("User accessed deary files.")
