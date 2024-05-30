from typing import Dict, List
import dearpygui.dearpygui as dpg

from lenscraft.utils import uid


def node_options():
    types = Node.__subclasses__()
    return {t.__name__: t for t in types}


def factory(node_type: str, editor, **kwargs) -> "Node":
    return node_options()[node_type](editor, **kwargs)


class Link:
    def __init__(self, a1, a2):
        self.output = a1
        self.input = a2
        self.id = uid()

    def disconnect(self):
        self.output.delink(self.input)

    def connect(self):
        self.output.link(self.input)


class Node:
    def __init__(self, node_id=None):
        if node_id is None:
            self.id = uid()
        else:
            self.id = node_id

        self.pause = False

    def compute(self):
        pass

    def draw_config(self):
        pass

    def position(self):
        return dpg.get_item_pos(self.id)

    def add_to_editor(self, parent=0, pos=(0, 0)):
        with dpg.node(label=self.name, parent=parent, pos=pos, tag=self.id):
            self.draw_config()
            for input in self.inputs:
                input.draw()
            for output in self.outputs:
                output.draw()

    def get_input_value(self, name):
        for input in self.inputs:
            if input.name == name:
                return input.value

        raise ValueError(f"No such input: {name}")

    def set_output_value(self, name, value):
        for output in self.outputs:
            if output.name == name:
                output.set_value(value)
                return

        raise ValueError(f"No such output: {name}")

    def input_attribute_by_name(self, name) -> "NodeInput":
        for a in self.inputs:
            if a.name == name:
                return a

        raise ValueError(f"No such input attribute: {name}")

    def output_attribute_by_name(self, name) -> "NodeOutput":
        for a in self.outputs:
            if a.name == name:
                return a

        values = [a.name for a in self.outputs]
        raise ValueError(f"No such output attribute: {name}, only: {values}")

    def values_to_json(self):
        values = {}
        for input in self.inputs:
            value = input.value
            if type(value) in (int, float, str):
                values[input.name] = value

        return values

    def load_values(self, data):
        """State is persisted to json using the `values_to_json` method. This method loads
        the state and applies it back to the node

        Args:
            data (dict): json encoded node values
        """
        for name in data:
            attr = self.input_attribute_by_name(name)
            attr.update_value(data[name])


class NodeInput:
    def __init__(self, name, node: Node):
        self.name = name
        self.id = uid()
        self.value = None
        self.parent_node = node

    def update_value(self, new_value):
        self.value = new_value
        if not self.parent_node.pause:
            self.parent_node.compute()

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Input, tag=self.id):
            dpg.add_text(self.name)


class NodeOutput:
    outputs: Dict[any, "NodeOutput"] = {}

    def __init__(self, name, node: Node):
        self.name = name
        self.id = uid()
        self.downstream: List[NodeInput] = []
        self.value = None
        self.parent_node = node

    def link(self, input: NodeInput):
        self.downstream.append(input)
        if self.value is not None:
            input.update_value(self.value)

    def delink(self, input: NodeInput):
        self.downstream.remove(input)

    def set_value(self, new_value):
        self.value = new_value
        for d in self.downstream:
            d.update_value(new_value)

    def draw(self):
        with dpg.node_attribute(attribute_type=dpg.mvNode_Attr_Output, tag=self.id):
            dpg.add_text(default_value=self.name)
