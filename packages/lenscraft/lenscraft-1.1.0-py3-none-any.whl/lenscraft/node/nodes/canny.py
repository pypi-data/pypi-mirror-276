import cv2

from lenscraft.node import Node
from lenscraft.node.attributes import (
    ImageNodeInput,
    NumberSliderAttribute,
    ImageNodeOutput,
)


class CannyNode(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Canny"
        self.inputs = [
            ImageNodeInput("Image", self),
            NumberSliderAttribute("Threshold1", self, 255, 0, 100),
            NumberSliderAttribute("Threshold2", self, 255, 0, 200),
        ]
        self.outputs = [ImageNodeOutput("Result", self)]

    def compute(self):
        image = self.get_input_value("Image")
        t1 = self.get_input_value("Threshold1")
        t2 = self.get_input_value("Threshold2")

        result = cv2.Canny(image, t1, t2)
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        self.set_output_value("Result", result)
