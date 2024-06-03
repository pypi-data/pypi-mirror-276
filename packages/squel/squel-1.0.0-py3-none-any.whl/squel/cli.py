# -*- coding: utf-8 -*-
import click

from .app import Squel


class Cli:

    @click.group()
    def main():
        pass

    @staticmethod
    @main.command()
    @click.argument('path')
    def parse(path):
        click.echo(Squel.parse(path))
