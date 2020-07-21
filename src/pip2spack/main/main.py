from pip2spack.actions.action_dispatcher import ActionDispatcher


def main():
    try:
        action_dispatcher = ActionDispatcher()
        action_dispatcher.process_application()
    except ImportError as err:
        print(err)
        exit(1)


if __name__ == '__main__':
    main()
