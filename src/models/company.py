from pydantic import BaseModel, Field, constr, conint, conlist, StringConstraints, field_validator, model_serializer
from typing import List, Optional
from typing_extensions import Annotated
from datetime import date


class Address(BaseModel):
    country_id: Annotated[Optional[int], Field(strict=True, gt=0)]
    # is_preferred: Optional[bool]
    title: Annotated[str, StringConstraints(max_length=255,), Field(validate_default=True)] = "Hauptanschrift"
    recipient_1: Annotated[Optional[str], Field(max_length=255, json_schema_extra={
            'title': 'First Line of Recipient',
            'description': 'Usually the name of the recipient. E.g. The Company Name'
        })]
    recipient_2: Annotated[Optional[str], Field(max_length=255)]
    recipient_3: Annotated[Optional[str], Field(max_length=255)]
    street_name: Annotated[Optional[str], Field(max_length=255)]
    street_number: Annotated[Optional[str], Field(max_length=255)]
    street_additional: Annotated[Optional[str], Field(max_length=255)]
    zip: Annotated[Optional[str], Field(max_length=255)]
    location: Annotated[Optional[str], Field(max_length=255)]
    state: Annotated[Optional[str], Field(max_length=255)]
    # pos: Annotated[Optional[int], Field(strict=True)]


class Contact(BaseModel):
    contact_type_id: Annotated[int, Field(strict=True, gt=0, json_schema_extra={
            'title': 'Internal ID',
            'description': 'The internal ID of the contact type. Phone: 1, Mail: 2, Fax: 4, Mobile: 7, Web: 6, Other: 11'
        }, validate_default=True)] = 1
    # is_preferred: Optional[bool]
    title: Annotated[Optional[str], StringConstraints(max_length=255,)]
    value: Annotated[Optional[str], StringConstraints(max_length=255,)]
    # pos: Annotated[Optional[int], Field(strict=True)]


class Tag(BaseModel):
    id: Annotated[int, Field(strict=True, gt=0)]


class Company(BaseModel):
    id: Annotated[Optional[int], Field(strict=True, gt=0)]
    company_group_id: Annotated[Optional[int], Field(strict=True, gt=0)]
    name: Annotated[Optional[str], Field(max_length=255)]
    name_legal: Annotated[Optional[str], Field(max_length=255)]
    name_token: Annotated[Optional[str], Field(min_length=1, max_length=255, pattern=r'^[a-zA-Z0-9]+$', json_schema_extra={
            'title': 'Short Name of Company',
            'description': 'Usually a short name or abbreviation of the company name. E.g. The Company Name -> tcn. Keep it Short with 4 characters.'
        })]
    type: Annotated[str, Field(max_length=255, validate_default=True, pattern=r'^(company|person)$')] = "company"
    uid: Annotated[Optional[str], Field(max_length=255)]
    management: Annotated[Optional[str], Field(max_length=255)]
    jurisdiction: Annotated[Optional[str], Field(max_length=255)]
    commercial_register: Annotated[Optional[str], Field(max_length=255)]
    data_privacy_number: Annotated[Optional[str], Field(max_length=255)]
    # salutation: Annotated[Optional[str], Field(max_length=255)]
    # title: Annotated[Optional[str], Field(max_length=255)]
    # firstname: Annotated[Optional[str], Field(max_length=255)]
    # middlename: Annotated[Optional[str], Field(max_length=255)]
    # lastname: Annotated[Optional[str], Field(max_length=255)]
    # nickname: Annotated[Optional[str], Field(max_length=255)]
    # position: Annotated[Optional[str], Field(max_length=255)]
    # function: Annotated[Optional[str], Field(max_length=255)]
    # department: Annotated[Optional[str], Field(max_length=255)]
    # maiden_name: Annotated[Optional[str], Field(max_length=255)]
    # birthday: Annotated[Optional[date], Field()]
    # gender: Annotated[Optional[str], Field(regex=r'^(m|f)$')]
    addresses: Optional[List[Address]]
    contacts: Optional[List[Contact]]
    tags: Optional[List[Tag]] = []

    @field_validator("type", mode="before")
    def validate_location(cls, value):
        if value == None:
            return cls.model_fields["type"].default
        return value


class Person(BaseModel):
    company_id: Annotated[Optional[int], Field(strict=True, gt=0)]
    company_subsidiary_id: Annotated[Optional[int], Field(strict=True, gt=0)]
    salutation: Annotated[Optional[str], Field(max_length=255)]
    title: Annotated[Optional[str], Field(max_length=255)]
    firstname: Annotated[Optional[str], Field(max_length=255)]
    middlename: Annotated[Optional[str], Field(max_length=255)]
    lastname: Annotated[str, Field(min_length=1, max_length=255)]
    nickname: Annotated[Optional[str], Field(max_length=255)]
    position: Annotated[Optional[str], Field(max_length=255)]
    function: Annotated[Optional[str], Field(max_length=255)]
    department: Annotated[Optional[str], Field(max_length=255)]
    maiden_name: Annotated[Optional[str], Field(max_length=255)]
    birthday: Annotated[Optional[date], Field()]
    gender: Annotated[Optional[str], Field(pattern=r'^(m|f)$')]
    addresses: Optional[List[Address]]
    contacts: Optional[List[Contact]]
    tags: Optional[List[Tag]]
