import os
from typing import List
import logging
import glob


class TextureModelLibrary:
    def __init__(self):
        self.models: List[str] = []
        self._on_update_callbacks = []

    def find_models_in_directory(self, path):
        model_files = glob.glob("*.keras", root_dir=path)
        for file in model_files:
            self.models.append(os.path.join(path, file))
        self._trigger_on_update()

    def add_model(self, path):
        self.models.append(path)
        self._trigger_on_update()

    def on_update(self, callback):
        """Register callback that will be called if the list of images changes"""
        self._on_update_callbacks.append(callback)

    def _trigger_on_update(self):
        for callback in self._on_update_callbacks:
            try:
                callback()
            except Exception as ex:
                logging.warning(ex)
