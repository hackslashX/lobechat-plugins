
class InvalidEngineSettings(Exception):
    def __init__(self, class_name, error):
        message = f"Invalid settings for {class_name} engine: {error}"
        super().__init__(message)


class ErrorInEngine(Exception):
    def __init__(self, class_name, error):
        message = f"Error in {class_name} engine: {error}"
        super().__init__(message)
