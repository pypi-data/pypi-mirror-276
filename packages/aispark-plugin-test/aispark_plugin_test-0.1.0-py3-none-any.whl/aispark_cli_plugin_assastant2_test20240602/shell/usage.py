from time import ctime

from aispark-cli-plugin-assastant2-test20240602 import __version__


def run():
    cur_time = ctime()
    text = f"""
    # aispark-cli-plugin-assastant2-test20240602

    version {__version__} ({cur_time} +0800)
    """
    print(text)
