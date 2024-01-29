import sys
import os
import maya.cmds as cmds
from ui import _main_ui_  # noqa
from pathlib import Path


def set_maya_command_port():
    """Set Maya command line to Pycharm listener"""
    try:
        if not cmds.commandPort(":4434", query=True):
            cmds.commandPort(name=":4434")
        if cmds.commandPort(":4434", query=True):
            print("Maya command port set to 4434")
        else:
            print("Maya command port not set")
    except Exception as e:
        print("Error during Maya startup:", str(e))


def push_scripts_to_sys():
    """Add custom scripts folder to sys.path"""
    try:
        scripts_folder = str(Path(__file__).parent.parent)
        if scripts_folder not in sys.path:
            sys.path.append(scripts_folder)
            print("Custom scripts folder added to sys.path")
        else:
            print("Custom scripts folder already in sys.path")
    except Exception as e:
        print("Error during Maya startup:", str(e))


def set_tool_tab_on_start():
    """Create Custom Tools tab at the top of the Maya main window for every scene"""
    try:
        cmds.scriptJob(event=("SceneOpened", refresh_tools))
        cmds.scriptJob(event=("NewSceneOpened", refresh_tools))
        print("Custom Tools event added to Maya sceneOpened event")
        check = cmds.file(query=True, exists=True)
        open_scene = cmds.file(query=True, sceneName=True)
        print("Checking if scene is currently open...")
        if check and open_scene:
            print("CONFIRMED SCENE IS OPEN, running refresh_tools()")
            print("SCENE:", open_scene)
            refresh_tools()
    except Exception as e:
        print("Error during Maya startup:", str(e))


def refresh_tools():
    """Refresh the component menu"""
    try:
        _main_ui_.create_tools_menu()
    except Exception as e:
        print("Error during Maya startup:", str(e))


def get_substance_plugin_working():
    """
    Houdini Path holds the plugin hostage and makes substance unable to load
    Reordering the path fixes the issue, performing this fix below
    """
    try:
        print('reordering substance path')
        import os
        path = os.getenv('PATH')
        path_items = path.split(';')
        houdini_path = ''
        substance_path = ''
        for string in path_items:
            if 'Substance' in string:
                substance_path = string
                continue
            if 'Houdini' in string:
                houdini_path = string
                continue

        if substance_path:
            path_items.remove(substance_path)
        if houdini_path:
            path_items.remove(houdini_path)

        path_items.append(substance_path)
        path_items.append(houdini_path)

        path_reorder = ';'.join(path_items)
        os.environ["PATH"] = path_reorder
        print('substance path reordered')
    except Exception as e:
        print("Error during Maya startup:", str(e))


def set_maya_on_start():
    get_substance_plugin_working()
    set_maya_command_port()
    push_scripts_to_sys()
    set_tool_tab_on_start()


def create_user_setup(year: str = None, _open: bool = False):
    user_setup = str(Path(cmds.internalVar(userScriptDir=True) / "userSetup.py")) if \
        cmds.internalVar(userScriptDir=True) else \
        str(Path(Path.home() / f"documents/maya/{year}/scripts/userSetup.py")) if year else None
    try:
        if not Path(user_setup).parent.exists():
            raise FileNotFoundError(f"Could not find userSetup.py at {user_setup}")
    except TypeError:
        raise TypeError("Could not find userSetup.py")
    print(f"Provided Path Validated...\n---ATTEMPT--- Creating userSetup.py at: '{user_setup}'...")
    with open(user_setup, "w") as file:
        file.write(
            """import maya.cmds as cmds
from config.maya_setup import set_maya_on_start

cmds.evalDeferred('set_maya_on_start()', lowestPriority=True)
""")

    if Path(user_setup).exists():
        print(f"---SUCCESS--- created userSetup.py at {user_setup}")
        if _open:
            if sys.platform == "win32":
                os.startfile(user_setup)
    else:
        print(f"---FAIL--- to create userSetup.py at {user_setup}")


if __name__ == "__main__":
    set_maya_on_start()
    # refresh_tools()
    # create_user_setup("2024", _open=True)
