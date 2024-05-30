import dearpygui.dearpygui as dpg

from lenscraft.image import Image
from lenscraft.node import Node, NodeOutput


class ImageLibraryNode(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Image Library"
        self.inputs = []
        self.outputs = [ImageLibraryAttribute("Image", self, context.library)]


class ImageLibraryAttribute(NodeOutput):
    def __init__(self, name, node, library):
        super().__init__(name, node)
        self.library = library
        self.library.on_update(self._on_library_update)
        self.option_dict = {}
        self.preview = None

    def draw(self):
        image_names = self.options()
        with dpg.node_attribute(
            attribute_type=dpg.mvNode_Attr_Output, tag=self.id
        ) as attr:
            self.combo_id = dpg.add_combo(
                image_names, label=self.name, width=200, callback=self._image_selected
            )
            self.preview_container = attr

    def options(self):
        self.option_dict = {}
        for i, img in enumerate(self.library.images):
            key = f"({i}) {img.name}"
            self.option_dict[key] = img
        return [str(k) for k in self.option_dict.keys()]

    def lookup(self, option: str) -> Image:
        return self.option_dict[option]

    def _image_selected(self, caller, app_data):
        image = self.lookup(app_data)
        print(f"Select: {image}")
        if self.preview:
            dpg.delete_item(self.preview)
        self.preview = image.add_to_parent(self.preview_container, width=200)
        self.set_value(image.array)

    def _on_library_update(self):
        image_names = self.options()
        dpg.configure_item(self.combo_id, items=image_names)
