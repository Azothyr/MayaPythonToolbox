import sys
import os
import maya.cmds as cmds
from ui import _main_ui_ # noqa
from pathlib import Path


def set_maya_command_port():
    """Set Maya command line to Pycharm listener"""
    try:
        print("[INFO] Setting Maya command port to 4434")
        if not cmds.commandPort(":4434", query=True):
            cmds.commandPort(name=":4434")
        if cmds.commandPort(":4434", query=True):
            print("[INFO] SUCCESS | Maya command port set to 4434")
        else:
            print("[WARNING] FAILURE | Maya command port not set")
    except Exception as e:
        print("[ERROR] UNEXPECTED EXCEPTION | Error occured during Maya startup - Set Maya Command Port:", str(e))


def push_scripts_to_sys():
    """Add custom scripts folder to sys.path"""
    try:
        scripts_folder = str(Path(__file__).parent.parent)
        if scripts_folder not in sys.path:
            sys.path.append(scripts_folder)
            print("[INFO] SUCCESS | Custom scripts folder added to sys.path")
        else:
            print("[INFO] SKIPPING | Custom scripts folder already in sys.path")
    except Exception as e:
        print("[ERROR] UNEXPECTED EXCEPTION | Error occured during Maya startup - Push Scripts To Sys:", str(e))


def set_tool_tab_on_start():
    """Create Custom Tools tab at the top of the Maya main window for every scene"""
    try:
        cmds.scriptJob(event=("SceneOpened", refresh_tools))
        cmds.scriptJob(event=("NewSceneOpened", refresh_tools))
        print("[INFO] Custom Tools event added to Maya sceneOpened event")
        check = cmds.file(query=True, exists=True)
        open_scene = cmds.file(query=True, sceneName=True)
        print("[INFO] Checking if scene is currently open...")
        if check and open_scene:
            print("[INFO] CONFIRMED SCENE IS OPEN, running refresh_tools()")
            print("[INFO] SCENE:", open_scene)
            refresh_tools()
    except Exception as e:
        print("[ERROR] UNEXPECTED EXCEPTION | Error occured during Maya startup - Set Tool Tab on Start:", str(e))


def refresh_tools():
    """Refresh the component menu"""
    try:
        _main_ui_.create_tools_menu()
    except Exception as e:
        print("[ERROR] UNEXPECTED EXCEPTION | Error occured during Maya startup - Refresh Tools:", str(e))


def get_substance_plugin_working():
    """
    Houdini Path holds the plugin hostage and makes substance unable to load
    Reordering the path fixes the issue, performing this fix below
    """
    try:
        print('[INFO] reordering substance path')
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
        print('[INFO] SUCCESS | substance path reordered.')
    except Exception as e:
        print("[ERROR] UNEXPECTED EXCEPTION | Error occured during Maya startup - Get Substance Plugin Working:", str(e))


def set_maya_on_start():
    get_substance_plugin_working()
    set_maya_command_port()
    push_scripts_to_sys()
    set_tool_tab_on_start()


def create_user_setup(year: str = None, maya_is_open: bool = False):
    maya_app_dir = os.environ.get("MAYA_APP_DIR") or Path.home() / "Documents" / "maya"
    script_dir = Path(maya_app_dir) / f"{year}" / "scripts" if year else None
    user_setup = str(Path(script_dir) / "userSetup.py")

    try:
        if not Path(script_dir).exists():
            raise FileNotFoundError(f"---ERROR--- Could not find {script_dir}")
    except TypeError:
        raise TypeError(f"---ERROR--- Could not find {user_setup}")

    print(f"Provided Path Validated...\n---ATTEMPT--- Creating userSetup.py at: '{user_setup}'...")

    with open(user_setup, "w") as file:
        file.write(
            """import maya.cmds as cmds
from config.maya_setup import set_maya_on_start

try:
    print('[INFO] Running ZP Tools setup...')
    cmds.evalDeferred('set_maya_on_start()', lowestPriority=True)
except Exception as e:
    print('[ERROR] UNEXPECTED EXCEPTION | Error setting up ZP Tools during Maya startup:', str(e))
""")

    if Path(user_setup).exists():
        print(f"---SUCCESS--- created userSetup.py at {user_setup}")
        if maya_is_open:
            if sys.platform == "win32":
                os.startfile(user_setup)
    else:
        print(f"---FAIL--- failed to create userSetup.py at {user_setup}")


def set_maya_on_start():
    get_substance_plugin_working()
    set_maya_command_port()
    push_scripts_to_sys()
    set_tool_tab_on_start()


if __name__ == "__main__":
    # set_maya_on_start()
    # refresh_tools()
    # create_user_setup("2026", maya_is_open=True)
    create_user_setup("2026")
