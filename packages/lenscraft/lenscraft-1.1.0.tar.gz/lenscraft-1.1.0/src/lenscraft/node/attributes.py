import dearpygui.dearpygui as dpg

from lenscraft.image import DynamicTexture
from lenscraft.node import Node, NodeInput, NodeOutput


class ImageNodeInput(NodeInput):
    def __init__(self, name, node):
        super().__init__(name, node)

    def draw(self):
        with dpg.node_attribute(
            label=self.id, attribute_type=dpg.mvNode_Attr_Input, tag=self.id
        ):
            dpg.add_text("Image")


class NumberSliderAttribute(NodeInput):
    def __init__(self, name, node, max_value=100, min_value=0, initial_value=50):
        super().__init__(name, node)
        self.max_value = max_value
        self.min_value = min_value
        self.initial_value = initial_value
        self.value = initial_value

    def _callback(self, sender, app_data):
        self.update_value(app_data)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_slider_int(
                label=self.name,
                max_value=self.max_value,
                min_value=self.min_value,
                default_value=self.value,
                width=200,
                callback=self._callback,
            )


class IntNodeInput(NodeInput):
    def __init__(self, name, node: Node):
        super().__init__(name, node)
        self.value = 12

    def _callback(self, sender, app_data):
        self.update_value(app_data)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_input_int(
                label=self.name,
                default_value=self.value,
                width=100,
                callback=self._callback,
            )


class ImageNodeOutput(NodeOutput):
    def __init__(self, name, node):
        super().__init__(name, node)

        self.preview = None
        self.texture = None

    def draw(self):
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Output, tag=self.id
        ) as attr:
            dpg.add_text(self.name)
            self.preview_container = attr

    def set_value(self, new_value):
        super().set_value(new_value)

        if self.texture is None:
            self.texture = DynamicTexture(new_value)
        else:
            self.texture.update(new_value)

        if self.preview:
            dpg.delete_item(self.preview)
        self.preview = self.texture.add_to_parent(self.preview_container, width=200)


class ImageNodeInput(NodeInput):
    def __init__(self, name, node):
        super().__init__(name, node)

    def draw(self):
        with dpg.node_attribute(
            label=self.id, attribute_type=dpg.mvNode_Attr_Input, tag=self.id
        ):
            dpg.add_text("Image")
