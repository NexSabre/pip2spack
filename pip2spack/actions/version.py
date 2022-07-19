from pip2spack.actions.action import Action


class ShowVersion(Action):
    ACTION = "version"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        pass

    def process_action(self, configuration):
        print("pip2spack: v1.0")
