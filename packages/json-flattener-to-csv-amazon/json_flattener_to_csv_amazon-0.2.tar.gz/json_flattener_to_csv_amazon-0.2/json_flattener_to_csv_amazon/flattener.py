import pandas as pd
import json 

class Flattener:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def flatten_json(self, json_data):
        try:
            return pd.json_normalize(json_data)
        except Exception as e:
            print(f"An error occurred during JSON flattening: {e}")
            return None

flattener_instance = Flattener()
