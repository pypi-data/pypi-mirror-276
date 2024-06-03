# -*- coding: utf-8 -*-
import io

from .parser import Parser


class Squel:

    @staticmethod
    def parse(path):
        with io.open(path, 'r') as file:
            source = file.read()
        return Parser().parse(source)
