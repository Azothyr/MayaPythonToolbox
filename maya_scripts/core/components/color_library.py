class ColorIndex:
    def __init__(self):
        self.__name = 'Color Library'
        self.library = [
            ('Maya Default Blue', 0, (0, 0, 255)),
            ('Black', 1, (0, 0, 0)),
            ('White', 16, (255, 255, 255)),
            ('Light Grey', 3, (211, 211, 211)),
            ('Dark Grey', 2, (105, 105, 105)),
            ('Red', 13, (255, 0, 0)),
            ('Dark Red', 4, (139, 0, 0)),
            ('Light Pink', 20, (255, 182, 193)),
            ('Mid Pink', 31, (255, 105, 180)),
            ('Pink', 9, (255, 192, 203)),
            ('Light Yellow', 22, (255, 255, 224)),
            ('Yellow', 17, (255, 255, 0)),
            ('Dark Yellow', 25, (204, 204, 0)),
            ('Light Orange', 21, (255, 165, 0)),
            ('Dark Orange', 12, (255, 140, 0)),
            ('Light Green', 27, (144, 238, 144)),
            ('Green', 23, (0, 128, 0)),
            ('Dark Green', 7, (0, 100, 0)),
            ('Light Neon Green', 19, (50, 205, 50)),
            ('Neon Green', 14, (57, 255, 20)),
            ('Dark Neon Green', 26, (34, 139, 34)),
            ('Neon Blue', 18, (70, 130, 180)),
            ('Light Navy Blue', 28, (100, 149, 237)),
            ('Navy Blue', 15, (0, 0, 128)),
            ('Light Blue', 29, (173, 216, 230)),
            ('Blue', 6, (0, 0, 255)),
            ('Dark Blue', 5, (0, 0, 139)),
            ('Light Purple', 30, (147, 112, 219)),
            ('Dark Purple', 8, (128, 0, 128)),
            ('Light Brown', 10, (181, 101, 29)),
            ('Brown', 11, (139, 69, 19)),
            ('Golden Brown', 24, (218, 165, 32))
        ]
        self.color_order = [item[0] for item in self.library]
        self.cvalue_order = [item[1] for item in self.library]
        self.rgb_order = [item[2] for item in self.library]

    def __str__(self): return self.__name

    def __repr__(self):
        formatted_return = ",\n".join(f"{color}:\nMaya Index -> {cvalue}/31\n RGB value -> {rgb}"
                                      for color, cvalue, rgb in self.library)
        return formatted_return

    def get_color_order(self) -> list[str]: return self.color_order

    def get_cvalue_order(self) -> list[int]: return self.cvalue_order

    def get_rgb_order(self) -> list[tuple[int, int, int]]: return self.rgb_order

    def get_color_from_cvalue(self, _num: int) -> str:
        assert isinstance(_num, int), "Expected _num to be a integer"
        return self.color_order[self.cvalue_order.index(_num)]  # noqa

    def get_cvalue_from_color(self, _color: str) -> int:
        assert isinstance(_color, str), "Expected _color to be a string"
        _color = _color.title()
        return self.cvalue_order[self.color_order.index(_color)]

    def get_color_from_index(self, _index: int) -> str:
        assert isinstance(_index, int), "Expected _index to be a integer"
        return self.color_order[_index]

    def get_cvalue_from_index(self, _index: int) -> int:
        assert isinstance(_index, int), "Expected _index to be a integer"
        return self.cvalue_order[_index]

    def get_rgb_from_index(self, _index: int) -> tuple:
        assert isinstance(_index, int), "Expected _index to be a integer"
        return self.rgb_order[_index]


if __name__ == "__main__":
    library = ColorIndex()
    print(library)
    print(library.get_color_from_cvalue(1))
    print(library.get_cvalue_from_color("Black"))
    print(library.get_cvalue_from_color("white"))
    print(library.get_cvalue_from_color("wHiTe"))
    print(library.get_color_from_index(1))
    print(library.get_cvalue_from_index(1))
    print(library.get_rgb_from_index(1))
