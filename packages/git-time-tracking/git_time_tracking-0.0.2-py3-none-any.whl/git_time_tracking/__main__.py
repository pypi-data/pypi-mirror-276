import argparse
import datetime
import subprocess
from pathlib import Path

from .utils import (CONFIG_PATH, SETTINGS, SETTINGS_EXISTED, console,
                    load_config, save_config)


def configure():
    save_config()
    subprocess.call(['nano', str(CONFIG_PATH)])
    load_config()


def main():
    # get the user input
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="The date to get the logs for", nargs="?", const=None)
    parser.add_argument("--author", help="The author to get the logs for", nargs="?", const=None)
    parser.add_argument("--config", action=argparse.BooleanOptionalAction, help="Configure the settings")
    args = parser.parse_args()

    if not SETTINGS_EXISTED or args.config:
        configure()

    parsed_date = raw_date = args.date.replace("date=", "") if args.date is not None else datetime.datetime.now().strftime(SETTINGS["date_format"])
    try:
        date = datetime.datetime.strptime(raw_date, SETTINGS["date_format"]).date()
        parsed_date = date.strftime("%Y-%m-%d")
    except ValueError as e:
        pass
    
    if SETTINGS["git_author"] is None:
        SETTINGS["git_author"] = console.input("Whats your name? ").strip()
        
    parsed_author = (args.author or SETTINGS["git_author"]).replace("'", "")
    pretty_author = parsed_author if not SETTINGS["censor_author"] else "*" * len(parsed_author)

    console.print("date:\t", parsed_date, style="bold")
    console.print("author:\t", pretty_author, style="bold")

    # build the command
    command = "git log --format=short --author='{}' --since='{} 00:00' --until='{} 23:59'".format(parsed_author, parsed_date, parsed_date)
    console.print()
    console.print(command)

    # run the command in every git directory
    for path in SETTINGS["git_directories"]:
        path = path.strip()

        console.print()
        console.print(path, style="bold")
        console.print()
    
        subprocess.run(command, shell=True, cwd=path)



if __name__ == "__main__":
    main()
