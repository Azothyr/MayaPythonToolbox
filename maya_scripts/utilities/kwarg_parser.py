class Parser:
    """
    A utility class for parsing keyword arguments (kwargs) and extracting a value based on a list of potential keys (options).
    """

    def __init__(self, options: list, default_value: str | None = None, **kwargs):
        if not isinstance(options, list):
            raise ValueError("Options must be a list.")
        self.options = options
        self.default = default_value
        self.kwargs = kwargs

    def __call__(self) -> str:
        return self.get()

    def __str__(self):
        return f"{self.__class__.__name__}({self.options}, {self.default}, {self.kwargs})"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.options!r}, {self.default!r}, **{self.kwargs!r})"

    def get(self) -> str:
        return self._extract_value_from_kwargs(self.options, self.kwargs, self.default)

    @staticmethod
    def _extract_value_from_kwargs(options: list, kwargs: dict, default: str | None = None) -> str:
        """
        Fetches the first found expected variant parameter names from provided kwargs or returns user-defined `default`
         or None if not found.

        REQUIRED
        :param options: A list of expected variant parameter names.
        :param kwargs: A dictionary of keyword arguments.
        OPTIONAL
        :param default: The default value to return if no variant parameter names are found.

        :return: The attribute name or user-defined `default` or None if not found.
        """
        return next((kwargs[key] for key in options if key in kwargs), default)


if __name__ == "__main__":
    # printing the __repr__ of the Parser class
    print(Parser(["attribute", "attr", "at", "a"], attribute="test1", attr="test2", at="test3",
                 default_value="MISSING").__repr__())
    # printing the __str__ of the Parser class
    print(Parser(["attribute", "attr", "at", "a"], attribute="test1", attr="test2", at="test3",
                 default_value="MISSING"))
    # printing the explicit __call__ of the Parser class
    print(Parser(["attribute", "attr", "at", "a"], attribute="test1", attr="test2", at="test3",
                 default_value="MISSING")())
