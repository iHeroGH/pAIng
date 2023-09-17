from typing import Any

class GameObject:
    def __init__(self):
        pass

    def get_drawable(self) -> tuple[Any]:
        raise NotImplemented()

    def set_rect(self, rect: Any):
        raise NotImplemented()