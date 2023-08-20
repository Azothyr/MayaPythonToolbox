optionMenu_arg_map = {
	"acc": {
		"name": "alwaysCallChangeCommand",
		"description": "Toggle whether to always call the change command, regardless of the change.",
		"type": "boolean",
		"property": "C Q"
	},
	"ann": {
		"name": "annotation",
		"description": "Annotate the control with an extra string value.",
		"type": "string",
		"property": "C Q E"
	},
	"bgc": {
		"name": "backgroundColor",
		"description": "The background color of the control. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0. When setting backgroundColor,"
		" the background is automatically enabled, unless enableBackground is also specified with"
		" a false value.",
		"type": "[float, float, float]",
		"property": "C Q E"
	},
	"bsp": {
		"name": "beforeShowPopup",
		"description": "Callback that is called just before we show the drop down menu.",
		"type": "script",
		"property": "C E"
	},
	"cc": {
		"name": "changeCommand",
		"description": "Adds a callback that is called when a new item is selected. The MEL script will have the"
		" newly selected item's value substituted for #1. For Python, the callback should be a callable"
		" object which accepts one argument, which is the newly selected item's value.",
		"type": "script",
		"property": "C E"
	},
	"dt": {
		"name": "defineTemplate",
		"description": "Puts the command in a mode where any other flags and arguments are parsed and added to"
		" the command template specified in the argument. They will be used as default arguments"
		" in any subsequent invocations of the command when templateName is set as the current template.",
		"type": "string",
		"property": "C"
	},
	"dai": {
		"name": "deleteAllItems",
		"description": "Delete all the items in this menu.",
		"type": "boolean",
		"property": "E"
	},
	"dtg": {
		"name": "docTag",
		"description": "Add a documentation flag to the control. The documentation flag has a directory structure."
		" (e.g., -dt render/multiLister/createNode/material)",
		"type": "string",
		"property": "C Q E"
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
		"property": "C E"
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
		"property": "C E"
	},
	"en": {
		"name": "enable",
		"description": "The enable state of the control. By default, this flag is set to true and the control is"
		" enabled. Specify false and the control will appear dimmed or greyed-out indicating it"
		" is disabled.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ebg": {
		"name": "enableBackground",
		"description": "Enables the background color of the control.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ekf": {
		"name": "enableKeyboardFocus",
		"description": "If enabled, the user can navigate to the control with the tab key and select values with"
		" the keyboard or mouse. This flag would typically be used to turn off focus support from"
		" controls that get it by default, like Edit and List controls If disabled, text in text"
		" fields can still be selected with the mouse but it cannot be copied (except in Linux when"
		" \"Middle Click Paste\" is enabled).",
		"type": "boolean",
		"property": "C Q E"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "C"
	},
	"fpn": {
		"name": "fullPathName",
		"description": "Return the full path name of the widget, which includes all the parents.",
		"type": "boolean",
		"property": "Q"
	},
	"h": {
		"name": "height",
		"description": "The height of the control. The control will attempt to be this size if it is not overruled"
		" by parent layout conditions.",
		"type": "int",
		"property": "C Q E"
	},
	"hlc": {
		"name": "highlightColor",
		"description": "The highlight color of the control. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0.",
		"type": "[float, float, float]",
		"property": "C Q E"
	},
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Q"
	},
	"ill": {
		"name": "itemListLong",
		"description": "The long names of the menu items.",
		"type": "boolean",
		"property": "Q"
	},
	"ils": {
		"name": "itemListShort",
		"description": "The short names of the menu items.",
		"type": "boolean",
		"property": "Q"
	},
	"l": {
		"name": "label",
		"description": "The optional label text to the left of the popup menu.",
		"type": "string",
		"property": "C Q E"
	},
	"m": {
		"name": "manage",
		"description": "Manage state of the control. An unmanaged control is not visible, nor does it take up any"
		" screen real estate. All controls are created managed by default.",
		"type": "boolean",
		"property": "C Q E"
	},
	"mvi": {
		"name": "maxVisibleItems",
		"description": "The maximum number of items that are visible in the popup menu. If the popup contains more"
		" items than this, a scrollbar is added automatically.",
		"type": "int",
		"property": "C Q E"
	},
	"nbg": {
		"name": "noBackground",
		"description": "Clear/reset the control's background. Passing true means the background should not be drawn"
		" at all, false means the background should be drawn. The state of this flag is inherited"
		" by children of this control.",
		"type": "boolean",
		"property": "C E"
	},
	"ni": {
		"name": "numberOfItems",
		"description": "The number of menu items.",
		"type": "boolean",
		"property": "Q"
	},
	"npm": {
		"name": "numberOfPopupMenus",
		"description": "Return the number of popup menus attached to this control.",
		"type": "boolean",
		"property": "Q"
	},
	"p": {
		"name": "parent",
		"description": "The parent layout for this control.",
		"type": "string",
		"property": "C Q"
	},
	"pma": {
		"name": "popupMenuArray",
		"description": "Return the names of all the popup menus attached to this control.",
		"type": "boolean",
		"property": "Q"
	},
	"pmc": {
		"name": "postMenuCommand",
		"description": "Specify a script to be executed when the popup menu is about to be shown.",
		"type": "script",
		"property": "C E"
	},
	"pmo": {
		"name": "postMenuCommandOnce",
		"description": "Indicate the -pmc/postMenuCommand should only be invoked once. Default value is false,"
		" ie. the -pmc/postMenuCommand is invoked every time the popup menu is shown.",
		"type": "boolean",
		"property": "C Q E"
	},
	"po": {
		"name": "preventOverride",
		"description": "If true, this flag prevents overriding the control's attribute via the control's right"
		" mouse button menu.",
		"type": "boolean",
		"property": "C Q E"
	},
	"sl": {
		"name": "select",
		"description": "The current menu item. The argument and return value is 1-based. Note that the current"
		" menu item can only be set if it is enabled.",
		"type": "int",
		"property": "C Q E"
	},
	"sbm": {
		"name": "statusBarMessage",
		"description": "Extra string to display in the status bar when the mouse is over the control.",
		"type": "string",
		"property": "C E"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "C"
	},
	"v": {
		"name": "value",
		"description": "The text of the current menu item.",
		"type": "string",
		"property": "C Q E"
	},
	"vis": {
		"name": "visible",
		"description": "The visible state of the control. A control is created visible by default. Note that a"
		" control's actual appearance is also dependent on the visible state of its parent layout(s).",
		"type": "boolean",
		"property": "C Q E"
	},
	"vcc": {
		"name": "visibleChangeCommand",
		"description": "Command that gets executed when visible state of the control changes.",
		"type": "script",
		"property": "C Q E"
	},
	"w": {
		"name": "width",
		"description": "The width of the control. The control will attempt to be this size if it is not overruled"
		" by parent layout conditions.",
		"type": "int",
		"property": "C Q E"
	},
}
