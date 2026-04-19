from pydantic import BaseModel, model_validator, Field
from typing import ClassVar, Iterable, Any

class CallbackDataRequest(BaseModel):
    name: str = Field() # max_length = 15
    step: int | None = Field(ge=0, lt=100, serialization_alias="s", default=0) # max_length = 2
    page: int | None = Field(ge=0, lt=100, serialization_alias="p", default=0) # max_length = 2
    origin: str | None = Field(serialization_alias="o", default="") # max_length = 15
    index: int | None = Field(gt=-100, lt=100, serialization_alias="i", default=0) # max_length = 3
    message_id: int = Field(ge=0, lt=100_000_000_000_000, serialization_alias="m") # max_length = 15
    
    page_size: ClassVar[int] = 5
        
    aliases: ClassVar[dict[str, str]] = {
        "s": "step",
        "p": "page",
        "o": "origin",
        "i": "index",
        "m": "message_id",
    }
    
    @property
    def start(self) -> int:
        if self.page is None:
            return 0
        return self.page * self.page_size
    
    @property
    def end(self) -> int:
        if self.page is None:
            return self.page_size
        return self.start + self.page_size
    
    @property
    def paginate(self) -> Iterable:
        return range(self.start, self.end)

    def encode(
        self,
        step: int | None = None,
        page: int | None = None,
        origin: str | None = None,
        index: int | None = None,
    ) -> str:

        to_update = {
            "step": step,
            "page": page,
            "origin": origin,
            "index": index,
            "message_id": self.message_id,
        }
        
        copy = self.model_copy(update=to_update)
        pairs = copy.model_dump(
            exclude_none=True,
            exclude_unset=True,
            by_alias=True,
            exclude={"name"},
        )
        
        to_encode = self.name
        
        for key, value in pairs.items():
            to_encode += f"{key}:{value}"
                
        return to_encode.strip()