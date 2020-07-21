import argparse
from abc import abstractmethod


class Action:
    ACTION = None
    PARAM_NAME = None

    def __init__(self, subparsers):
        self.parser = argparse.ArgumentParser(add_help=False)
        self.fill_parser_arguments()
        self.parser.set_defaults(**{self.PARAM_NAME: self.ACTION})
        subparsers.add_parser(self.ACTION, parents=[self.parser], formatter_class=argparse.RawTextHelpFormatter)

    def fill_parser_arguments(self):
        pass

    @abstractmethod
    def process_action(self, configuration):
        pass

    def get_config(self):
        self.parser.parse_args()
