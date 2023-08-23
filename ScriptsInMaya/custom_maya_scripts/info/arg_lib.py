arg_lib = {
"button": {
    "aop": {
        "name": "actOnPress",
        "description": "If true then the command specified by the command flag will be executed when a mouse button"
                       " is pressed. If false then that command will be executed after the mouse button is released."
                       " The default value is false.",
        "type": "boolean",
        "property": "Create|Query|Edit"
    },
    "ais": {
        "name": "actionIsSubstitute",
        "description": "This flag is obsolete and should no longer be used.",
        "type": "boolean",
        "property": "Create|Query|Edit"
    },
    "al": {
        "name": "align",
        "description": "This flag is obsolete and should no longer be used. The button label will always be "
                       "center-aligned.",
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
                       "color components. Each component ranges in value from 0.0 to 1.0. When setting backgroundColor,"
                       " the background is automatically enabled, unless enableBackground is also specified with"
                       " a false value.",
        "type": "[float, float, float]",
        "property": "Create|Query|Edit"
    },
    "c": {
        "name": "command",
        "description": "Command executed when the control is pressed.",
        "type": "script",
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
                       " int $x, int $y, int $mods  The proc returns a string array that is transferred to the"
                       " drop site. By convention the first string in the array describes the user settable message"
                       " type. Controls that are application defined drag sources may ignore the callback. $mods"
                       " allows testing for the key modifiers CTRL and SHIFT. Possible values are 0 == No modifiers,"
                       " 1 == SHIFT, 2 == CTRL, 3 == CTRL + SHIFT.  In Python, it is similar, but there are two"
                       " ways to specify the callback. The recommended way is to pass a Python function object"
                       " as the argument. In that case, the Python callback should have the form:  def callbackName"
                       " dragControl, x, y, modifiers :  The values of these arguments are the same as those for"
                       " the MEL version above.  The other way to specify the callback in Python is to specify"
                       " a string to be executed. In that case, the string will have the values substituted into"
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
                       "site. The MEL version of the callback is of the form: global proc callbackNamestring "
                       "$dragControl,"
                       " string $dropControl, string $msgs[], int $x, int $y, int $type  The proc receives a string"
                       " array that is transferred from the drag source. The first string in the msgs array describes"
                       " the user defined message type. Controls that are application defined drop sites may ignore"
                       " the callback. $type can have values of 1 == Move, 2 == Copy, 3 == Link.  In Python, it"
                       " is similar, but there are two ways to specify the callback. The recommended way is to"
                       " pass a Python function object as the argument. In that case, the Python callback should"
                       " have the form:  def pythonDropTest dragControl, dropControl, messages, x, y, dragType"
                       " :  The values of these arguments are the same as those for the MEL version above.  The"
                       " other way to specify the callback in Python is to specify a string to be executed. In"
                       " that case, the string will have the values substituted into it via the standard Python"
                       " format operator. The format values are passed in a dictionary with the keys \"dragControl\","
                       " \"dropControl\", \"messages\", \"x\", \"y\", \"type\". The \"dragControl\" value is a"
                       "string and the other values are integers eg the callback string could be \"print '%dragControls"
                       " %dropControls %messagesr %xd %yd %typed'\"",
        "type": "script",
        "property": "Create|Edit"
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
},
"menuItem": {
	"aob": {
		"name": "allowOptionBoxes",
		"description": "Deprecated. All menus and menu items always allow option boxes. In the case of submenu"
		" items this flag specifies whether the submenu will be able to support option box menu"
		" items. Always returns true.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"ann": {
		"name": "annotation",
		"description": "Annotate the menu item with an extra string value.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"bld": {
		"name": "boldFont",
		"description": "Specify if text should be bold. Only supported in menus which use the marking menu implementation."
		" Default is false for Windows, and true for all other platforms.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"cb": {
		"name": "checkBox",
		"description": "Creates a check box menu item. Argument specifies the check box value.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"cl": {
		"name": "collection",
		"description": "To explicitly add a radio menu item to a radioMenuItemCollection.",
		"type": "string",
		"property": "Create|Query"
	},
	"c": {
		"name": "command",
		"description": "Attaches a command/script that will be executed when the item is selected. Note this command"
		" is not executed when the menu item is in an optionMenu control.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"da": {
		"name": "data",
		"description": "Attaches a piece of user-defined data to the menu item.",
		"type": "int",
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
	"d": {
		"name": "divider",
		"description": "Creates a divider menu item.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"dl": {
		"name": "dividerLabel",
		"description": "Adds a label to a divider menu item.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"dtg": {
		"name": "docTag",
		"description": "Attaches a tag to the menu item.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ddc": {
		"name": "dragDoubleClickCommand",
		"description": "If the menu item is put on the shelf then this command will be invoked when the corresponding"
		" shelf object is double clicked.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"dmc": {
		"name": "dragMenuCommand",
		"description": "If the menu item is put on the shelf then this command will be invoked when the corresponding"
		" shelf object is clicked.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"ec": {
		"name": "echoCommand",
		"description": "Specify whether the action attached with the c/command flag should echo to the command"
		" output areas when invoked. This flag is false by default and must be specified with the"
		" c/command flag.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"en": {
		"name": "enable",
		"description": "Enable state for the menu item. A disabled menu item is dimmed and unresponsive. An enabled"
		" menu item is selectable and has normal appearance.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ecr": {
		"name": "enableCommandRepeat",
		"description": "This flag only affects menu items to which a command can be attached. Specify true and"
		" the command may be repeated by executing the command repeatLast. This flag is true by"
		" default for all items except for option box items.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "Create"
	},
	"fi": {
		"name": "familyImage",
		"description": "Get the filename of the family icon associated with the menu. The family icon will be used"
		" for the shelf unless an icon is specified with the image flag.",
		"type": "string",
		"property": "Query"
	},
	"i": {
		"name": "image",
		"description": "The filename of the icon associated with the menu item. If the menu containing the menu"
		" item is being edited with a menuEditor widget, then the menuEditor will use this icon"
		" to represent the menu item. This icon will be displayed on the shelf when the menu item"
		" is placed there.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"iol": {
		"name": "imageOverlayLabel",
		"description": "Specify a short (5 character) text string to be overlayed on top of the icon associated"
		" with the menu item. This is primarily a mechanism for differentiating menu items that"
		" are using a Family icon due to the fact that an icon image had not been explicitly defined."
		" The image overlay label will not be used if an icon image is defined for the menu item.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ia": {
		"name": "insertAfter",
		"description": "Specify After which item the new one will be placed. If this flag is not specified, item"
		" is added at the end of the menu. Use the empty string \"\" to insert before the first"
		" item of the menu.",
		"type": "string",
		"property": "Create"
	},
	"icb": {
		"name": "isCheckBox",
		"description": "Returns true if the item is a check box item.",
		"type": "boolean",
		"property": "Query"
	},
	"iob": {
		"name": "isOptionBox",
		"description": "Returns true if the item is an option box item.",
		"type": "boolean",
		"property": "Query"
	},
	"irb": {
		"name": "isRadioButton",
		"description": "Returns true if the item is a radio button item.",
		"type": "boolean",
		"property": "Query"
	},
	"itl": {
		"name": "italicized",
		"description": "Specify if text should be italicized. Only supported in menus which use the marking menu"
		" implementation. Default is false.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"l": {
		"name": "label",
		"description": "The text that appears in the item.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ld": {
		"name": "longDivider",
		"description": "Indicate whether the divider is long or short. Has no effect if divider label is set. Default"
		" is true.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"lt": {
		"name": "ltVersion",
		"description": "This flag is used to specify the Maya LT version that this control feature was introduced,"
		" if the version flag is not specified, or if the version flag is specified but its argument"
		" is different. This value is only used by Maya LT, and otherwise ignored. The argument"
		" should be given as a string of the version number (e.g. \"2013\", \"2014\"). Currently"
		" only accepts major version numbers (e.g. 2013 Ext 1, or 2013.5 should be given as \"2014\").",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ob": {
		"name": "optionBox",
		"description": "Indicates that the menu item will be an option box item. This item will appear to the right"
		" of the preceeding menu item.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"obi": {
		"name": "optionBoxIcon",
		"description": "The filename of an icon to be used instead of the usual option box icon. The icon is searched"
		" for in the folder specified by the XBMLANGPATH environment variable. The icon can be any"
		" size, but will be resized to the standard 16x16 pixels when drawn.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"p": {
		"name": "parent",
		"description": "Specify the menu that the item will appear in.",
		"type": "string",
		"property": "Create"
	},
	"pmc": {
		"name": "postMenuCommand",
		"description": "Specify a script to be executed when the submenu is about to be shown.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"pmo": {
		"name": "postMenuCommandOnce",
		"description": "Indicate the pmc/postMenuCommand should only be invoked once. Default value is false, ie."
		" the pmc/postMenuCommand is invoked everytime the sub menu is shown.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"rp": {
		"name": "radialPosition",
		"description": "The radial position of the menu item if it is in a Marking Menu. Radial positions are given"
		" in the form of a cardinal direction, and may be \"N\", \"NW\", \"W\", \"SW\", \"S\", \"SE\","
		" \"E\" or \"NE\".",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"rb": {
		"name": "radioButton",
		"description": "Creates a radio button menu item. Argument specifies the radio button value.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"rtc": {
		"name": "runTimeCommand",
		"description": "A shortcut flag to link the menu item with a runTimeCommand. The value is the name of the"
		" runTimeCommand (unique). It copies the following fields from the runTimeCommand if those"
		" fields have not been provided to this command: label, annotation, image, command. Note:"
		" command will be set to the runTimeCommand itself.",
		"type": "string",
		"property": "Create|Edit"
	},
	"stp": {
		"name": "sourceType",
		"description": "Set the language type for a command script. Can only be used in conjunction with a command"
		" flag. Without this flag, commands are assumed to be the same language of the executing"
		" script. In query mode, will return the language of the specified command. Valid values"
		" are \"mel\" and \"python\".",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"sm": {
		"name": "subMenu",
		"description": "Indicates that the item will have a submenu. Subsequent menuItems will be added to the"
		" submenu until setParent -menu is called. Note that a submenu item creates a menu object"
		" and consequently the menu command may be used on the submenu item.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"to": {
		"name": "tearOff",
		"description": "For the case where the menu item is a sub menu this flag will make the sub menu tear-off-able."
		" Note that this flag has no effect on the other menu item types.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "Create"
	},
	"ver": {
		"name": "version",
		"description": "Specify the version that this menu item feature was introduced. The argument should be"
		" given as a string of the version number (e.g. \"2013\", \"2014\"). Currently only accepts"
		" major version numbers (e.g. 2013 Ext 1, or 2013.5 should be given as \"2014\").",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"vis": {
		"name": "visible",
		"description": "The visible state of the menu item. A menu item is created visible by default. Note that"
		" a menu item's actual appearance is also dependent on the visible state of its parent layout(s).",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
},
"optionMenu": {
	"acc": {
		"name": "alwaysCallChangeCommand",
		"description": "Toggle whether to always call the change command, regardless of the change.",
		"type": "boolean",
		"property": "Create|Query"
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
	"bsp": {
		"name": "beforeShowPopup",
		"description": "Callback that is called just before we show the drop down menu.",
		"type": "script",
		"property": "Create|Edit"
	},
	"cc": {
		"name": "changeCommand",
		"description": "Adds a callback that is called when a new item is selected. The MEL script will have the"
		" newly selected item's value substituted for #1. For Python, the callback should be a callable"
		" object which accepts one argument, which is the newly selected item's value.",
		"type": "script",
		"property": "Create|Edit"
	},
	"dt": {
		"name": "defineTemplate",
		"description": "Puts the command in a mode where any other flags and arguments are parsed and added to"
		" the command template specified in the argument. They will be used as default arguments"
		" in any subsequent invocations of the command when templateName is set as the current template.",
		"type": "string",
		"property": "Create"
	},
	"dai": {
		"name": "deleteAllItems",
		"description": "Delete all the items in this menu.",
		"type": "boolean",
		"property": "Edit"
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
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Query"
	},
	"ill": {
		"name": "itemListLong",
		"description": "The long names of the menu items.",
		"type": "boolean",
		"property": "Query"
	},
	"ils": {
		"name": "itemListShort",
		"description": "The short names of the menu items.",
		"type": "boolean",
		"property": "Query"
	},
	"l": {
		"name": "label",
		"description": "The optional label text to the left of the popup menu.",
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
	"mvi": {
		"name": "maxVisibleItems",
		"description": "The maximum number of items that are visible in the popup menu. If the popup contains more"
		" items than this, a scrollbar is added automatically.",
		"type": "int",
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
	"ni": {
		"name": "numberOfItems",
		"description": "The number of menu items.",
		"type": "boolean",
		"property": "Query"
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
	"pmc": {
		"name": "postMenuCommand",
		"description": "Specify a script to be executed when the popup menu is about to be shown.",
		"type": "script",
		"property": "Create|Edit"
	},
	"pmo": {
		"name": "postMenuCommandOnce",
		"description": "Indicate the -pmc/postMenuCommand should only be invoked once. Default value is false,"
		" ie. the -pmc/postMenuCommand is invoked every time the popup menu is shown.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"po": {
		"name": "preventOverride",
		"description": "If true, this flag prevents overriding the control's attribute via the control's right"
		" mouse button menu.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"sl": {
		"name": "select",
		"description": "The current menu item. The argument and return value is 1-based. Note that the current"
		" menu item can only be set if it is enabled.",
		"type": "int",
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
	"v": {
		"name": "value",
		"description": "The text of the current menu item.",
		"type": "string",
		"property": "Create|Query|Edit"
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
},
"rowColumnLayout": {
	"adj": {
		"name": "adjustableColumn",
		"description": "Specifies which column has an adjustable size that changes with the sizing of the layout.",
		"type": "int",
		"property": "Create|Edit"
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
	"ca": {
		"name": "childArray",
		"description": "Returns a string array of the names of the layout's immediate children.",
		"type": "boolean",
		"property": "Query"
	},
	"cal": {
		"name": "columnAlign",
		"description": "Alignment for text and pixmaps in the specified column. Values are: \"left\", \"right\""
		" and \"center\". Only valid for column format, ie. number of columns specified with -nc/numberOfColumns"
		" flag.",
		"type": "[int, string]",
		"property": "Create|Edit|Multi-use"
	},
	"cat": {
		"name": "columnAttach",
		"description": "The attachments and offsets for the children in the specified column. The first argument"
		" is the 1-based column index. The second argument is the attachment, valid values are \"left\","
		" \"right\" and \"both\". The third argument must be greater than 0 and specifies the offset.",
		"type": "[int, string, int]",
		"property": "Create|Edit|Multi-use"
	},
	"co": {
		"name": "columnOffset",
		"description": "The attachment offset for the specified column. The first argument is the 1-based column"
		" index. The second argument is the attachment, valid values are \"left\", \"right\" and"
		" \"both\". The third argument must be greater than 0 and specifies the offset.",
		"type": "[int, string, int]",
		"property": "Create|Edit|Multi-use"
	},
	"cs": {
		"name": "columnSpacing",
		"description": "The space between columns in pixels. In column format this flag specifies that the space"
		" be to the left of the given column. In row format it specifies the space between all columns,"
		" however a valid column index is still required. The first argument is the 1-based column"
		" index. The second argument must be greater than 0 and specifies the spacing.",
		"type": "[int, int]",
		"property": "Create|Edit|Multi-use"
	},
	"cw": {
		"name": "columnWidth",
		"description": "Width of a column. This flag is valid only in column format. The column width must be greater"
		" than 0. The first argument is the 1-based column index. The second argument must be greater"
		" than 0 and specifies the column width.",
		"type": "[int, int]",
		"property": "Create|Edit|Multi-use"
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
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Query"
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
	"nch": {
		"name": "numberOfChildren",
		"description": "Returns in an int the number of immediate children of the layout.",
		"type": "boolean",
		"property": "Query"
	},
	"nc": {
		"name": "numberOfColumns",
		"description": "Number of columns. This flag is mutually exclusive to the -nr/numRows flag. Either one"
		" or the other can be specified.",
		"type": "int",
		"property": "Create|Query"
	},
	"npm": {
		"name": "numberOfPopupMenus",
		"description": "Return the number of popup menus attached to this control.",
		"type": "boolean",
		"property": "Query"
	},
	"nr": {
		"name": "numberOfRows",
		"description": "Number of rows. This flag is mutually exclusive to the -nc/numColumns flag. Either one"
		" or the other can be specified.",
		"type": "int",
		"property": "Create|Query"
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
	"ral": {
		"name": "rowAlign",
		"description": "Alignment for text and pixmaps in the specified row. Values are: \"left\", \"right\" and"
		" \"center\". Only valid for row format, ie. number of rows specified with -nr/numberOfRows"
		" flag.",
		"type": "[int, string]",
		"property": "Create|Edit|Multi-use"
	},
	"rat": {
		"name": "rowAttach",
		"description": "The attachments and offsets for the children in the specified row. The first argument is"
		" the 1-based row index. The second argument is the attachment, valid values are \"top\","
		" \"bottom\" and \"both\". The third argument must be greater than 0 and specifies the offset.",
		"type": "[int, string, int]",
		"property": "Create|Edit|Multi-use"
	},
	"rh": {
		"name": "rowHeight",
		"description": "Height of a row. This flag is only valid in row format. The row height must be greater"
		" than 0. The first argument is the 1-based row index. The second argument must be greater"
		" than 0 and specifies the row height.",
		"type": "[int, int]",
		"property": "Create|Edit|Multi-use"
	},
	"ro": {
		"name": "rowOffset",
		"description": "The attachment offset for the specified row. The first argument is the 1-based row index."
		" The second argument is the attachment, valid values are \"top\", \"bottom\" and \"both\"."
		" The third argument must be greater than 0 and specifies the offset.",
		"type": "[int, string, int]",
		"property": "Create|Edit|Multi-use"
	},
	"rs": {
		"name": "rowSpacing",
		"description": "The space between rows, in pixels. In row format this specifies the space above the specified"
		" row. In column format it specifies the space between all rows, however a valid row index"
		" is still required. The first argument is the 1-based row index. The second argument must"
		" be greater than 0 and specifies the spacing.",
		"type": "[int, int]",
		"property": "Create|Edit|Multi-use"
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
},
"tabLayout": {
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
	"bs": {
		"name": "borderStyle",
		"description": "Specify the style of the border for tab layout. Valid values are: \"none\", \"top\", \"notop\""
		" and \"full\". By default, it will use \"full\" to draw a simple frame around the body"
		" area of the tab layout. \"none\" - Do not draw borders around the body area of the tab"
		" layout \"top\" - Only draw a simple line right below the tabs \"notop\" - Draw a simple"
		" frame on the left/right/bottom no top of the tab layout \"full\" - Draw a simple frame"
		" around the body area of the tab layout",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"cc": {
		"name": "changeCommand",
		"description": "Command executed when a tab is selected interactively. This command is only invoked when"
		" the selected tab changes. Re-selecting the current tab will not invoke this command.",
		"type": "script",
		"property": "Create|Edit"
	},
	"ca": {
		"name": "childArray",
		"description": "Returns a string array of the names of the layout's immediate children.",
		"type": "boolean",
		"property": "Query"
	},
	"cr": {
		"name": "childResizable",
		"description": "Set to true if you want the child of the control layout to be as wide as the scroll area."
		" You may also indicate a minimum width for the child using the -mcw/minChildWidth flag.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"ct": {
		"name": "closeTab",
		"description": "Close the tab at the given index.",
		"type": "int",
		"property": "Create|Edit"
	},
	"ctc": {
		"name": "closeTabCommand",
		"description": "Specify a script to be executed when one of the tabs are closed by clicking on the header"
		" widget (MMB or X button).",
		"type": "script",
		"property": "Create|Edit"
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
	"dcc": {
		"name": "doubleClickCommand",
		"description": "Command executed when a tab is double clicked on. Note that the first click will select"
		" the tab and the second click will execute the double click command. Double clicking the"
		" current tab will re-invoke the double click command.",
		"type": "script",
		"property": "Create|Edit"
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
	"hst": {
		"name": "horizontalScrollBarThickness",
		"description": "Thickness of the horizontal scroll bar. Specify an integer value greater than or equal"
		" to zero. This flag has no effect on Windows systems.",
		"type": "int",
		"property": "Create|Edit"
	},
	"i": {
		"name": "image",
		"description": "Image appearing in top right corner of tab layout.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"iv": {
		"name": "imageVisible",
		"description": "Visibility of tab image.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"imh": {
		"name": "innerMarginHeight",
		"description": "Margin height for all tab children.",
		"type": "int",
		"property": "Create|Query"
	},
	"imw": {
		"name": "innerMarginWidth",
		"description": "Margin width for all tab children.",
		"type": "int",
		"property": "Create|Query"
	},
	"io": {
		"name": "isObscured",
		"description": "Return whether the control can actually be seen by the user. The control will be obscured"
		" if its state is invisible, if it is blocked (entirely or partially) by some other control,"
		" if it or a parent layout is unmanaged, or if the control's window is invisible or iconified.",
		"type": "boolean",
		"property": "Query"
	},
	"m": {
		"name": "manage",
		"description": "Manage state of the control. An unmanaged control is not visible, nor does it take up any"
		" screen real estate. All controls are created managed by default.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"mcw": {
		"name": "minChildWidth",
		"description": "Specify a positive non-zero integer value indicating the minimum width the tab layout's"
		" children. This flag only has meaning when the -cr/childResizable flag is set to true.",
		"type": "int",
		"property": "Create|Query"
	},
	"mt": {
		"name": "moveTab",
		"description": "Move the tab from the current index to a new index.",
		"type": "[int, int]",
		"property": "Create|Edit"
	},
	"ntc": {
		"name": "newTabCommand",
		"description": "Command executed when the 'New Tab' button (on the tab bar) is clicked. Note: in order"
		" to show the new tab button use the -snt/showNewTab flag. Using this command will override"
		" any internal Maya logic for adding a new tab (only this command will be executed).",
		"type": "script",
		"property": "Create|Edit"
	},
	"nbg": {
		"name": "noBackground",
		"description": "Clear/reset the control's background. Passing true means the background should not be drawn"
		" at all, false means the background should be drawn. The state of this flag is inherited"
		" by children of this control.",
		"type": "boolean",
		"property": "Create|Edit"
	},
	"nch": {
		"name": "numberOfChildren",
		"description": "Returns in an int the number of immediate children of the layout.",
		"type": "boolean",
		"property": "Query"
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
	"pmc": {
		"name": "postMenuCommand",
		"description": "Specify a script to be executed when the popup menu is about to be shown.",
		"type": "script",
		"property": "Create|Edit"
	},
	"psc": {
		"name": "preSelectCommand",
		"description": "Command executed when a tab is selected but before it's contents become visible. Re-selecting"
		" the current tab will not invoke this command. Note that this command is not executed by"
		" using either of the -st/selectTab or -sti/selectTabIndex flags.",
		"type": "script",
		"property": "Create|Edit"
	},
	"po": {
		"name": "preventOverride",
		"description": "If true, this flag prevents overriding the control's attribute via the control's right"
		" mouse button menu.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"scr": {
		"name": "scrollable",
		"description": "Puts all children of this layout within a scroll area.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"stb": {
		"name": "scrollableTabs",
		"description": "If true, the active tab in the layout can be scrolled through with the mouse wheel. Default"
		" is true.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"sc": {
		"name": "selectCommand",
		"description": "Command executed when a tab is selected interactively This command will be invoked whenever"
		" a tab is selected, ie. re-selecting the current tab will invoke this command. Note that"
		" this command is not executed by using either of the -st/selectTab or -sti/selectTabIndex"
		" flags.",
		"type": "script",
		"property": "Create|Query|Edit"
	},
	"st": {
		"name": "selectTab",
		"description": "The name, in short form, of the selected tab. An empty string is returned on query if there"
		" are no child tabs.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"sti": {
		"name": "selectTabIndex",
		"description": "Identical to the -st/selectTab flag except this flag takes a 1-based index to identify"
		" the selected tab. A value of 0 is returned on query if there are no child tabs.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"snt": {
		"name": "showNewTab",
		"description": "Set to true if you want to have a 'New Tab' button shown at the end of the tab bar. Note:"
		" use the -ntc/newTabCommand flag to set the command executed when this button is clicked.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"sbm": {
		"name": "statusBarMessage",
		"description": "Extra string to display in the status bar when the mouse is over the control.",
		"type": "string",
		"property": "Create|Edit"
	},
	"ti": {
		"name": "tabIcon",
		"description": "Set an icon for a tab. The first argument is the name of a control that must be a child"
		" of the tab layout. The second argument is the icon file name.",
		"type": "[string, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tii": {
		"name": "tabIconIndex",
		"description": "Identical to the -ti/tabIcon flag except this flag takes a 1-based index to identify the"
		" tab you want to set the icon for. If this flag is queried the tab icons for all the children"
		" are returned.",
		"type": "[int, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tl": {
		"name": "tabLabel",
		"description": "Set a tab label. The first argument is the name of a control that must be a child of the"
		" tab layout. The second argument is the label for the tab associated with that child. If"
		" this flag is queried then the tab labels for all the children are returned.",
		"type": "[string, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tli": {
		"name": "tabLabelIndex",
		"description": "Identical to the -tl/tabLabel flag except this flag takes a 1-based index to identify the"
		" tab you want to set the label for. If this flag is queried the tab labels for all the"
		" children are returned.",
		"type": "[int, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tp": {
		"name": "tabPosition",
		"description": "Changes the tab position. The possible values are: \"north\", \"east\" and \"west\".",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"tt": {
		"name": "tabTooltip",
		"description": "Set a tab tooltip. The first argument is the name of a control that must be a child of"
		" the tab layout. The second argument is the tooltip for the tab associated with that child."
		" If this flag is queried then the tab tooltips for all the children are returned.",
		"type": "[string, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tti": {
		"name": "tabTooltipIndex",
		"description": "Identical to the -tt/tabTooltip flag except this flag takes a 1-based index to identify"
		" the tab you want to set the tooltip for. If this flag is queried the tab tooltips for"
		" all the children are returned.",
		"type": "[int, string]",
		"property": "Create|Query|Edit|Multi-use"
	},
	"tc": {
		"name": "tabsClosable",
		"description": "Set to true if you want to have a close button icon on all created tabs.",
		"type": "boolean",
		"property": "Create|Query"
	},
	"tv": {
		"name": "tabsVisible",
		"description": "Visibility of the tab labels.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "Create"
	},
	"vst": {
		"name": "verticalScrollBarThickness",
		"description": "Thickness of the vertical scroll bar. Specify an integer value greater than or equal to"
		" zero. This flag has no effect on Windows systems.",
		"type": "int",
		"property": "Create|Edit"
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
},
"textField": {
	"aie": {
		"name": "alwaysInvokeEnterCommandOnReturn",
		"description": "Sets whether to always invoke the enter command when the return key is pressed by the user."
		" By default, this option is false.",
		"type": "boolean",
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
	"cc": {
		"name": "changeCommand",
		"description": "Command executed when the text changes. This command is not invoked when the value changes"
		" via the -tx/text flag.",
		"type": "script",
		"property": "Create|Edit"
	},
	"dt": {
		"name": "defineTemplate",
		"description": "Puts the command in a mode where any other flags and arguments are parsed and added to"
		" the command template specified in the argument. They will be used as default arguments"
		" in any subsequent invocations of the command when templateName is set as the current template.",
		"type": "string",
		"property": "Create"
	},
	"db": {
		"name": "disableButtons",
		"description": "Sets the visibility state of search field buttons to true/false depending on the passed"
		" value. In Query mode returns whether both buttons are visible or not.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"dcb": {
		"name": "disableClearButton",
		"description": "Sets the visibility state of search field clear button to true/false depending on the passed"
		" value. In Query mode returns whether clear button of search field is visible or not.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"dhb": {
		"name": "disableHistoryButton",
		"description": "Sets the visibility state of search field history button to true/false depending on the"
		" passed value. In Query mode returns whether history button of search field is visible"
		" or not.",
		"type": "boolean",
		"property": "Create|Query|Edit"
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
	"dif": {
		"name": "drawInactiveFrame",
		"description": "Sets whether the text field draws itself with a frame when it's inactive. By default, this"
		" option is false.",
		"type": "boolean",
		"property": "Create|Query|Edit"
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
	"ed": {
		"name": "editable",
		"description": "The edit state of the field. By default, this flag is set to true and the field value may"
		" be changed by typing into it. If false then the field is 'read only' and can not be typed"
		" into. The text in the field can always be changed with the -tx/text flag regardless of"
		" the state of the -ed/editable flag.",
		"type": "boolean",
		"property": "Create|Query|Edit"
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
	"ec": {
		"name": "enterCommand",
		"description": "Command executed when the keypad 'Enter' key is pressed.",
		"type": "script",
		"property": "Create|Edit"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "Create"
	},
	"fi": {
		"name": "fileName",
		"description": "Text in the field as a filename. This does conversions between internal and external (UI)"
		" file representation.",
		"type": "string",
		"property": "Create|Query|Edit"
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
	"it": {
		"name": "insertText",
		"description": "Insert text into the field at the current insertion position (specified by the -ip/insertionPosition"
		" flag).",
		"type": "string",
		"property": "Create|Edit"
	},
	"ip": {
		"name": "insertionPosition",
		"description": "The insertion position for inserted text. This is a 1 based value where position 1 specifies"
		" the beginning of the field. Position 0 may be used to specify the end of the field.",
		"type": "int",
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
	"pht": {
		"name": "placeholderText",
		"description": "Setting this property makes the line edit display a grayed-out placeholder text as long"
		" as the text field is empty and the widget doesn't have focus. By default, this property"
		" contains an empty string.",
		"type": "string",
		"property": "Create|Query|Edit"
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
	"rfc": {
		"name": "receiveFocusCommand",
		"description": "Command executed when the field receives focus.",
		"type": "script",
		"property": "Create|Edit"
	},
	"sf": {
		"name": "searchField",
		"description": "Creates a search field instead of a text field.",
		"type": "boolean",
		"property": "Create"
	},
	"sbm": {
		"name": "statusBarMessage",
		"description": "Extra string to display in the status bar when the mouse is over the control.",
		"type": "string",
		"property": "Create|Edit"
	},
	"tx": {
		"name": "text",
		"description": "The field text.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"tcc": {
		"name": "textChangedCommand",
		"description": "Command executed immediately when the field text changes.",
		"type": "script",
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
},
"text": {
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
},
"window": {
	"bgc": {
		"name": "backgroundColor",
		"description": "The background color of the window. The arguments correspond to the red, green, and blue"
		" color components. Each component ranges in value from 0.0 to 1.0.",
		"type": "[float, float, float]",
		"property": "Create|Edit"
	},
	"cc": {
		"name": "closeCommand",
		"description": "Script executed after the window is closed.",
		"type": "script",
		"property": "Create|Edit"
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
		"description": "Attach a tag to the window.",
		"type": "string",
		"property": "Create|Query|Edit"
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
		"property": "Create|Multi-use"
	},
	"ds": {
		"name": "dockStation",
		"description": "When set this flag specifies that this window can contain other docked sub-windows.",
		"type": "boolean",
		"property": "Create"
	},
	"dl": {
		"name": "dockingLayout",
		"description": "When queried this flag will return a string holding the docking layout information. This"
		" string can be set when creating or editing a docking station to restore the previous docking"
		" layout. This string is a hexadecimal representation of a binary string and is not meant"
		" to be humanly readable, but can be saved and loaded using the optionVar command to restore"
		" layouts across sessions of Maya.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"ex": {
		"name": "exists",
		"description": "Returns whether the specified object exists or not. Other flags are ignored.",
		"type": "boolean",
		"property": "Create"
	},
	"fw": {
		"name": "frontWindow",
		"description": "Return the name of the front window. Note: you must supply the name of any window (the"
		" window does not need to exist). Returns \"unknown\" if the front window cannot be determined.",
		"type": "boolean",
		"property": "Query"
	},
	"h": {
		"name": "height",
		"description": "Height of the window excluding any window frame in pixels.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"iconName": {
		"name": "iconName",
		"description": "The window's icon title. By default it is the same as the window's title.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"i": {
		"name": "iconify",
		"description": "Icon state of the window.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ip": {
		"name": "interactivePlacement",
		"description": "Deprecated flag. Recognized but not implemented. This flag will be removed in a future"
		" version of Maya.",
		"type": "boolean",
		"property": "Create"
	},
	"le": {
		"name": "leftEdge",
		"description": "Position of the left edge of the window.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"mm": {
		"name": "mainMenuBar",
		"description": "If this flag is used then the main menu bar will be enabled.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"mw": {
		"name": "mainWindow",
		"description": "Main window for the application. The main window has an 'Exit' item in the Window Manager"
		" menu. By default, the first created window becomes the main window.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"mxb": {
		"name": "maximizeButton",
		"description": "Turns the window's maximize button on or off.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"ma": {
		"name": "menuArray",
		"description": "Return a string array containing the names of the menus in the window's menu bar.",
		"type": "boolean",
		"property": "Query"
	},
	"mb": {
		"name": "menuBar",
		"description": "Adds an empty menu bar to the window. The Qt name of the object will be m_menubar_nameOfTheWindow.",
		"type": "boolean",
		"property": "Create|Query"
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
		"property": "Create|Edit"
	},
	"mbr": {
		"name": "menuBarResize",
		"description": "This flag should be used with the -mcw/-menuBarCornerWidget flag. This is used to resize"
		" the menu bar so that the corner widgets are updated.",
		"type": "boolean",
		"property": "Edit"
	},
	"mbv": {
		"name": "menuBarVisible",
		"description": "Visibility of the menu bar (if there is one).",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"mi": {
		"name": "menuIndex",
		"description": "Sets the index of a specified menu.",
		"type": "[string, uint]",
		"property": "Edit"
	},
	"mnb": {
		"name": "minimizeButton",
		"description": "Turns the window's minimize button on or off.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"mnc": {
		"name": "minimizeCommand",
		"description": "Script executed after the window is minimized (iconified).",
		"type": "script",
		"property": "Create|Edit"
	},
	"nde": {
		"name": "nestedDockingEnabled",
		"description": "Controls whether nested docking is enabled or not. Nested docking allows for docking windows"
		" next to other docked windows for more possible arrangement styles.",
		"type": "boolean",
		"property": "Create"
	},
	"nm": {
		"name": "numberOfMenus",
		"description": "Return the number of menus attached to the window's menu bar.",
		"type": "boolean",
		"property": "Query"
	},
	"p": {
		"name": "parent",
		"description": "Specifies a parent window or layout which the created window is always on top of. Note:"
		" If the parent is a window the created window is not modal, so events are still propagated"
		" to the parent window.",
		"type": "string",
		"property": "Create"
	},
	"rtf": {
		"name": "resizeToFitChildren",
		"description": "The window will always grow/shrink to just fit the controls it contains.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"rc": {
		"name": "restoreCommand",
		"description": "Script executed after the window is restored from it's minimized (iconified) state.",
		"type": "script",
		"property": "Create|Edit"
	},
	"ret": {
		"name": "retain",
		"description": "Retains the window after it has been closed. The default is to delete the window when it"
		" is closed.",
		"type": "boolean",
		"property": "Create"
	},
	"s": {
		"name": "sizeable",
		"description": "Whether or not the window may be interactively resized.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"st": {
		"name": "state",
		"description": "When queried this flag will return a string holding the window state information. This"
		" string is a hexadecimal representation of a binary string and is not meant to be humanly"
		" readable, but can be saved and loaded using the optionVar command to restore window state"
		" across sessions of Maya.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"t": {
		"name": "title",
		"description": "The window's title.",
		"type": "string",
		"property": "Create|Query|Edit"
	},
	"tb": {
		"name": "titleBar",
		"description": "Turns the window's title bar on or off.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"tbm": {
		"name": "titleBarMenu",
		"description": "Controls whether the title bar menu exists in the window title bar. Only valid if -tb/titleBar"
		" is true. This Windows only flag is true by default.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"tlb": {
		"name": "toolbox",
		"description": "Makes this a toolbox style window. A Windows only flag that makes the title bar smaller"
		" and uses a slightly different display style.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"te": {
		"name": "topEdge",
		"description": "Position of the top edge of the window.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"tlc": {
		"name": "topLeftCorner",
		"description": "Position of the window's top left corner.",
		"type": "[int, int]",
		"property": "Create|Query|Edit"
	},
	"ut": {
		"name": "useTemplate",
		"description": "Forces the command to use a command template other than the current one.",
		"type": "string",
		"property": "Create"
	},
	"vis": {
		"name": "visible",
		"description": "The window's visibility.",
		"type": "boolean",
		"property": "Create|Query|Edit"
	},
	"w": {
		"name": "width",
		"description": "Width of the window excluding any window frame in pixels.",
		"type": "int",
		"property": "Create|Query|Edit"
	},
	"wh": {
		"name": "widthHeight",
		"description": "Window's width and height excluding any window frame in pixels.",
		"type": "[int, int]",
		"property": "Create|Query|Edit"
	},
}
}
