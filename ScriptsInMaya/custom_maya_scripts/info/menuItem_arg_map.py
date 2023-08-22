menuItem_arg_map = {
	"aob": {
		"name": "allowOptionBoxes",
		"description": "Deprecated. All menus and menu items always allow option boxes. In the case of submenu"
		" items this flag specifies whether the submenu will be able to support option box menu"
		" items. Always returns true.",
		"type": "boolean",
		"property": "C Q"
	},
	"ann": {
		"name": "annotation",
		"description": "Annotate the menu item with an extra string value.",
		"type": "string",
		"property": "C Q E"
	},
	"bld": {
		"name": "boldFont",
		"description": "Specify if text should be bold. Only supported in menus which use the marking menu implementation."
		" Default is false for Windows, and true for all other platforms.",
		"type": "boolean",
		"property": "C Q"
	},
	"cb": {
		"name": "checkBox",
		"description": "Creates a check box menu item. Argument specifies the check box value.",
		"type": "boolean",
		"property": "C Q E"
	},
	"cl": {
		"name": "collection",
		"description": "To explicitly add a radio menu item to a radioMenuItemCollection.",
		"type": "string",
		"property": "C Q"
	},
	"c": {
		"name": "command",
		"description": "Attaches a command/script that will be executed when the item is selected. Note this command"
		" is not executed when the menu item is in an optionMenu control.",
		"type": "script",
		"property": "C Q E"
	},
	"da": {
		"name": "data",
		"description": "Attaches a piece of user-defined data to the menu item.",
		"type": "int",
		"property": "C Q E"
	},
	"dt": {
		"name": "defineTemplate",
		"description": "Puts the command in a mode where any other flags and arguments are parsed and added to"
		" the command template specified in the argument. They will be used as default arguments"
		" in any subsequent invocations of the command when templateName is set as the current template.",
		"type": "string",
		"property": "C"
	},
	"d": {
		"name": "divider",
		"description": "Creates a divider menu item.",
		"type": "boolean",
		"property": "C Q"
	},
	"dl": {
		"name": "dividerLabel",
		"description": "Adds a label to a divider menu item.",
		"type": "string",
		"property": "C Q E"
	},
	"dtg": {
		"name": "docTag",
		"description": "Attaches a tag to the menu item.",
		"type": "string",
		"property": "C Q E"
	},
	"ddc": {
		"name": "dragDoubleClickCommand",
		"description": "If the menu item is put on the shelf then this command will be invoked when the corresponding"
		" shelf object is double clicked.",
		"type": "script",
		"property": "C Q E"
	},
	"dmc": {
		"name": "dragMenuCommand",
		"description": "If the menu item is put on the shelf then this command will be invoked when the corresponding"
		" shelf object is clicked.",
		"type": "script",
		"property": "C Q E"
	},
	"ec": {
		"name": "echoCommand",
		"description": "Specify whether the action attached with the c/command flag should echo to the command"
		" output areas when invoked. This flag is false by default and must be specified with the"
		" c/command flag.",
		"type": "boolean",
		"property": "C Q E"
	},
	"en": {
		"name": "enable",
		"description": "Enable state for the menu item. A disabled menu item is dimmed and unresponsive. An enabled"
		" menu item is selectable and has normal appearance.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ecr": {
		"name": "enableCommandRepeat",
		"description": "This flag only affects menu items to which a command can be attached. Specify true and"
		" the command may be repeated by executing the command repeatLast. This flag is true by"
		" default for all items except for option box items.",
		"type": "boolean",
		"property": "C Q E"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "C"
	},
	"fi": {
		"name": "familyImage",
		"description": "Get the filename of the family icon associated with the menu. The family icon will be used"
		" for the shelf unless an icon is specified with the image flag.",
		"type": "string",
		"property": "Q"
	},
	"i": {
		"name": "image",
		"description": "The filename of the icon associated with the menu item. If the menu containing the menu"
		" item is being edited with a menuEditor widget, then the menuEditor will use this icon"
		" to represent the menu item. This icon will be displayed on the shelf when the menu item"
		" is placed there.",
		"type": "string",
		"property": "C Q E"
	},
	"iol": {
		"name": "imageOverlayLabel",
		"description": "Specify a short (5 character) text string to be overlayed on top of the icon associated"
		" with the menu item. This is primarily a mechanism for differentiating menu items that"
		" are using a Family icon due to the fact that an icon image had not been explicitly defined."
		" The image overlay label will not be used if an icon image is defined for the menu item.",
		"type": "string",
		"property": "C Q E"
	},
	"ia": {
		"name": "insertAfter",
		"description": "Specify After which item the new one will be placed. If this flag is not specified, item"
		" is added at the end of the menu. Use the empty string \"\" to insert before the first"
		" item of the menu.",
		"type": "string",
		"property": "C"
	},
	"icb": {
		"name": "isCheckBox",
		"description": "Returns true if the item is a check box item.",
		"type": "boolean",
		"property": "Q"
	},
	"iob": {
		"name": "isOptionBox",
		"description": "Returns true if the item is an option box item.",
		"type": "boolean",
		"property": "Q"
	},
	"irb": {
		"name": "isRadioButton",
		"description": "Returns true if the item is a radio button item.",
		"type": "boolean",
		"property": "Q"
	},
	"itl": {
		"name": "italicized",
		"description": "Specify if text should be italicized. Only supported in menus which use the marking menu"
		" implementation. Default is false.",
		"type": "boolean",
		"property": "C Q"
	},
	"l": {
		"name": "label",
		"description": "The text that appears in the item.",
		"type": "string",
		"property": "C Q E"
	},
	"ld": {
		"name": "longDivider",
		"description": "Indicate whether the divider is long or short. Has no effect if divider label is set. Default"
		" is true.",
		"type": "boolean",
		"property": "C Q E"
	},
	"lt": {
		"name": "ltVersion",
		"description": "This flag is used to specify the Maya LT version that this control feature was introduced,"
		" if the version flag is not specified, or if the version flag is specified but its argument"
		" is different. This value is only used by Maya LT, and otherwise ignored. The argument"
		" should be given as a string of the version number (e.g. \"2013\", \"2014\"). Currently"
		" only accepts major version numbers (e.g. 2013 Ext 1, or 2013.5 should be given as \"2014\").",
		"type": "string",
		"property": "C Q E"
	},
	"ob": {
		"name": "optionBox",
		"description": "Indicates that the menu item will be an option box item. This item will appear to the right"
		" of the preceeding menu item.",
		"type": "boolean",
		"property": "C Q"
	},
	"obi": {
		"name": "optionBoxIcon",
		"description": "The filename of an icon to be used instead of the usual option box icon. The icon is searched"
		" for in the folder specified by the XBMLANGPATH environment variable. The icon can be any"
		" size, but will be resized to the standard 16x16 pixels when drawn.",
		"type": "string",
		"property": "C Q E"
	},
	"p": {
		"name": "parent",
		"description": "Specify the menu that the item will appear in.",
		"type": "string",
		"property": "C"
	},
	"pmc": {
		"name": "postMenuCommand",
		"description": "Specify a script to be executed when the submenu is about to be shown.",
		"type": "script",
		"property": "C Q E"
	},
	"pmo": {
		"name": "postMenuCommandOnce",
		"description": "Indicate the pmc/postMenuCommand should only be invoked once. Default value is false, ie."
		" the pmc/postMenuCommand is invoked everytime the sub menu is shown.",
		"type": "boolean",
		"property": "C Q E"
	},
	"rp": {
		"name": "radialPosition",
		"description": "The radial position of the menu item if it is in a Marking Menu. Radial positions are given"
		" in the form of a cardinal direction, and may be \"N\", \"NW\", \"W\", \"SW\", \"S\", \"SE\","
		" \"E\" or \"NE\".",
		"type": "string",
		"property": "C Q E"
	},
	"rb": {
		"name": "radioButton",
		"description": "Creates a radio button menu item. Argument specifies the radio button value.",
		"type": "boolean",
		"property": "C Q E"
	},
	"rtc": {
		"name": "runTimeCommand",
		"description": "A shortcut flag to link the menu item with a runTimeCommand. The value is the name of the"
		" runTimeCommand (unique). It copies the following fields from the runTimeCommand if those"
		" fields have not been provided to this command: label, annotation, image, command. Note:"
		" command will be set to the runTimeCommand itself.",
		"type": "string",
		"property": "C E"
	},
	"stp": {
		"name": "sourceType",
		"description": "Set the language type for a command script. Can only be used in conjunction with a command"
		" flag. Without this flag, commands are assumed to be the same language of the executing"
		" script. In query mode, will return the language of the specified command. Valid values"
		" are \"mel\" and \"python\".",
		"type": "string",
		"property": "C Q E"
	},
	"sm": {
		"name": "subMenu",
		"description": "Indicates that the item will have a submenu. Subsequent menuItems will be added to the"
		" submenu until setParent -menu is called. Note that a submenu item creates a menu object"
		" and consequently the menu command may be used on the submenu item.",
		"type": "boolean",
		"property": "C Q"
	},
	"to": {
		"name": "tearOff",
		"description": "For the case where the menu item is a sub menu this flag will make the sub menu tear-off-able."
		" Note that this flag has no effect on the other menu item types.",
		"type": "boolean",
		"property": "C Q"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "C"
	},
	"ver": {
		"name": "version",
		"description": "Specify the version that this menu item feature was introduced. The argument should be"
		" given as a string of the version number (e.g. \"2013\", \"2014\"). Currently only accepts"
		" major version numbers (e.g. 2013 Ext 1, or 2013.5 should be given as \"2014\").",
		"type": "string",
		"property": "C Q E"
	},
	"vis": {
		"name": "visible",
		"description": "The visible state of the menu item. A menu item is created visible by default. Note that"
		" a menu item's actual appearance is also dependent on the visible state of its parent layout(s).",
		"type": "boolean",
		"property": "C Q E"
	},
}
