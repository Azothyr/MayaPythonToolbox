from .set_attr import set_


def toggle_on(obj, attr):
    keyable(obj, attr)
    unhide(obj, attr)
    unlock(obj, attr)


def toggle_off(obj, attr):
    unkeyable(obj, attr)
    hide(obj, attr)
    lock(obj, attr)


def lock(obj, attr):
    set_(obj, attr=attr, lock=True)


def unlock(obj, attr):
    set_(obj, attr, lock=False)


def hide(obj, attr):
    set_(obj, attr, channelBox=False)


def unhide(obj, attr):
    set_(obj, attr, channelBox=True)


def keyable(obj, attr):
    set_(obj, attr, keyable=True)


def unkeyable(obj, attr):
    set_(obj, attr, keyable=False)
