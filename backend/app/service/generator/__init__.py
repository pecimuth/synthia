from typing import Dict, List, Any

# represents one generated row
# key is column name
# value is the result of make_value or make_preview_value
# should be updated after each call to make_value/make_preview_value
GeneratedRow = Dict[str, Any]

GeneratedTable = List[GeneratedRow]

# holds all generated values in a generation procedure
# key is table name
GeneratedDatabase = Dict[str, GeneratedTable]
