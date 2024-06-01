from typing import Optional, Union

from .base_model import BaseModel


class APILinks(BaseModel):
    links: Optional[dict[str, Optional[str]]] = None


class APIDataBase(BaseModel):
    id: str
    type: str


class APIDataWithFields(BaseModel):
    id: str
    type: str
    fields: dict


class APILinksAndData(APILinks):
    data: Optional[Union[str, APIDataWithFields, APIDataBase, list[Union[str, APIDataWithFields, APIDataBase]]]] = None


class APIData(APIDataWithFields):
    fields: dict
    relationships: dict[str, Optional[Union[APILinksAndData, APILinks, list[Union[APILinksAndData, APILinks]]]]]
    links: dict[str, Optional[str]]


class APIResponse(APILinks):
    data: APIData
    meta: Optional[dict] = None


class ListAPIResponse(APIResponse):
    data: list[Union[APIData, dict]]
