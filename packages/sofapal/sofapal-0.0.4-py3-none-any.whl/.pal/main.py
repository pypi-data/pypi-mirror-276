import argparse
import json
import os
import urllib.request
import webbrowser
from pathlib import Path

from InquirerPy import inquirer
from InquirerPy.base.control import Choice

configs = (
    Path.home().joinpath(".pal")
    if os.path.exists(Path.home().joinpath(".pal"))
    else None
)

print(configs)


def run():
    parser = argparse.ArgumentParser(
        prog="pal",
        description="pal - A friend; a chum.",
        epilog='Use "%(prog)s {command} --help" for more information about a command.',
    )
    commands = parser.add_subparsers(dest="command", title="Available Commands")

    create = commands.add_parser(
        "create",
        help="Create project using a template",
        description="Create project using a template",
    )
    create.add_argument("-n", "--name", help="Name of the project", action="store")
    create.add_argument(
        "-e",
        "--editor",
        help="Code editor to open project with",
        choices=["zed", "code"],
        default="zed",
    )

    browse = commands.add_parser(
        "browse", help="Web related commands", description="Web related commands"
    )
    browse.add_argument("query", action="store")
    browse.add_argument(
        "-e", "--engine", help="Select engine to use", action="store_true"
    )

    weather = commands.add_parser(
        "weather", help="Weather information", description="Weather information"
    )
    weather.add_argument(
        "-l",
        "--location",
        help="Search location to get information from",
        action="store_true",
    )
    weather.add_argument(
        "-s", "--setup", help="Setup weather configuration", action="store_true"
    )

    args = parser.parse_args()

    if args.command == "create":
        name = args.name
        editor = args.editor

        if not name:
            name = inquirer.text(message="Project name:").execute()

        path = configs.joinpath("templates")

        templates = [
            Choice(
                template.name,
                name=" ".join(str(template.name).removesuffix(".sh").split("-")),
                enabled=False,
            )
            for template in path.iterdir()
        ]
        templates.append(Choice(value=None, name="Exit"))
        templating = inquirer.fuzzy(
            message="Select template:",
            choices=templates,
            default=None,
            max_height="50%",
            mandatory=True,
        ).execute()

        if templating:
            os.system(f"bash {path}/{templating} {name}")

            if not editor:
                editor = inquirer.rawlist(
                    message="Open in:",
                    choices=[
                        Choice("zed", name="Zed", enabled=True),
                        Choice("code", name="Visual Studio Code", enabled=False),
                    ],
                    cycle=False,
                    long_instruction="Select code editor to open project with.",
                ).execute()

            os.system(f"{editor} {name}")

    elif args.command == "browse":
        config = json.loads(configs.joinpath("browse.json").read_text(encoding="utf-8"))
        engines = config["engines"]
        engine = config["default"]["url"]

        if args.engine:
            searchers = [
                Choice(engine["url"], name=engine["name"]) for engine in engines
            ]
            searchers.append(Choice(value=None, name="Exit"))

            engine = inquirer.fuzzy(
                message="Select engine:",
                choices=searchers,
                default=None,
                max_height="50%",
                mandatory=True,
            ).execute()

        webbrowser.open(f'{str(engine).replace("%s", args.query)}')
    elif args.command == "weather":
        if not args.setup:
            config = json.loads(
                configs.joinpath("weather.json").read_text(encoding="utf-8")
            )
            api_key = config["api_key"]
            location = config["default"]

            def get_weather(_):
                choices = []
                result = []

                # api request to get location autocomplete here

                return result

            if args.location:
                location = inquirer.fuzzy(
                    message="Find location:",
                    choices=get_weather,
                    max_height="50%",
                    mandatory=True,
                    default=location
                    # transformer - lambada - global var - access to that and get location
                ).execute()

            with urllib.request.urlopen(
                f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=yes"
            ) as response:
                data = response.read()
                details = json.loads(data)

            print(details)
        else:

            def validate_key(key: str):
                try:
                    with urllib.request.urlopen(
                        f"http://api.weatherapi.com/v1/current.json?key={key}&q=london"
                    ) as response:
                        if response.getcode() == 200:
                            return True
                        else:
                            return False
                except:
                    return False

            # pyloader

            api_key = inquirer.secret(
                message="Api key:",
                validate=lambda key: validate_key(key),
                invalid_message="Api key not found.",
                long_instruction="Get a free api key from https://www.weatherapi.com",
                mandatory=True,
            ).execute()

            name = inquirer.text(message="Default location name:").execute()

            with urllib.request.urlopen(
                f"https://api.weatherapi.com/v1/search.json?key={api_key}&q={name}"
            ) as response:
                data = response.read()
                results = json.loads(data)

            locations = [
                Choice(
                    result["url"],
                    name=f"{result['name']} > {result['region']} > {result['country']}",
                )
                for result in results
            ]
            locations.append(Choice(value=True, name="Try again"))
            locations.append(Choice(value=None, name="Exit"))

            location = inquirer.fuzzy(
                message="Choose location:",
                choices=locations,
                max_height="50%",
                mandatory=True,
            ).execute()

            print("saved to config")

    else:
        parser.print_help()
        parser.exit()
