''' app/utils/config.py '''

config = {
    'theme': 'light'
}

class AppConfig:
    """
    Configuration File
    """
    APP_NAME: str = "ErrorLens"

    @classmethod
    def initialize(cls) -> None:
        """
        Perform any necessary initializations here, e.g.:
        - Loading settings from a file
        """
    def get_var(self) -> None:
        """
        Get the Var.
        """
