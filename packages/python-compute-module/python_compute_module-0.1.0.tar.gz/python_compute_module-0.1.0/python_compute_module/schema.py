import inspect
from typing import Any, Callable, List, Optional, Union

from pydantic import BaseModel


class PrimitiveType(BaseModel):
    type: str = "primitiveType"
    primitiveType: str  # "BOOL" | "INT" | "FLOAT" | "STRING"


class UnknownType(BaseModel):
    type: str = "unknownType"
    unknownType: dict = {}


class Entry(BaseModel):
    name: str
    type: Union[PrimitiveType, "ComplexType", UnknownType]  # DataType


class StructType(BaseModel):
    type: str = "structType"
    structType: dict = {"fields": List[Entry]}


class ListType(BaseModel):
    type: str = "listType"
    elementType: Union[PrimitiveType, "ComplexType", UnknownType]  # DataType


class ComplexType(BaseModel):
    type: str = "complexType"
    complexType: Union[StructType, ListType]


Entry.update_forward_refs()  # Update DataType in Entry


class Schema(BaseModel):
    name: str
    inputType: StructType
    outputType: Union[PrimitiveType, ComplexType, UnknownType]  # DataType


def generate_schema(func: Callable[..., Any], name: Optional[str] = None) -> Schema:
    name = name or func.__name__
    signature = inspect.signature(func)

    input_fields = []
    for param_name, param in signature.parameters.items():
        if param.annotation is not inspect.Parameter.empty:
            input_fields.append(
                Entry(
                    name=param_name,
                    type=PrimitiveType(primitiveType=param.annotation.__name__),
                )
            )

    if signature.return_annotation is not inspect.Signature.empty:
        output_type = PrimitiveType(primitiveType=signature.return_annotation.__name__)
    else:
        output_type = UnknownType()

    input_type = StructType(structType={"fields": input_fields})

    return Schema(name=name, inputType=input_type, outputType=output_type)
