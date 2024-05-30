import cv2

from lenscraft.node import Node
from lenscraft.node.attributes import (
    ImageNodeOutput,
    ImageNodeInput,
    NumberSliderAttribute,
)
from lenscraft.utils import debounce


class ThresholdNode(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Threshold"
        self.inputs = [
            ImageNodeInput("Image", self),
            NumberSliderAttribute("Threshold", self, 255, 0, 128),
            NumberSliderAttribute("Max", self, 255, 0, 255),
        ]
        self.outputs = [ImageNodeOutput("Result", self)]

    @debounce(0.2)
    def compute(self):
        image = self.get_input_value("Image")
        threshold_value = self.get_input_value("Threshold")
        max_value = self.get_input_value("Max")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(
            gray,
            threshold_value,
            max_value,
            cv2.THRESH_BINARY,
        )
        result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        self.set_output_value("Result", result)
