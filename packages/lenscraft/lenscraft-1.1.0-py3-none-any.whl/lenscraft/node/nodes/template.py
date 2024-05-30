from importlib import resources
import cv2
import numpy as np

from lenscraft.node import Node
from lenscraft.node.attributes import (
    ImageNodeInput,
    ImageNodeOutput,
)


class TemplateNode(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Template Match"
        self.inputs = [ImageNodeInput("Image", self)]
        self.outputs = [ImageNodeOutput("Result", self)]
        with resources.path("lenscraft.assets", "CornerTemplate.png") as img_path:
            print("Find template", img_path)
            self.template = cv2.imread(str(img_path))

    def compute(self):
        image = self.get_input_value("Image")

        result = cv2.matchTemplate(image, self.template, cv2.TM_CCOEFF)
        normalized_result = (result - np.min(result)) / (
            np.max(result) - np.min(result)
        )
        result = (normalized_result * 255).astype(np.uint8)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

        self.set_output_value("Result", result)
