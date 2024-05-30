from unittest.mock import MagicMock
from lenscraft.node.editor import Graph
import lenscraft.node.nodes


def test_load_graph():
    context = MagicMock()
    graph = Graph()
    assert len(graph.nodes) == 0

    graph.load(
        {
            "nodes": [
                {
                    "id": 38,
                    "type": "ImageLibraryNode",
                    "values": {},
                    "position": {"x": 0, "y": 0},
                },
                {
                    "id": 73,
                    "type": "CannyNode",
                    "values": {"Threshold1": 162, "Threshold2": 200},
                    "position": {"x": 327, "y": 123},
                },
                {
                    "id": 83,
                    "type": "TemplateNode",
                    "values": {},
                    "position": {"x": 718, "y": 168},
                },
            ],
            "links": [
                {
                    "id": 90,
                    "output": {
                        "nodeId": 38,
                        "attributeId": 39,
                        "attributeName": "Image",
                    },
                    "input": {
                        "nodeId": 73,
                        "attributeId": 78,
                        "attributeName": "Image",
                    },
                },
                {
                    "id": 91,
                    "output": {
                        "nodeId": 73,
                        "attributeId": 81,
                        "attributeName": "Result",
                    },
                    "input": {
                        "nodeId": 83,
                        "attributeId": 86,
                        "attributeName": "Image",
                    },
                },
            ],
        },
        context,
    )

    assert len(graph.nodes) == 3
