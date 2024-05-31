from typing import Dict, List, Union

JSONString = str
JSONNumber = float
JSONBool = bool
JSONNull = type(None)
JSONArray = List["JSONData"]
JSONObject = Dict[str, "JSONData"]

JSONData = Union[JSONString, JSONNumber, JSONBool, JSONNull, JSONArray, JSONObject]
