import json
import os
from .step00_utils import setup_logger

logger = setup_logger(__name__)

class InventoryManager:
    def __init__(self, json_path):
        self.json_path = json_path
        self.inventory = []
        self._load()

    def _load(self):
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    self.inventory = json.load(f)
            except json.JSONDecodeError:
                logger.error(f"Failed to decode JSON at {self.json_path}. Starting with empty inventory.")
                self.inventory = []
        else:
            self.inventory = []
            self._save()

    def _save(self):
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.inventory, f, indent=4, ensure_ascii=False)

    def add_item(self, topic):
        new_id = len(self.inventory) + 1
        item = {
            "id": new_id,
            "topic": topic,
            "status": "PENDING",
            "script_path": "",
            "image_paths": [],
            "audio_path": "",
            "subtitle_path": "",
            "output_path": "",
            "metadata_path": ""
        }
        self.inventory.append(item)
        self._save()
        logger.info(f"Added new item: {topic} (ID: {new_id})")
        return item

    def get_item(self, item_id):
        for item in self.inventory:
            if item["id"] == item_id:
                return item
        return None

    def update_status(self, item_id, status):
        item = self.get_item(item_id)
        if item:
            item["status"] = status
            self._save()
            logger.info(f"Updated status for ID {item_id} to {status}")
            return True
        return False

    def update_paths(self, item_id, **kwargs):
        item = self.get_item(item_id)
        if item:
            for key, value in kwargs.items():
                if key in item:
                    item[key] = value
            self._save()
            return True
        return False
