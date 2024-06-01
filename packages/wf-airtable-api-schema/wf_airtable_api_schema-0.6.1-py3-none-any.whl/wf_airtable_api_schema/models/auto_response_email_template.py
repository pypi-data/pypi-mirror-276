from typing import Optional, Union

from pydantic import RootModel

from .base_model import BaseModel
from . import response as response_models

MODEL_TYPE = "auto_response_email_template"


class APIAutoResponseEmailTemplateFields(BaseModel):
    # area_contacts: Optional[list[str]] = None
    geographic_areas: Optional[list[str]] = None
    sendgrid_template_id: Optional[str] = None
    contact_type: Optional[str] = None
    language: Optional[str] = None
    first_contact_email: Optional[str] = None
    # area_name: Optional[str] = None
    # area_type: Optional[str] = None
    # city_radius: Optional[int] = 20
    # polygon_coordinates: Optional[str] = None
    # hub_name: Optional[str] = None
    # latitude: Optional[float] = None
    # longitude: Optional[float] = None
    # geocode: Optional[dict] = None


class APIAutoResponseEmailTemplateRelationships(BaseModel):
    hub: Optional[response_models.APILinksAndData] = None
    assigned_rse: Optional[response_models.APILinksAndData] = None
    geographic_areas: Optional[response_models.APILinksAndData] = None


class APIAutoResponseEmailTemplateData(response_models.APIData):
    fields: APIAutoResponseEmailTemplateFields


class ListAPIAutoResponseEmailTemplateData(RootModel):
    root: list[APIAutoResponseEmailTemplateData]


class APIAutoResponseEmailTemplateResponse(response_models.APIResponse):
    data: APIAutoResponseEmailTemplateData


class ListAPIAutoResponseEmailTemplateResponse(response_models.ListAPIResponse):
    data: list[Union[APIAutoResponseEmailTemplateResponse, dict]]
