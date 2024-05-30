import cv2

from lenscraft.node import Node, NodeInput
from lenscraft.node.attributes import ImageNodeOutput, ImageNodeInput


class ShowPoint(Node):
    def __init__(self, context, node_id=None):
        super().__init__(node_id)
        self.name = "Show Point"
        self.inputs = [ImageNodeInput("Image", self), NodeInput("Point", self)]
        self.outputs = [ImageNodeOutput("Result", self)]

    def compute(self):
        image = self.get_input_value("Image")
        point = self.get_input_value("Point")

        marked_image = image.copy()
        cv2.circle(marked_image, point, radius=10, color=(255, 0, 0), thickness=-1)
        cv2.imwrite("result.png", marked_image)

        self.set_output_value("Result", marked_image)

