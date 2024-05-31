from select import select
import click
import datetime
from functools import update_wrapper
from .diary import encryption
from .diary.config import PWD_ITERATIONS, PASSWORD_MESSAGE, DATA_PATH, PWD_ITERATIONS, PWD_MIN_LENGTH, FILES_PATH, PASSWORD_KEY_PATH
from pathlib import Path
import os
from tabulate import tabulate

EXIT = ['quit', 'exit', 'q']
FILE_NAME_FORMAT = "%Y-%m-%d_%H-%M-%S"

def format_timedelta(td):
  minutes, _ = divmod(td.seconds, 60)
  hours, minutes = divmod(minutes, 60)
  return f"{td.days}d {hours:02d}h {minutes:02d}m"


def prompt_for_existing_password():
    """Prompt for an existing password."""
    while True:
        password_input = click.prompt("Password", type=str, hide_input=True)
        if validate_password(password_input, PASSWORD_KEY_PATH):
            click.echo("Yippie correct password!!\n")
            return password_input
        else:
            click.echo("Wrong Password!!")

def prompt_for_new_password():
    """Prompt for a new password."""
    while True:
        password_input = click.prompt(
            "Create a new password", type=str, hide_input=True, confirmation_prompt=True)
        if len(password_input) < PWD_MIN_LENGTH:
            click.echo(
                f"Whoops. The password must be at least {PWD_MIN_LENGTH} {'characters' if PWD_MIN_LENGTH > 1 else 'character'} long.")
        else:
            return password_input

def ask_psk(f):
    """Decorator to prompt for a password before invoking the decorated function."""
    @click.pass_context
    def wrapper(ctx, *args, **kwargs):
        password = None
        
        if PASSWORD_KEY_PATH.exists():
            password = prompt_for_existing_password() 
        else:
            click.echo("No existing password found.")
            password = prompt_for_new_password()
            
        # Encrypt the verification message using the password and save it to the password file
        encrypted_verify_msg = encryption.encrypt_message(PASSWORD_MESSAGE, password, PWD_ITERATIONS)
        PASSWORD_KEY_PATH.write_bytes(encrypted_verify_msg)

        return ctx.invoke(f, password, *args, **kwargs)

    return wrapper

def validate_password(test_password, password_path):
    """
    Validate the provided password against the stored password token.
    """
    return encryption.decrypt_message(password_path.read_bytes(), test_password) == PASSWORD_MESSAGE


def get_files(path):
  return sorted(path.glob("*.deary.md"))


def ll(directory_path, numbered=False):
    if not directory_path.exists():
        click.echo("No files found in the specified directory.")
        return []

    files = sorted(file for file in directory_path.glob("*.deary.md") if file.is_file())

    if numbered:
        click.echo("ID\tNAME")
        click.echo("--------------------------------------------")
        for idx, name in enumerate(files, start=1):
            click.echo(f"{idx}\t{name.name}")
    # else:
    #     click.echo("NAME")
    #     click.echo("--------------------------------------------")
    #     for file in files:
    #         click.echo(file.name)

    return files

def select_file():
    files = ll(FILES_PATH, numbered=True)
    while True:
        selected = input("Enter the ID number of the day or enter 'q' to exit: ").lower()

        if selected in EXIT:
            return None

        selected_id = None
        try:
            selected_id = int(selected) - 1
            if selected_id < 0 or selected_id >= len(files):
                raise ValueError("There exists no such ID!!\n")
        except ValueError:
            click.echo("There exists no such ID!!\n")
            continue

        return files[selected_id]

@click.group()
def cli():
  """
  Encrypted deary
  """
  # Create data directory if it doesn't already exist
  if not DATA_PATH.exists():
    DATA_PATH.mkdir()

@cli.command(name="list")
def list_cmd():
#   """
#   List all deary files
#   """
  ll(FILES_PATH, True)


@cli.command(name="info")
def info_option():
    files = get_files(FILES_PATH)
    if not files:
        click.echo("No files found.")
        return

    deltas = []
    for i in range(len(files) - 1):
        e0 = files[i]
        e1 = files[i + 1]
        try:
            date0 = datetime.datetime.strptime(e0.stem[:-6], FILE_NAME_FORMAT)
            date1 = datetime.datetime.strptime(e1.stem[:-6], FILE_NAME_FORMAT)
            d = date1 - date0
            deltas.append(d.total_seconds())
        except ValueError:
            # Handle invalid date format
            click.echo(f"Invalid date format for files: {e0.name} or {e1.name}")

    if deltas:
        d_avg = datetime.timedelta(seconds=sum(deltas) / len(deltas))
    else:
        d_avg = datetime.timedelta(seconds=0)

    try:
        newest_date = datetime.datetime.strptime(files[-1].stem[:-6], FILE_NAME_FORMAT)
    except ValueError:
        newest_date = "No files"

    try:
        oldest_date = datetime.datetime.strptime(files[0].stem[:-6], FILE_NAME_FORMAT)
    except ValueError:
        oldest_date = "No files"

    total_size = sum(day.stat().st_size for day in files)

    # Author Information
    # Assuming author information is stored in the environment variable
    author_info = os.getenv("AUTHOR_INFO", "Unknown")

    # Prepare data for the table
    table_data = [
        ["Password set", PASSWORD_KEY_PATH.exists()],
        ["Deary path", FILES_PATH.resolve()],
        ["Number of files", len(files)],
        ["Avg time between files", format_timedelta(d_avg)],
        ["Newest File Date", newest_date],
        ["Oldest File Date", oldest_date],
        ["Total Storage Size", f"{total_size} bytes"],
        ["Author Information", author_info]
    ]

    # Print the table
    click.echo(tabulate(table_data, headers=["Property", "Value"], tablefmt="grid"))


@cli.command(name="create")
@ask_psk
def create_cmd(pwd):
    """
    Create a new encrypted deary day
    """
    FILES_PATH.mkdir(parents=True, exist_ok=True)

    # Open text editor for user to enter deary data
    file_contents = click.edit(require_save=True)
    if file_contents is None:
        click.echo("Cancelled deary creation")
        return

    file_size = file_contents.encode("utf-8")

    file_name = datetime.datetime.utcnow().strftime(FILE_NAME_FORMAT).replace(':', '-')
    new_path = FILES_PATH.joinpath(file_name + '.deary.md')

    # Check if a day with the same name already exists
    if new_path.exists():
        click.echo(f"Unable to save the deary. A day with the name '{file_name}' is already present.")
        return

    # Encrypt text and save to file
    encrypted_content = encryption.encrypt_message(file_size, pwd)
    new_path.write_bytes(encrypted_content)

    click.echo(f"New day in deary successfully written at:\n{new_path}")

@cli.command(name="edit")
@ask_psk
def edit_cmd(pwd):
    """
    Edit an existing deary day. Overwrites data in the original day.
    """
    click.echo("Pick a file to edit:\n")
    file_path = select_file()
    if file_path is None:
        return

    try:
        file_size = file_path.read_bytes()
    except Exception as e:
        click.echo(f"ERROR: Unable to open file. {e}")
        return

    try:
        og_data = encryption.decrypt_message(file_size, pwd)
    except Exception as e:
        click.echo(f"ERROR: Failed to decrypt the file. {e}")
        return

    new_data = click.edit(text=og_data, require_save=True)
    if new_data is None:
        click.echo(f"\nNo changes were made to the deary '{file_path.name}'")
        return

    encrypted_content = encryption.encrypt_message(new_data.encode("utf-8"), pwd)
    file_path.write_bytes(encrypted_content)

    click.echo(f"\nChanges to the deary file '{file_path.name}' saved successfully!")

@cli.command(name="read")
@ask_psk
def read_cmd(pwd):
    """
    Decrypt and read a deary file
    """
    while True:
        click.echo("Pick a day to read:\n")
        file_path = select_file()
        if file_path is None:
            break

        try:
            file_size = file_path.read_bytes()
        except Exception as e:
            click.echo(f"ERROR: Unable to open file. {e}")
            continue

        try:
            data = encryption.decrypt_message(file_size, pwd)
        except Exception as e:
            click.echo(f"ERROR: Failed to decrypt the file. {e}")
            continue

        click.edit(
            text="NOTE: This is just a dummy file, changing data in this won't affect the original file even though you have edit access of this file.\nIf you want to edit, use the edit option."
                 + "\n------------------------------------\n\n" + data
        )



@cli.command(name="delete")
@ask_psk
@click.argument('password')
def delete_cmd(password):
    """
    Delete an existing deary file.
    """
    click.echo("\nThis is not your usual blah-blah, this operation is irreversible and will permanently delete this file.\n\nYOU WON'T BE ABLE TO RECOVER THE FILES AGAIN!!\n")
    click.echo("Pick a file to delete:\n")
    file_path = select_file()
    if file_path is None:
        return
    try:
        # Attempt to remove the selected dearyday
        file_path.unlink()
        click.echo(f"File '{file_path.name}' has been deleted successfully!")
    except Exception as e:
        click.echo(f"Error deleting the day: {e}")

