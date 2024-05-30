"""
Example pluigin
"""

import click


@click.command(help="This is a help string")
def joey():
    """Joey command"""
    print("My command is running!")


@click.command(help="This is a help string")
def jill():
    """Jill command"""
    print("My jILL is running!")


def something_else():
    """something else command"""
