window_arg_map = {
	"bgc": {
		"name": "backgroundColor",
		"description": "The background color of the window. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0.",
		"type": "[float, float, float]",
		"property": "C E"
	},
	"cc": {
		"name": "closeCommand",
		"description": "Script executed after the window is closed.",
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
		"description": "Attach a tag to the window.",
		"type": "string",
		"property": "C Q E"
	},
	"dc": {
		"name": "dockCorner",
		"description": "Specifies which docking areas occupied the four different corners of the window. By default"
		" docking windows on the bottom or top will span the whole window. Use multiple instances"
		" of this flag to allow the left and right docking areas to occupy the corners. This method"
		" has two arguments: docking corner and docking area. Possible values for docking corner"
		" are \"topLeft\", \"topRight\", bottomLeft\", and \"bottomRight\". Possible values for"
		" docking area are \"left\", \"right\", \"top\", and \"bottom\".",
		"type": "[string, string]",
		"property": "C M"
	},
	"ds": {
		"name": "dockStation",
		"description": "When set this flag specifies that this window can contain other docked sub-windows.",
		"type": "boolean",
		"property": "C"
	},
	"dl": {
		"name": "dockingLayout",
		"description": "When queried this flag will return a string holding the docking layout information. This"
		" string can be set when creating or editing a docking station to restore the previous docking"
		" layout. This string is a hexadecimal representation of a binary string and is not meant"
		" to be humanly readable, but can be saved and loaded using the optionVar command to restore"
		" layouts across sessions of Maya.",
		"type": "string",
		"property": "C Q E"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "C"
	},
	"fw": {
		"name": "frontWindow",
		"description": "Return the name of the front window. Note: you must supply the name of any window (the"
		" window does not need to exist). Returns \"unknown\" if the front window cannot be determined.",
		"type": "boolean",
		"property": "Q"
	},
	"h": {
		"name": "height",
		"description": "Height of the window excluding any window frame in pixels.",
		"type": "int",
		"property": "C Q E"
	},
	"iconName": {
		"name": "iconName",
		"description": "The window's icon title. By default it is the same as the window's title.",
		"type": "string",
		"property": "C Q E"
	},
	"i": {
		"name": "iconify",
		"description": "Icon state of the window.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ip": {
		"name": "interactivePlacement",
		"description": "Deprecated flag. Recognized but not implemented. This flag will be removed in a future"
		" version of Maya.",
		"type": "boolean",
		"property": "C"
	},
	"le": {
		"name": "leftEdge",
		"description": "Position of the left edge of the window.",
		"type": "int",
		"property": "C Q E"
	},
	"mm": {
		"name": "mainMenuBar",
		"description": "If this flag is used then the main menu bar will be enabled.",
		"type": "boolean",
		"property": "C Q E"
	},
	"mw": {
		"name": "mainWindow",
		"description": "Main window for the application. The main window has an 'Exit' item in the Window Manager"
		" menu. By default, the first created window becomes the main window.",
		"type": "boolean",
		"property": "C Q E"
	},
	"mxb": {
		"name": "maximizeButton",
		"description": "Turns the window's maximize button on or off.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ma": {
		"name": "menuArray",
		"description": "Return a string array containing the names of the menus in the window's menu bar.",
		"type": "boolean",
		"property": "Q"
	},
	"mb": {
		"name": "menuBar",
		"description": "Adds an empty menu bar to the window. The Qt name of the object will be m_menubar_nameOfTheWindow.",
		"type": "boolean",
		"property": "C Q"
	},
	"mcw": {
		"name": "menuBarCornerWidget",
		"description": "This flag specifies a widget to add to a corner of the parent window. The first argument"
		" corresponds to the widget name and the second to the position of the widget. Possible"
		" values for widget position are \"topLeft\", \"topRight\", \"bottomLeft\", \"bottomRight\"."
		" In query mode this flag returns all the corner widget names in the following order: topLeft,"
		" topRight, bottomLeft, bottomRight. Add the -mbr/-menuBarResize flag to the changeCommand"
		" of widget passed (first argument) so that it will always have an appropriate size.",
		"type": "[string, string]",
		"property": "Q E"
	},
	"mbr": {
		"name": "menuBarResize",
		"description": "This flag should be used with the -mcw/-menuBarCornerWidget flag. This is used to resize"
		" the menu bar so that the corner widgets are updated.",
		"type": "boolean",
		"property": "E"
	},
	"mbv": {
		"name": "menuBarVisible",
		"description": "Visibility of the menu bar (if there is one).",
		"type": "boolean",
		"property": "C Q E"
	},
	"mi": {
		"name": "menuIndex",
		"description": "Sets the index of a specified menu.",
		"type": "[string, uint]",
		"property": "E"
	},
	"mnb": {
		"name": "minimizeButton",
		"description": "Turns the window's minimize button on or off.",
		"type": "boolean",
		"property": "C Q E"
	},
	"mnc": {
		"name": "minimizeCommand",
		"description": "Script executed after the window is minimized (iconified).",
		"type": "script",
		"property": "C E"
	},
	"nde": {
		"name": "nestedDockingEnabled",
		"description": "Controls whether nested docking is enabled or not. Nested docking allows for docking windows"
		" next to other docked windows for more possible arrangement styles.",
		"type": "boolean",
		"property": "C"
	},
	"nm": {
		"name": "numberOfMenus",
		"description": "Return the number of menus attached to the window's menu bar.",
		"type": "boolean",
		"property": "Q"
	},
	"p": {
		"name": "parent",
		"description": "Specifies a parent window or layout which the created window is always on top of. Note:"
		" If the parent is a window the created window is not modal, so events are still propagated"
		" to the parent window.",
		"type": "string",
		"property": "C"
	},
	"rtf": {
		"name": "resizeToFitChildren",
		"description": "The window will always grow/shrink to just fit the controls it contains.",
		"type": "boolean",
		"property": "C Q E"
	},
	"rc": {
		"name": "restoreCommand",
		"description": "Script executed after the window is restored from it's minimized (iconified) state.",
		"type": "script",
		"property": "C E"
	},
	"ret": {
		"name": "retain",
		"description": "Retains the window after it has been closed. The default is to delete the window when it"
		" is closed.",
		"type": "boolean",
		"property": "C"
	},
	"s": {
		"name": "sizeable",
		"description": "Whether or not the window may be interactively resized.",
		"type": "boolean",
		"property": "C Q E"
	},
	"st": {
		"name": "state",
		"description": "When queried this flag will return a string holding the window state information. This"
		" string is a hexadecimal representation of a binary string and is not meant to be humanly"
		" readable, but can be saved and loaded using the optionVar command to restore window state"
		" across sessions of Maya.",
		"type": "string",
		"property": "C Q E"
	},
	"t": {
		"name": "title",
		"description": "The window's title.",
		"type": "string",
		"property": "C Q E"
	},
	"tb": {
		"name": "titleBar",
		"description": "Turns the window's title bar on or off.",
		"type": "boolean",
		"property": "C Q E"
	},
	"tbm": {
		"name": "titleBarMenu",
		"description": "Controls whether the title bar menu exists in the window title bar. Only valid if -tb/titleBar"
		" is true. This Windows only flag is true by default.",
		"type": "boolean",
		"property": "C Q E"
	},
	"tlb": {
		"name": "toolbox",
		"description": "Makes this a toolbox style window. A Windows only flag that makes the title bar smaller"
		" and uses a slightly different display style.",
		"type": "boolean",
		"property": "C Q E"
	},
	"te": {
		"name": "topEdge",
		"description": "Position of the top edge of the window.",
		"type": "int",
		"property": "C Q E"
	},
	"tlc": {
		"name": "topLeftCorner",
		"description": "Position of the window's top left corner.",
		"type": "[int, int]",
		"property": "C Q E"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "C"
	},
	"vis": {
		"name": "visible",
		"description": "The window's visibility.",
		"type": "boolean",
		"property": "C Q E"
	},
	"w": {
		"name": "width",
		"description": "Width of the window excluding any window frame in pixels.",
		"type": "int",
		"property": "C Q E"
	},
	"wh": {
		"name": "widthHeight",
		"description": "Window's width and height excluding any window frame in pixels.",
		"type": "[int, int]",
		"property": "C Q E"
	},
}
