# django-adx


This module enable creating aggregated data on multiple dimensions (CUBE)

It was initially build as part of openimis-be-dhis2_etl_py made by Damian Borowiecki @dborowiecki (models) and Kamil Malinowski @Malinowskikam (dev) and Patrick Delcroix (desing)

it was design to send data to a DataSet of a DHIS2 server there for there is also some integration function with DHIS2 included but ADX cubes could be serialized to other format or converted to other object or database table rows

## links:

PYPI: https://pypi.org/project/django-adx

GITHUB: https://github.com/delcroip/django-adx


## concepts


To create cubes that can later be serialized using the ADX format some steps are required

ADX cubes have 3 mandatory dimensions : WHAT (data_value), WHEN and WHERE (org_unit); but more dimension can be added to them, it requires the utilization of category (Very similar of how DHIS2 data element works); here are the step to create 

- creating slices/options including a filter 
- creating Category with their slices defined before

the ADX format use the CODE extensively therefore the WHEN, WHERE, WHAT, CATEGORY and CATEGORY OPTIONS need to have a code
sometime the code need to be resolved that why there is a `to_org_unit_code_func` that can generate the code from the object acting as the org_unit. 

the code can only be alpha numeric, all other char will be replaced by "_"

## how it works


the ADX structure (simplified) is :

adx:
    period
    list_adx_group:
        list_data_values:
            list_categories:
                list_options:

the data generation is done with a period and a list of org_unit.

- on the adx level `to_org_unit_code_func` will generate the org_unit code
- on the data_value level:
    - `dataset_from_orgunit_func` will get the data_value object quesryset from the org_unit
    - `period_filter_func` should return a Q object to filter the period on data_value object quesryset
    - `aggregation_func` will be used in the annotate can be Sum, Count etc
- on the category_option level:
    - `filter` should return a Q object to filter the slice on data_value object queryset

The groups don't have any other goal than grouping data_values

Will be added to the "WHAT" django Query after the filter defined to the "WHEN" and "WHERE"


## **ADX Formatting** 

ADX Formatters allow transforming ADXMapping objects to diffrent formats. 
At the moment only XML Format is implemented.


## Examples

### category


example of a method that return a category definition including the slices, this method has a parameter `prefix` so it can be used on object where the gender found  in found through another object e.g `insuree__gender__code`,  then the prefix would be `insuree__`

```python
from django_adx.models.adx import (
    ADXMappingCategoryDefinition,
    ADXCategoryOptionDefinition
)


def get_sex_categories(prefix='') -> ADXMappingCategoryDefinition:
    return ADXMappingCategoryDefinition(
        category_name="sex",
        category_options=[
            ADXCategoryOptionDefinition(
                code="M", name= "MALE", filter= q_with_prefix( 'gender__code', 'M', prefix)),
            ADXCategoryOptionDefinition(
                code="F", name= "FEMALE", filter=q_with_prefix( 'gender__code', 'F', prefix)),
            ADXCategoryOptionDefinition(
                code="O", name= "OTHER", is_default = True)
        ]
    )

```

The `is_default` attribute prevent adding a filter but it also prevent having data that are not covers by any options

The category name is also used for the CODE


### ADX Data definition


```python
from django_adx.models.adx import (
    ADXMappingDefinition,
    ADXMappingGroupDefinition,
    ADXMappingDataValueDefinition,
    ADXMappingCategoryDefinition,
    ADXCategoryOptionDefinition
)


ADXMappingDefinition(
    period_type=ISOFormatPeriodType(), # Format of handled period type, at the moment only ISO Format is supported 
    to_org_unit_code_func= lambda l: build_dhis2_id(l.uuid),
    groups=[
        ADXMappingGroupDefinition(
            comment=str, # Generic comment 
            name=str, # Name of ADX Mapping Definition 
            data_values=[
                ADXMappingDataValueDefinition(
                    data_element=str, # Name of calculated value 
                    period_filter_func =  function # function expection an queryset to filter and a period as input and should return a queryset
                    dataset_from_orgunit_func=function # Function extracting collection from group orgunit object
                    aggregation_func=function # Function transforming filtered queryset to dataset value 
                    categories=[
                        ADXMappingCategoryDefinition(
                            category_name=str,
                            category_options=[
                                ADXCategoryOptionDefinition(
                                    code=code,
                                    name=name,
                                    filter=function # Django Q filter to gather the data of that stratifier `dataset_from_orgunit_func`
                                )
    ])])])])
```
#### Example definition: [HF Number of insurees](django_adx/tests/adx_tests.py)


### ADX Data generation


```python
from django_adx.builders import ADXBuilder
from django_adx.models.adx.definition import ADXMappingGroupDefinition


definition = ADXMappingGroupDefinition(...)
builder = ADXBuilder(definition)
period_type = "2019-01-01/P2Y"  # In format accepted by definition.period_type
org_units = HealthFaciltity.objects.filter(validity_to__isnull=True)  # All HF
builder.create_adx_cube(period_type, org_units)  # Returns ADXMapping object
```

### ADX Formatters


```python
from django_adx.converters.adx.formatters import XMLFormatter
from django_adx.models.adx.data import ADXMapping


adx_format = ADXMapping(...)
xml_formatter = XMLFormatter()
xml_format = xml_formatter.format_adx(adx_format)
```

