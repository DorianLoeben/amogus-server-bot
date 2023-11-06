import json
import os


def get_data_for_guild(guild_id: int):
    # get the data from ../data/{guild_id}.json if it exists
    # else return None
    path = f"data/{guild_id}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(f"data/{guild_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"guild_id": guild_id}


def get_field_from_guild(guild_id: int, field: str, default=None):
    data = get_data_for_guild(guild_id)
    if field in data:
        return data[field]
    else:
        return default


def set_field_for_guild(guild_id: int, field: str, value):
    data = get_data_for_guild(guild_id)
    data[field] = value
    with open(f"data/{guild_id}.json", "w") as f:
        json.dump(data, f)
