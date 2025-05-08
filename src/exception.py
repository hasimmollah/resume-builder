class MissingJobDescriptionError(Exception):
    def __init__(self, message="Job description is required but not provided"):
        super().__init__(message)

class MissingPromptDataError(Exception):
    def __init__(self, message="Prompt Data is required but not provided"):
        super().__init__(message)
