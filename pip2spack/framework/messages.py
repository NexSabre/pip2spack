from typing import List


class Messages:
    @staticmethod
    def package_availability(available: List, unavailable: List):
        Messages.info("Package status")
        if available:
            print("Available:")
            for key in available:
                print(f"\t{key}")

        packages_not_found = unavailable
        if not packages_not_found:
            print()
            return

        print("\nUnavailable:")
        for p in packages_not_found:
            print(f"\t{p}")
        else:
            print()

    @staticmethod
    def error(message):
        print(f"ERRO :: {message}")

    @staticmethod
    def warn(message):
        print(f"WARN :: {message}")

    @staticmethod
    def info(message):
        print(f"INFO :: {message}")

    @staticmethod
    def ok(message):
        print(f" OK  :: {message}")

    @staticmethod
    def clean(message):
        print(f"     :: {message}")
