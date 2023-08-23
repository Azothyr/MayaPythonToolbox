text_arg_map = {
	"al": {
		"name": "align",
		"description": "The label alignment. Alignment values are \"left\", \"right\", and \"center\". Note that"
		" the alignment will only be noticable if the control is wider than the label length. By"
		" default, the label is aligned \"center\".",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ann": {
		"name": "annotation",
		"description": "Annotate the control with an extra string value.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"bgc": {
		"name": "backgroundColor",
		"description": "The background color of the control. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0. When setting backgroundColor,"
		" the background is automatically enabled, unless enableBackground is also specified with"
		" a false value.",
		"type": "[float, float, float]",
		"property": "Create|Query|Edit"
	},
	"dt": {
		"name": "defineTemplate",
		"description": "Puts the command in a mode where any other flags and arguments are parsed and added to"
		" the command template specified in the argument. They will be used as default arguments"
		" in any subsequent invocations of the command when templateName is set as the current template.",
		"type": "string",
		"property": "Create"
	},
	"dtg": {
		"name": "docTag",
		"description": "Add a documentation flag to the control. The documentation flag has a directory structure."
		" (e.g., -dt render/multiLister/createNode/material)",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"dgc": {
		"name": "dragCallback",
		"description": "Adds a callback that is called when the middle mouse button is pressed. The MEL version"
		" of the callback is of the form: global proc string[] callbackNamestring $dragControl,"
		" int $x, int $y, int $mods The proc returns a string array that is transferred to the drop"
		" site. By convention the first string in the array describes the user settable message"
		" type. Controls that are application defined drag sources may ignore the callback. $mods"
		" allows testing for the key modifiers CTRL and SHIFT. Possible values are 0 == No modifiers,"
		" 1 == SHIFT, 2 == CTRL, 3 == CTRL + SHIFT. In Python, it is similar, but there are two"
		" ways to specify the callback. The recommended way is to pass a Python function object"
		" as the argument. In that case, the Python callback should have the form: def callbackName"
		" dragControl, x, y, modifiers : The values of these arguments are the same as those for"
		" the MEL version above. The other way to specify the callback in Python is to specify a"
		" string to be executed. In that case, the string will have the values substituted into"
		" it via the standard Python format operator. The format values are passed in a dictionary"
		" with the keys \"dragControl\", \"x\", \"y\", \"modifiers\". The \"dragControl\" value"
		" is a string and the other values are integers eg the callback string could be \"print"
		" '%dragControls %xd %yd %modifiersd'\"",
		"type": "script",
		"property": "Create|Edit"
	},
	"dpc": {
		"name": "dropCallback",
		"description": "Adds a callback that is called when a drag and drop operation is released above the drop"
		" site. The MEL version of the callback is of the form: global proc callbackNamestring $dragControl,"
		" string $dropControl, string $msgs[], int $x, int $y, int $type The proc receives a string"
		" array that is transferred from the drag source. The first string in the msgs array describes"
		" the user defined message type. Controls that are application defined drop sites may ignore"
		" the callback. $type can have values of 1 == Move, 2 == Copy, 3 == Link. In Python, it"
		" is similar, but there are two ways to specify the callback. The recommended way is to"
		" pass a Python function object as the argument. In that case, the Python callback should"
		" have the form: def pythonDropTest dragControl, dropControl, messages, x, y, dragType :"
		" The values of these arguments are the same as those for the MEL version above. The other"
		" way to specify the callback in Python is to specify a string to be executed. In that case,"
		" the string will have the values substituted into it via the standard Python format operator."
		" The format values are passed in a dictionary with the keys \"dragControl\", \"dropControl\","
		" \"messages\", \"x\", \"y\", \"type\". The \"dragControl\" value is a string and the other"
		" values are integers eg the callback string could be \"print '%dragControls %dropControls"
		" %messagesr %xd %yd %typed'\"",
		"type": "script",
		"property": "Create|Edit"
	},
	"drc": {
		"name": "dropRectCallback",
		"description": "Adds a callback that is called when a drag and drop operation is hovering above the drop"
		" site. It returns the shape of the rectangle to be drawn to highlight the entry, if the"
		" control can receive the dropped data. The MEL version of the callback is of the form:"
		" global proc int[] callbackNamestring $dropControl, int $x, int $y The return value is"
		" an array of size 4, with the parameters, in order, being the left and top coordinates"
		" of the rectangle to be drawn, followed by the width and height. This functionality is"
		" currently only implemented in MEL.",
		"type": "script",
		"property": "Edit"
	},
	"en": {
		"name": "enable",
		"description": "The enable state of the control. By default, this flag is set to true and the control is"
		" enabled. Specify false and the control will appear dimmed or greyed-out indicating it"
		" is disabled.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ebg": {
		"name": "enableBackground",
		"description": "Enables the background color of the control.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ekf": {
		"name": "enableKeyboardFocus",
		"description": "If enabled, the user can navigate to the control with the tab key and select values with"
		" the keyboard or mouse. This flag would typically be used to turn off focus support from"
		" controls that get it by default, like Edit and List controls If disabled, text in text"
		" fields can still be selected with the mouse but it cannot be copied (except in Linux when"
		" \"Middle Click Paste\" is enabled).",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "Create"
	},
	"fn": {
		"name": "font",
		"description": "The font for the text. Valid values are \"boldLabelFont\", \"smallBoldLabelFont\", \"tinyBoldLabelFont\","
		" \"plainLabelFont\", \"smallPlainLabelFont\", \"obliqueLabelFont\", \"smallObliqueLabelFont\","
		" \"fixedWidthFont\" and \"smallFixedWidthFont\".",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"fpn": {
		"name": "fullPathName",
		"description": "Return the full path name of the widget, which includes all the parents.",
		"type": "boolean",
		"property": "Query"
	},
	"h": {
		"name": "height",
		"description": "The height of the control. The control will attempt to be this size if it is not overruled"
		" by parent layout conditions.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"hlc": {
		"name": "highlightColor",
		"description": "The highlight color of the control. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0.",
		"type": "[float, float, float]",
		"property": "Create|Query|Edit"
	},
	"hl": {
		"name": "hyperlink",
		"description": "Sets the label text to be a hyperlink if the argument is true. The label text must be a"
		" proper HTML link. In MEL, double quotes in the link will most likely have to be protected"
		" from the MEL interpreter by preceding them with a backslash. Clicking on the link will"
		" open it in an external Web browser.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Query"
	},
	"l": {
		"name": "label",
		"description": "The label text. The default label is the name of the control.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"m": {
		"name": "manage",
		"description": "Manage state of the control. An unmanaged control is not visible, nor does it take up any"
		" screen real estate. All controls are created managed by default.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"nbg": {
		"name": "noBackground",
		"description": "Clear/reset the control's background. Passing true means the background should not be drawn"
		" at all, false means the background should be drawn. The state of this flag is inherited"
		" by children of this control.",
		"type": "boolean",
		"property": "Create|Edit"
	},
	"npm": {
		"name": "numberOfPopupMenus",
		"description": "Return the number of popup menus attached to this control.",
		"type": "boolean",
		"property": "Query"
	},
	"p": {
		"name": "parent",
		"description": "The parent layout for this control.",
		"type": "string",
		"property": "Create|Query"
	},
	"pma": {
		"name": "popupMenuArray",
		"description": "Return the names of all the popup menus attached to this control.",
		"type": "boolean",
		"property": "Query"
	},
	"po": {
		"name": "preventOverride",
		"description": "If true, this flag prevents overriding the control's attribute via the control's right"
		" mouse button menu.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"rs": {
		"name": "recomputeSize",
		"description": "If true then the control will recompute it's size to just fit the size of the label. If"
		" false then the control size will remain fixed as you change the size of the label. The"
		" default value of this flag is true.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"sbm": {
		"name": "statusBarMessage",
		"description": "Extra string to display in the status bar when the mouse is over the control.",
		"type": "string",
		"property": "Create|Edit"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "Create"
	},
	"vis": {
		"name": "visible",
		"description": "The visible state of the control. A control is created visible by default. Note that a"
		" control's actual appearance is also dependent on the visible state of its parent layout(s).",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"vcc": {
		"name": "visibleChangeCommand",
		"description": "Command that gets executed when visible state of the control changes.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"w": {
		"name": "width",
		"description": "The width of the control. The control will attempt to be this size if it is not overruled"
		" by parent layout conditions.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"ww": {
		"name": "wordWrap",
		"description": "If true then label text is wrapped where necessary at word-breaks. If false, it is not"
		" wrapped at all. The default value of this flag is false.",
		"type": "boolean",
		"property": "Create|Query"
	},
}
