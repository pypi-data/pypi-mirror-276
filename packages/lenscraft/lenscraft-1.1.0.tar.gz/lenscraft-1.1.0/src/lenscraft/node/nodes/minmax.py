from importlib import resources
import cv2
import numpy as np

from lenscraft.node import Node, NodeOutput
from lenscraft.node.attributes import ImageNodeInput, IntNodeInput


class MaxPoint(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Min Max"
        self.inputs = [
            ImageNodeInput("Image", self),
            IntNodeInput("OffsetX", self),
            IntNodeInput("OffsetY", self),
        ]
        self.outputs = [
            NodeOutput("MaxPoint", self),
            NodeOutput("MinPoint", self),
            NodeOutput("MaxVal", self),
            NodeOutput("MinVal", self),
        ]

    def compute(self):
        image = self.get_input_value("Image")
        offset_x = self.get_input_value("OffsetX")
        offset_y = self.get_input_value("OffsetY")

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(image)

        max_point = (maxLoc[0] + offset_x, maxLoc[1] + offset_y)
        min_point = (minLoc[0] + offset_x, minLoc[1] + offset_y)

        self.set_output_value("MaxPoint", max_point)
        self.set_output_value("MinPoint", min_point)
        self.set_output_value("MaxVal", maxVal)
        self.set_output_value("MinVal", minVal)
