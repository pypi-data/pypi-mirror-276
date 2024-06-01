# Copyright Patrick Delcoix <patrick@pmpd.eu>
# dhis2 types
from typing import List, Optional
import importlib.metadata
from packaging import version
from pydantic import BaseModel, constr

PYDANTIC_2 = version.parse(importlib.metadata.version('pydantic')) >= version.parse('2.0')


def flex_constr(regex):
    if PYDANTIC_2 :
        return constr(pattern=regex)
    else:
        return constr(regex=regex)
    

#normal uid
uid = flex_constr(regex="^[a-zA-Z][a-zA-Z0-9]{10}$")
# for Dataelement with Categories
uidList = flex_constr(regex="^[a-zA-Z][a-zA-Z0-9]{10}(.[a-zA-Z][a-zA-Z0-9]{10})*$")
# dates
dateStr = flex_constr(regex="^\d{4}-\d{2}-\d{2}$")
datetimeStr = flex_constr(regex="^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$")
# string
str50 = flex_constr(regex="^.{0,50}$")
str130 = flex_constr(regex="^.{0,130}$")
str150 = flex_constr(regex="^.{0,150}$")
str230  = flex_constr(regex="^.{0,230}$")
str255  = flex_constr(regex="^.{0,255}$")
period= flex_constr(regex="^(?:[0-9]{4})|(?:[0-9]{6})|(?:[0-9]{8})$")

class DHIS2Ref(BaseModel):
    id: Optional[uid]
    code: Optional[str]

class DeltaDHIS2Ref(BaseModel):
    additions: List[DHIS2Ref] = []
    deletions: List[DHIS2Ref] = []

class AttributeValue(BaseModel):
    created: Optional[datetimeStr]
    lastUpdated: Optional[datetimeStr]
    attribute: uid
    value: str
    storedBy: Optional[DHIS2Ref]


