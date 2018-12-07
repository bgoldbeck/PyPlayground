from src.rendering.scene_object import SceneObject


class Scene:
    def __init__(self):
        self.scene_objects = {}
        self.scene_objects["obj1"] = SceneObject()
        self.scene_objects["obj1"].load_model("test.stl")

    def draw(self):
        for key, value in self.scene_objects.items():
            value.draw()

    def get_scene_object(self, tag):
        return self.objects[tag]

