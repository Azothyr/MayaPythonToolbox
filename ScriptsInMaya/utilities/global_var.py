class GlobalVar:
    def __init__(self, name, globals_dict=None, **kwargs):
        if len(kwargs) != 1:
            raise ValueError("Expected exactly one keyword argument")

        self.globals_dict = globals_dict or globals()
        self._name = name
        self._value = list(kwargs.values())[0]
        self._type = type(self._value)

        self._place_in_global()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, self._type):
            raise TypeError(f"Expected type {self._type}, but got {type(new_value)}")
        self._value = new_value
        self.globals_dict[self._name] = self._value

    def __repr__(self):
        return str(self._value)

    def __iter__(self):
        if hasattr(self._value, '__iter__'):
            return iter(self._value)
        else:
            raise TypeError(f"'{type(self._value).__name__}' object is not iterable")

    def __len__(self):
        if hasattr(self._value, '__len__'):
            return len(self._value)
        else:
            raise TypeError(f"'{type(self._value).__name__}' object has no len()")

    def __getitem__(self, index):
        if isinstance(self._value, str):
            raise TypeError(f"'{type(self._value).__name__}' object is not subscriptable in this context")
        elif hasattr(self._value, '__getitem__'):
            return self._value[index]
        else:
            raise TypeError(f"'{type(self._value).__name__}' object is not subscriptable")

    def __setitem__(self, index, value):
        if hasattr(self._value, '__setitem__'):
            self._value[index] = value
            self.globals_dict[self._name] = self._value
        else:
            raise TypeError(f"'{type(self._value).__name__}' object does not support item assignment")

    def _place_in_global(self):
        if self._name not in self.globals_dict:
            self.globals_dict[self._name] = self._value

    def append(self, value):
        if isinstance(self._value, list):
            self._value.append(value)
            self.globals_dict[self._name] = self._value
        else:
            raise TypeError(f"'{type(self._value).__name__}' object has no method 'append'")
