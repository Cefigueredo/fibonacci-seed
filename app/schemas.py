from datetime import datetime as dt

import pydantic


class Input(pydantic.BaseModel):
    datetime: dt | None = None

    model_config = {
        "json_schema_extra": {"examples": [{"datetime": dt.now().isoformat()}]}
    }


class Output(pydantic.BaseModel):
    id: int
    datetime: str
    fibonacci: str
