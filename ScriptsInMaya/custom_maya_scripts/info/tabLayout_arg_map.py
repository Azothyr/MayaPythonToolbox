tabLayout_arg_map = {
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
	"bs": {
		"name": "borderStyle",
		"description": "Specify the style of the border for tab layout. Valid values are: \"none\", \"top\", \"notop\""
		" and \"full\". By default, it will use \"full\" to draw a simple frame around the body"
		" area of the tab layout. \"none\" - Do not draw borders around the body area of the tab"
		" layout \"top\" - Only draw a simple line right below the tabs \"notop\" - Draw a simple"
		" frame on the left/right/bottom no top of the tab layout \"full\" - Draw a simple frame"
		" around the body area of the tab layout",
		"type": "string",
		"property": "C Q E"
	},
	"cc": {
		"name": "changeCommand",
		"description": "Command executed when a tab is selected interactively. This command is only invoked when"
		" the selected tab changes. Re-selecting the current tab will not invoke this command.",
		"type": "script",
		"property": "C E"
	},
	"ca": {
		"name": "childArray",
		"description": "Returns a string array of the names of the layout's immediate children.",
		"type": "boolean",
		"property": "Q"
	},
	"cr": {
		"name": "childResizable",
		"description": "Set to true if you want the child of the control layout to be as wide as the scroll area."
		" You may also indicate a minimum width for the child using the -mcw/minChildWidth flag.",
		"type": "boolean",
		"property": "C Q"
	},
	"ct": {
		"name": "closeTab",
		"description": "Close the tab at the given index.",
		"type": "int",
		"property": "C E"
	},
	"ctc": {
		"name": "closeTabCommand",
		"description": "Specify a script to be executed when one of the tabs are closed by clicking on the header"
		" widget (MMB or X button).",
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
	"dtg": {
		"name": "docTag",
		"description": "Add a documentation flag to the control. The documentation flag has a directory structure."
		" (e.g., -dt render/multiLister/createNode/material)",
		"type": "string",
		"property": "C Q E"
	},
	"dcc": {
		"name": "doubleClickCommand",
		"description": "Command executed when a tab is double clicked on. Note that the first click will select"
		" the tab and the second click will execute the double click command. Double clicking the"
		" current tab will re-invoke the double click command.",
		"type": "script",
		"property": "C E"
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
	"hst": {
		"name": "horizontalScrollBarThickness",
		"description": "Thickness of the horizontal scroll bar. Specify an integer value greater than or equal"
		" to zero. This flag has no effect on Windows systems.",
		"type": "int",
		"property": "C E"
	},
	"i": {
		"name": "image",
		"description": "Image appearing in top right corner of tab layout.",
		"type": "string",
		"property": "C Q E"
	},
	"iv": {
		"name": "imageVisible",
		"description": "Visibility of tab image.",
		"type": "boolean",
		"property": "C Q E"
	},
	"imh": {
		"name": "innerMarginHeight",
		"description": "Margin height for all tab children.",
		"type": "int",
		"property": "C Q"
	},
	"imw": {
		"name": "innerMarginWidth",
		"description": "Margin width for all tab children.",
		"type": "int",
		"property": "C Q"
	},
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Q"
	},
	"m": {
		"name": "manage",
		"description": "Manage state of the control. An unmanaged control is not visible, nor does it take up any"
		" screen real estate. All controls are created managed by default.",
		"type": "boolean",
		"property": "C Q E"
	},
	"mcw": {
		"name": "minChildWidth",
		"description": "Specify a positive non-zero integer value indicating the minimum width the tab layout's"
		" children. This flag only has meaning when the -cr/childResizable flag is set to true.",
		"type": "int",
		"property": "C Q"
	},
	"mt": {
		"name": "moveTab",
		"description": "Move the tab from the current index to a new index.",
		"type": "[int, int]",
		"property": "C E"
	},
	"ntc": {
		"name": "newTabCommand",
		"description": "Command executed when the 'New Tab' button (on the tab bar) is clicked. Note: in order"
		" to show the new tab button use the -snt/showNewTab flag. Using this command will override"
		" any internal Maya logic for adding a new tab (only this command will be executed).",
		"type": "script",
		"property": "C E"
	},
	"nbg": {
		"name": "noBackground",
		"description": "Clear/reset the control's background. Passing true means the background should not be drawn"
		" at all, false means the background should be drawn. The state of this flag is inherited"
		" by children of this control.",
		"type": "boolean",
		"property": "C E"
	},
	"nch": {
		"name": "numberOfChildren",
		"description": "Returns in an int the number of immediate children of the layout.",
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
	"psc": {
		"name": "preSelectCommand",
		"description": "Command executed when a tab is selected but before it's contents become visible. Re-selecting"
		" the current tab will not invoke this command. Note that this command is not executed by"
		" using either of the -st/selectTab or -sti/selectTabIndex flags.",
		"type": "script",
		"property": "C E"
	},
	"po": {
		"name": "preventOverride",
		"description": "If true, this flag prevents overriding the control's attribute via the control's right"
		" mouse button menu.",
		"type": "boolean",
		"property": "C Q E"
	},
	"scr": {
		"name": "scrollable",
		"description": "Puts all children of this layout within a scroll area.",
		"type": "boolean",
		"property": "C Q"
	},
	"stb": {
		"name": "scrollableTabs",
		"description": "If true, the active tab in the layout can be scrolled through with the mouse wheel. Default"
		" is true.",
		"type": "boolean",
		"property": "C Q E"
	},
	"sc": {
		"name": "selectCommand",
		"description": "Command executed when a tab is selected interactively This command will be invoked whenever"
		" a tab is selected, ie. re-selecting the current tab will invoke this command. Note that"
		" this command is not executed by using either of the -st/selectTab or -sti/selectTabIndex"
		" flags.",
		"type": "script",
		"property": "C Q E"
	},
	"st": {
		"name": "selectTab",
		"description": "The name, in short form, of the selected tab. An empty string is returned on query if there"
		" are no child tabs.",
		"type": "string",
		"property": "C Q E"
	},
	"sti": {
		"name": "selectTabIndex",
		"description": "Identical to the -st/selectTab flag except this flag takes a 1-based index to identify"
		" the selected tab. A value of 0 is returned on query if there are no child tabs.",
		"type": "int",
		"property": "C Q E"
	},
	"snt": {
		"name": "showNewTab",
		"description": "Set to true if you want to have a 'New Tab' button shown at the end of the tab bar. Note:"
		" use the -ntc/newTabCommand flag to set the command executed when this button is clicked.",
		"type": "boolean",
		"property": "C Q E"
	},
	"sbm": {
		"name": "statusBarMessage",
		"description": "Extra string to display in the status bar when the mouse is over the control.",
		"type": "string",
		"property": "C E"
	},
	"ti": {
		"name": "tabIcon",
		"description": "Set an icon for a tab. The first argument is the name of a control that must be a child"
		" of the tab layout. The second argument is the icon file name.",
		"type": "[string, string]",
		"property": "C Q E M"
	},
	"tii": {
		"name": "tabIconIndex",
		"description": "Identical to the -ti/tabIcon flag except this flag takes a 1-based index to identify the"
		" tab you want to set the icon for. If this flag is queried the tab icons for all the children"
		" are returned.",
		"type": "[int, string]",
		"property": "C Q E M"
	},
	"tl": {
		"name": "tabLabel",
		"description": "Set a tab label. The first argument is the name of a control that must be a child of the"
		" tab layout. The second argument is the label for the tab associated with that child. If"
		" this flag is queried then the tab labels for all the children are returned.",
		"type": "[string, string]",
		"property": "C Q E M"
	},
	"tli": {
		"name": "tabLabelIndex",
		"description": "Identical to the -tl/tabLabel flag except this flag takes a 1-based index to identify the"
		" tab you want to set the label for. If this flag is queried the tab labels for all the"
		" children are returned.",
		"type": "[int, string]",
		"property": "C Q E M"
	},
	"tp": {
		"name": "tabPosition",
		"description": "Changes the tab position. The possible values are: \"north\", \"east\" and \"west\".",
		"type": "string",
		"property": "C Q E"
	},
	"tt": {
		"name": "tabTooltip",
		"description": "Set a tab tooltip. The first argument is the name of a control that must be a child of"
		" the tab layout. The second argument is the tooltip for the tab associated with that child."
		" If this flag is queried then the tab tooltips for all the children are returned.",
		"type": "[string, string]",
		"property": "C Q E M"
	},
	"tti": {
		"name": "tabTooltipIndex",
		"description": "Identical to the -tt/tabTooltip flag except this flag takes a 1-based index to identify"
		" the tab you want to set the tooltip for. If this flag is queried the tab tooltips for"
		" all the children are returned.",
		"type": "[int, string]",
		"property": "C Q E M"
	},
	"tc": {
		"name": "tabsClosable",
		"description": "Set to true if you want to have a close button icon on all created tabs.",
		"type": "boolean",
		"property": "C Q"
	},
	"tv": {
		"name": "tabsVisible",
		"description": "Visibility of the tab labels.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "C"
	},
	"vst": {
		"name": "verticalScrollBarThickness",
		"description": "Thickness of the vertical scroll bar. Specify an integer value greater than or equal to"
		" zero. This flag has no effect on Windows systems.",
		"type": "int",
		"property": "C E"
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
