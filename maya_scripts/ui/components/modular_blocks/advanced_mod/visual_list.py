import maya.cmds as cmds
from ui.components.modular_blocks import FrameBase


class MainUI(FrameBase):
    def __init__(self, parent_ui: str, name: str, mode_callbacks: dict, text_format: str = "{}",
                 **kwargs):
        """
        Initializes a BaseUI class that handles custom actions for creating and handling a frame layout in maya with
        the specified parameters and optional keyword arguments.

        :type parent_ui: Str
        :param parent_ui: The parent UI element name.
        :type frame_name: Str
        :param frame_name: The name of the frame.
        :type mode_callbacks: Dict
        :param mode_callbacks: A dictionary of mode names and their corresponding callback functions.
        :type kwargs: Dict
        :param kwargs: A dictionary of additional keyword arguments:
        :keyword text_format: The format string for the text to be displayed in the list.\n
        :keyword label (str): The label text of the frame. Defaults to the readable name of the frame.:
        :keyword radio_label (str): The label text of the radio button group. Defaults to 'Add Mode:'.
        :keyword font (str): Font style for the label. Default is 'smallPlainLabelFont'.
        :keyword width (int): Width of the frame. Default is 300.
        :keyword height (int): Height of the frame. Default is 300.
        :keyword border (bool): Whether to show a border. Default is True.
        :keyword marginWidth (int): The width of the margin. Default is 5.
        :keyword marginHeight (int): The height of the margin. Default is 5.
        :keyword visible (bool): Whether the frame is visible. Default is True.
        :keyword collapsable (bool): Whether the frame is collapsible. Default is False.
        :keyword collapsed (bool): Whether the frame starts off collapsed. Default is False.
        :keyword color (list[float]): Background color of the label. Default is [0.5, 0.5, 0.5].
        :keyword annotation (str): Annotation for the frame. Default is an empty string.
        :keyword add_callback: A callback function to be executed when the add button is pressed.
        :keyword create (bool): Whether to create the frame on initialization. Default is False.

        :return: None
        """
        # Variables
        self.list = []
        self.__mode_callbacks = mode_callbacks
        self.text_format = text_format
        self.name = self._parse_init_name(name, before_super=True)
        self.radio_label = kwargs.get("radio_label", kwargs.get("r_label", kwargs.get("rl", "Add Mode:")))

        # Sub UIs
        self.add_opt_section = f"{self.name}_add_section"
        self.add_selection = f"{self.name}_add_mode"
        self.upper_button_grp = f"{self.name}_upper_buttons"
        self.upper_button_col1 = f"{self.name}_upper_buttons_col1"
        self.upper_button_col2 = f"{self.name}_upper_buttons_col2"
        self.upper_button_col3 = f"{self.name}_upper_buttons_col3"
        self.list_visual = f"{self.name}_list_vis"
        self.lower_button_grp = f"{self.name}_lower_buttons"
        self.lower_button_col1 = f"{self.name}_lower_buttons_col1"
        self.lower_button_col2 = f"{self.name}_lower_buttons_col2"

        # Sub UI Components
        self.input_columns = f"{self.name}_columns"
        self.list_label = f"{self.name}"
        self.count = "(%i):" % len(self.list)
        self.list_name = f"{self.name}_list"
        self.add_button = f"{self.name}_add"
        self.remove_button = f"{self.name}_remove"
        self.clear_button = f"{self.name}_clear"
        self.move_up_button = f"{self.name}_move_up"
        self.move_down_button = f"{self.name}_move_down"

        self.add_callback = kwargs.get("add_callback", kwargs.get("add_cb", kwargs.get("acb", None)))

        super_args = [parent_ui, name]
        super().__init__(*super_args, **kwargs)

    def __call__(self):
        return self.list

    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __setitem__(self, key, value):
        self.list[key] = value

    def __len__(self):
        return len(self.list)

    @property
    def mode_callbacks(self):
        return self.__mode_callbacks

    @mode_callbacks.setter
    def mode_callbacks(self, options):
        self.__mode_callbacks = options
        self.update_callbacks(options)

    def get(self):
        return self.list

    def insert(self, index, value):
        self.list.insert(index, value)

    def pop(self, index=-1):
        return self.list.pop(index)

    def _create_frame(self):
        super()._create_frame()

    def _setup_main_ui(self):
        _3_col_width = self.width / 3
        _2_col_width = self.width / 2

        cmds.rowColumnLayout(self.add_opt_section, adjustableColumn=1, parent=self.frame)
        cmds.rowLayout(self.upper_button_grp, numberOfColumns=3, adjustableColumn=[1, 2, 3],
                       enable=True, parent=self.frame)
        cmds.columnLayout(self.list_visual, adjustableColumn=1, parent=self.frame)
        cmds.rowLayout(self.lower_button_grp, numberOfColumns=2, adjustableColumn=[1, 2, 3],
                       enable=True, parent=self.frame)

        cmds.columnLayout(self.upper_button_col1, adjustableColumn=True, parent=self.upper_button_grp)
        cmds.columnLayout(self.upper_button_col2, adjustableColumn=True, parent=self.upper_button_grp)
        cmds.columnLayout(self.upper_button_col3, adjustableColumn=True, parent=self.upper_button_grp)

        cmds.columnLayout(self.lower_button_col1, adjustableColumn=True, parent=self.lower_button_grp)
        cmds.columnLayout(self.lower_button_col2, adjustableColumn=True, parent=self.lower_button_grp)

    def _setup_ui_components(self):
        self.add_selection = cmds.radioButtonGrp(label=self.radio_label, bgc=[.3, 0, .3], parent=self.add_opt_section)
        self.update_callbacks(self.mode_callbacks)
        self.add_button = cmds.button(
            label="Add", command=self._add_mode_query, backgroundColor=[0, 0, 0], parent=self.upper_button_col1)
        self.remove_button = cmds.button(self.remove_button,
                                         label="Remove", command=self._remove, backgroundColor=[0, 0, 0],
                                         parent=self.upper_button_col2)
        self.clear_button = cmds.button(self.clear_button,
                                        label="Clear", command=self.clear, backgroundColor=[0, 0, 0],
                                        parent=self.upper_button_col3)
        cmds.text(self.list_label, label=f"{self.readable_name} {self.count}", align="center", parent=self.list_visual)
        cmds.textScrollList(self.list_name, numberOfRows=6, allowMultiSelection=True, parent=self.list_visual)
        self.move_up_button = cmds.button(self.move_up_button,
                                          label="Move Up", command=self._move_up, backgroundColor=[0, 0, 0],
                                          parent=self.lower_button_col1)
        self.move_down_button = cmds.button(self.move_up_button,
                                            label="Move Down", command=self._move_down, backgroundColor=[0, 0, 0],
                                            parent=self.lower_button_col2)

    def update_callbacks(self, options: dict):
        if options and options != {}:
            if len(options) != len(self.mode_callbacks):
                raise ValueError("The number of options must match the number of mode callbacks.")
            self.add_opt_section = cmds.rowColumnLayout(self.add_opt_section, edit=True, numberOfColumns=len(options))
            kws = {f"labelArray{len(options)}": tuple(options.keys()), "numberOfRadioButtons": len(options),
                   "select": 1, "parent": self.add_opt_section}
            self.add_selection = cmds.radioButtonGrp(self.add_selection, edit=True, **kws)

        else:
            return

    def _add_mode_query(self, *_):
        selected_index = cmds.radioButtonGrp(self.add_selection, query=True, select=True)
        mode_name = list(self.mode_callbacks)[selected_index - 1]  # Adjust for 1-based index
        callback_func = self.mode_callbacks[mode_name]
        callback_func()
        if self.add_callback:
            self.add_callback()

    def _update_list_to_ui(self, *_):
        self.count = "(%i):" % len(self.list)
        cmds.text(self.list_label, edit=True, label=f"{self.readable_name} {self.count}")
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        for i, item in enumerate(self.list):
            list_text = self.text_format.format(*item)
            cmds.textScrollList(self.list_name, edit=True, append=f"{i + 1}: {list_text}")

    def _get_selected_index(self):
        selected_items = cmds.textScrollList(self.list_name, query=True, selectIndexedItem=True)
        if selected_items:
            return selected_items[0]
        return None

    def _move_up(self, *_):
        index = self._get_selected_index()
        if index > 1:
            self.list[index - 2], self.list[index - 1] = (self.list[index - 1], self.list[index - 2])
            self._update_list_to_ui()
            cmds.textScrollList(self.list_name, edit=True, selectIndexedItem=index - 1)

    def _move_down(self, *_):
        index = self._get_selected_index()
        if index is not None and index < len(self.list):
            # Adjusting index for a zero-based list
            adjusted_index = index - 1
            self.list[adjusted_index], self.list[adjusted_index + 1] = (
                self.list[adjusted_index + 1], self.list[adjusted_index])
            self._update_list_to_ui()
            cmds.textScrollList(self.list_name, edit=True, selectIndexedItem=index + 1)

    def _remove(self, *_):
        index = self._get_selected_index()
        if index:
            cmds.textScrollList(self.list_name, edit=True, removeIndexedItem=index)
            self.list.pop(index - 1)
            self._update_list_to_ui()

    def clear(self, *_):
        self.list.clear()
        cmds.textScrollList(self.list_name, edit=True, removeAll=True)
        self._update_list_to_ui()


if __name__ == "__main__":
    # Example usage:
    if cmds.window("main_window", exists=True):
        cmds.deleteUI("main_window")
    cmds.window("main_window")

    ui_instance = MainUI(
        "main_window",
        "visual_list",
        {},
        label="Bold Test Frame",
        label_visible=False,
        raido_label="Add Mode:",
        font="boldLabelFont",
        width=350,
        height=200,
        border=True,
        marginWidth=5,
        marginHeight=5,
        visible=True,
        collapsable=False,
        collapsed=False,
        color=[0.6, 0.5, 0.6],
        annotation="This is a test frame.",
        create=True)


    def mode1_callback():
        list_item = "Mode 1 selected"
        ui_instance.insert(0, list_item)


    def mode2_callback():
        list_item = "Mode 2 selected"
        ui_instance.insert(0, list_item)


    mode_callbacks = {
        "Mode 1": mode1_callback,
        "Mode 2": mode2_callback
    }

    ui_instance.mode_callbacks = mode_callbacks

    cmds.showWindow("main_window")
