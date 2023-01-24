class PathError(Exception):
    
    def __init__(self, *args: object) -> None:
        """
        Can be used when a path is invalid or incorrect
        """

        super().__init__(*args)