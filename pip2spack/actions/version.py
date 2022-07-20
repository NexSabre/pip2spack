from pip2spack.actions.action import Action


class ShowVersion(Action):
    ACTION: str = "version"
    PARAM_NAME: str = "ACTION"

    def fill_parser_arguments(self):
        pass

    def process_action(self, configuration):
        print("pip2spack: v1.0")
