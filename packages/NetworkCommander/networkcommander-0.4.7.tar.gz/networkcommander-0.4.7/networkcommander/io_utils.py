import sys
from typing import Iterable, TextIO, List

import typer
import yaml


def print_objects(objects: Iterable, object_name: str) -> None:
    """
    print objects in a specific format
    :param objects: the collection of the objects.
    :param object_name: the name of the objects
    """
    if not objects:
        typer.echo(f"there are 0 {object_name}")
        return

    typer.echo(f"{object_name}: ")
    number_of_objects = 0
    for obj in objects:
        number_of_objects += 1
        typer.echo(f"{str(obj)}")
    typer.echo(f"there are {number_of_objects} {object_name}")


def read_file(file: TextIO) -> List[str]:
    """
    this function reads the content of a file, cleans it and return the content of it.
    :param file: any file (for example: sys.stdin).
    :return: the lines this file contain.
    """
    user_inputs = file.readlines()
    user_inputs = [string.strip('\r\n ') for string in user_inputs]
    user_inputs = [string.replace('\4', '') for string in user_inputs]
    user_inputs = [string.replace("\26", '') for string in user_inputs]
    user_inputs = list(filter(bool, user_inputs))
    return user_inputs


def read_from_stdin():
    typer.echo("hit control-Z or control-D to continue")
    commands = read_file(sys.stdin)
    return commands


def convert_to_yaml(content: str):
    new_yaml = yaml.safe_load(content)
    return new_yaml
