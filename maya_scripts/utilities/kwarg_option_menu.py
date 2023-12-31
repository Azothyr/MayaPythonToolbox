class Menu:
    """
    A Menu class to manage a mapping of options and their variants to corresponding callback functions.
    This class is case-insensitive, meaning it treats all keywords (primary and variants) in lowercase.

    Attributes:
        option_mapping (dict): A dictionary mapping primary keywords to their callback functions.
        variant_mapping (dict): A dictionary mapping variant keywords to their respective primary keywords.
    """
    def __init__(self, mapping: dict[str, [list[str], callable]]):
        """
        Initializes the Menu class with a given mapping.

        The mapping should be a dictionary where each key is a primary keyword (string), and the value is a tuple
        consisting of a list of variant keywords and a callable (callback function).

        :param mapping: A dictionary of the format {primary_keyword: ([variants], callback)}.
        :raises ValueError: If the mapping is not in the expected format.
        """
        for key, val in mapping.items():
            if not isinstance(key, str):
                raise ValueError("Key in mapping must be a string.")
            if not isinstance(val, tuple) or len(val) != 2:
                raise ValueError("Value in mapping must be a tuple of (list, callable).")
            variants, callback = val
            if not isinstance(variants, list) or not all(isinstance(v, str) for v in variants):
                raise ValueError("Variants must be a list of strings.")
            if not callable(callback):
                raise ValueError("Callback must be callable.")

        self.option_mapping = {primary_keyword.lower(): callback for primary_keyword, (_, callback) in mapping.items()}
        self.variant_mapping = {}
        self.keywords = {}  # Dictionary to store primary keywords and their variants
        for primary_keyword, (variants, _) in mapping.items():
            primary_keyword = primary_keyword.lower()
            self.keywords[primary_keyword] = [variant.lower() for variant in variants]
            for variant in variants:
                variant_lower = variant.lower()
                if variant_lower in self.variant_mapping or variant_lower in self.option_mapping:
                    print(f"Variant '{variant_lower}' conflicts with an existing primary keyword or variant.")
                    continue
                self.variant_mapping[variant_lower] = primary_keyword

    def __str__(self):
        return (f"{self.__class__.__name__}"
                f"({[(kw, vars, self.option_mapping[kw]) for kw, vars in self.keywords.items()]})")

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"({[(kw, vars, self.option_mapping[kw]) for kw, vars in self.keywords.items()]!r})")

    def __call__(self, keyword, *args, **kwargs):
        """
        Allows the Menu instance to be called directly, passing a keyword to execute the corresponding callback.
        The keyword is treated in lowercase.

        :param keyword: The keyword to parse.
        :param args: Positional arguments to pass to the callback.
        :param kwargs: Keyword arguments to pass to the callback.
        """
        return self.parse_and_execute(keyword.lower(), *args, **kwargs)

    def add_option(self, primary_keyword, variants, callback):
        """
        Adds a new option with its variants and callback. The primary keyword and variants are treated in lowercase.

        :param primary_keyword: The primary keyword for the option.
        :param variants: A list of variants for the primary keyword.
        :param callback: The callback function to execute for this option.
        """
        primary_keyword = primary_keyword.lower()
        if primary_keyword in self.variant_mapping:
            raise ValueError(f"Primary keyword '{primary_keyword}' is already used as a variant.")
        self.option_mapping[primary_keyword] = callback
        for variant in variants:
            variant = variant.lower()
            if variant in self.variant_mapping:
                raise ValueError(f"Variant {variant} is already used.")
            self.variant_mapping[variant] = primary_keyword

    def parse_and_execute(self, keyword, *args, **kwargs):
        """
        Parses the keyword and executes the corresponding callback. The keyword is treated in lowercase.

        :param keyword: The keyword to parse.
        :param args: Positional arguments to pass to the callback.
        :param kwargs: Keyword arguments to pass to the callback.
        """
        primary_keyword = self.variant_mapping.get(keyword, keyword)
        callback = self.option_mapping.get(primary_keyword)
        if not callback:
            raise ValueError(f"No option found for keyword: '{keyword}'")
        return callback(*args, **kwargs)


# Example Usage
if __name__ == "__main__":
    def sample_callback(name, option):
        print(f"Callback for {name} with option {option}")

    mapping = {
        "transform": (["trans", "Tr"], sample_callback),
        "mesh": (["msh", "Ms"], sample_callback)
    }

    menu = Menu(mapping)
    # Executes sample_callback with "object_name" and "option_value"
    menu("TRANS", "object_name", "option_value")
    # Executes sample_callback with "another_object" and "another_option"
    menu("Mesh", "another_object", "another_option")