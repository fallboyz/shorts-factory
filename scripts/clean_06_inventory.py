import os
import json

def clean():
    print("Resetting Inventory...")
    inventory_path = 'data/inventory.json'
    if os.path.exists(inventory_path):
        try:
            with open(inventory_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            print(f"Inventory reset: {inventory_path}")
        except Exception as e:
            print(f"Error resetting inventory: {e}")

if __name__ == '__main__':
    clean()
