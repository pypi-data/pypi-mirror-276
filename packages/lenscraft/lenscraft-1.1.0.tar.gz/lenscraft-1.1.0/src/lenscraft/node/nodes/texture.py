from pathlib import Path
import pickle
import cv2
import dearpygui.dearpygui as dpg
import numpy as np

from lenscraft.gabor import Gabor
from lenscraft.node import Node, NodeOutput
from lenscraft.node.attributes import (
    ImageNodeInput,
    ImageNodeOutput,
)
from lenscraft.texture import TextureModelLibrary
from lenscraft.texture.model import ClassificationModel


class ObjectSVMNode(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Find Texture"
        self.inputs = [ImageNodeInput("Image", self)]
        self.outputs = [ImageNodeOutput("Result", self)]

        self.texture_select = TextureLibraryAttribute(
            "Texture Model", self, context.texture_library
        )
        self.texture_select.add_callback(self._on_select)

    def compute(self):
        image = self.get_input_value("Image")
        print("Image shape", image.shape)
        h, w = image.shape[0:2]
        gabor = Gabor()
        features = gabor.generate_features(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        fv = features.all()
        result = self.model.predict(fv).reshape((h, w))
        result = (result * 255).astype(np.uint8)

        # TODO: turning this into a color image is silly
        print("Result shape", result.shape)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        self.set_output_value("Result", result)

    def draw_config(self):
        super().draw_config()
        self.texture_select.draw()

    def _on_select(self, model):
        print("load model", model)
        self.model = ClassificationModel.load(model)

class TextureLibraryAttribute(NodeOutput):
    def __init__(self, name, node, library: TextureModelLibrary):
        super().__init__(name, node)
        self.library = library
        self.library.on_update(self._on_library_update)
        self.option_dict = {}
        self.callback = None

    def draw(self):
        image_names = self.options()
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Static, tag=self.id
        ) as attr:
            self.combo_id = dpg.add_combo(
                image_names, label=self.name, width=200, callback=self._item_selected
            )
            self.preview_container = attr

            dpg.add_button(label="Create Texture", width=200, height=20, callback=self._on_new_texture_btn)

    def add_callback(self, callback):
        self.callback = callback

    def _on_new_texture_btn(self):
        dpg.show_item("TextureToolWindow")

    def options(self):
        self.option_dict = {}
        for i, path in enumerate(self.library.models):
            key = f"({i}) {Path(path).name}"
            self.option_dict[key] = path
        return [str(k) for k in self.option_dict.keys()]

    def lookup(self, option: str) -> str:
        return self.option_dict[option]

    def _item_selected(self, caller, app_data):
        model = self.lookup(app_data)
        if self.callback:
            self.callback(model)

    def _on_library_update(self):
        image_names = self.options()
        dpg.configure_item(self.combo_id, items=image_names)