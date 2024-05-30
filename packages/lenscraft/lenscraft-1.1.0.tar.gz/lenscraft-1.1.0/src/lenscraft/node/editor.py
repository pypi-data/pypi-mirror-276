import logging
from typing import Dict, Tuple
import dearpygui.dearpygui as dpg

from lenscraft.image import ImageLibrary
from lenscraft.texture import TextureModelLibrary
from lenscraft.node import Node, Link, factory, node_options

logger = logging.getLogger(__name__)


class Graph:
    def __init__(self):
        self.nodes: Dict[any, Node] = {}
        self.links: Dict[any, Link] = {}
        self._node_positions = {}

    def add_node(self, node):
        logger.debug(f"Add node {node.name}:{node.id}")
        self.nodes[node.id] = node

    def add_link(self, link: Link):
        self.links[link.id] = link
        link.connect()

    def delink(self, link_id):
        link = self.links.pop(link_id)
        link.disconnect()

    def get_input(self, id):
        for node in self.nodes.values():
            for input in node.inputs:
                if input.id == id:
                    return input

        raise ValueError("No such input")

    def get_output(self, id):
        for node in self.nodes.values():
            for output in node.outputs:
                if output.id == id:
                    return output

        raise ValueError("No such output")

    def node_position(self, node_id) -> Tuple[int, int]:
        if node_id in self._node_positions:
            return self._node_positions[node_id]

        return (0, 0)

    def pause_computation(self, value=True):
        for node in self.nodes.values():
            node.pause = value

    def load(self, data, context):
        self.pause_computation(True)
        for node in data["nodes"]:
            new_node = factory(node["type"], context, node_id=node["id"])
            new_node.pause = True
            new_node.load_values(node["values"])
            self.add_node(new_node)

            if "position" in node:
                self._node_positions[new_node.id] = (
                    node["position"]["x"],
                    node["position"]["y"],
                )

        for link in data["links"]:
            n1 = self.nodes[link["output"]["nodeId"]]
            n2 = self.nodes[link["input"]["nodeId"]]
            a1 = n1.output_attribute_by_name(link["output"]["attributeName"])
            a2 = n2.input_attribute_by_name(link["input"]["attributeName"])

            new_link = Link(a1, a2)
            self.add_link(new_link)
            self.pause_computation(False)

        return self

    def to_json(self):
        data = {"nodes": [], "links": []}
        for node in self.nodes.values():
            node_pos = node.position()
            node_data = {
                "id": node.id,
                "type": type(node).__name__,
                "values": {},
                "position": {"x": node_pos[0], "y": node_pos[1]},
            }
            node_data["values"] = node.values_to_json()

            data["nodes"].append(node_data)

        for link in self.links.values():
            data["links"].append(
                {
                    "output": {
                        "nodeId": link.output.parent_node.id,
                        "attributeName": link.output.name,
                    },
                    "input": {
                        "nodeId": link.input.parent_node.id,
                        "attributeName": link.input.name,
                    },
                }
            )

        return data


class NodeEditor:
    def __init__(self, library: ImageLibrary, texture_library: TextureModelLibrary):
        self.library = library
        self.texture_library = texture_library
        self.id = "node_editor"
        self.graph = None

    def clear(self):
        self.graph = None
        dpg.delete_item(self.id, children_only=True)

    def set_graph(self, graph: Graph):
        self.clear()
        self.graph = graph

        for node_id, node in graph.nodes.items():
            pos = graph.node_position(node_id)
            node.add_to_editor(self.id, pos=pos)

        for link_id, link in graph.links.items():
            dpg.add_node_link(
                link.output.id, link.input.id, parent=self.id, tag=link_id
            )

    def add_to_context(self):
        with dpg.node_editor(
            callback=self.on_link,
            delink_callback=self.on_delink,
            minimap=True,
            minimap_location=dpg.mvNodeMiniMap_Location_BottomRight,
            tag=self.id,
        ):
            pass

        with dpg.window(
            label="Add Node",
            tag="popup_window",
            no_move=True,
            no_close=True,
            no_resize=True,
            no_collapse=True,
            show=False,
            width=200,
        ):
            options = list(node_options().keys())
            for option in options:
                dpg.add_button(
                    label=option,
                    width=-1,
                    callback=self._node_select_callback,
                    user_data=option,
                )

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self._click_callback)
            dpg.add_mouse_release_handler(callback=self._click_up_callback)

    def on_link(self, sender, app_data):
        print(f"link ", app_data)
        a1 = self.graph.get_output(dpg.get_item_alias(app_data[0]))
        a2 = self.graph.get_input(dpg.get_item_alias(app_data[1]))

        new_link = Link(a1, a2)
        print(f"Link {a1.name} to {a2.name}")

        dpg.add_node_link(app_data[0], app_data[1], parent=sender, tag=new_link.id)
        self.graph.add_link(new_link)

    def on_delink(self, sender, app_data):
        print(f"Delink {app_data}")
        self.graph.delink(dpg.get_item_alias(app_data))
        dpg.delete_item(app_data)

    def _node_select_callback(self, sender, app_data, user_data):
        # user_data is the name of the node type
        # Create new instance using the factory method
        new_node = factory(user_data, self)
        new_node.add_to_editor(parent=self.id, pos=self.add_pos)
        self.graph.add_node(new_node)
        dpg.hide_item("popup_window")

    def _click_up_callback(self, sender, app_data):
        if not dpg.is_item_hovered("popup_window"):
            dpg.hide_item("popup_window")

    def _click_callback(self, sender, app_data):
        if app_data == 1:
            self.add_pos = dpg.get_mouse_pos(local=True)
            if dpg.is_item_hovered(self.id):
                dpg.focus_item("popup_window")
                dpg.show_item("popup_window")
                dpg.set_item_pos("popup_window", dpg.get_mouse_pos(local=False))
