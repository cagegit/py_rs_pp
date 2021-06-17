import sys
import os


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = os.path.dirname(__file__)
        print(e)

    return os.path.join(base_path, relative_path)
