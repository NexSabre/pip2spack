from argparse import ArgumentParser

from pip2spack.actions.create.create_action import CreateAction
from pip2spack.actions.update.update_action import UpdateAction
from pip2spack.actions.version import ShowVersion
from pip2spack.framework.messages import Messages


class ActionDispatcher:
    ACTION_HANDLERS = [CreateAction, ShowVersion, UpdateAction]

    def __init__(self):
        self.parser = ArgumentParser()
        subparsers = self.parser.add_subparsers()
        self.action_handlers = {action_handler.ACTION: action_handler(subparsers) for action_handler in
                                self.ACTION_HANDLERS}

    def process_application(self):
        configuration = self.parser.parse_args()
        try:
            self.action_handlers[configuration.ACTION].process_action(configuration)
        except AttributeError:
            Messages.clean("pip2spack ::")
            Messages.clean("quick tool for pip -> spack package conversion\n")
            Messages.clean("Choose operation:"
                           "\n\t\t - create -- for creation a new package"
                           "\n\t\t - update -- for update a existing package.py")
            Messages.clean("")
            Messages.info("All information are base on the pypi.org")
