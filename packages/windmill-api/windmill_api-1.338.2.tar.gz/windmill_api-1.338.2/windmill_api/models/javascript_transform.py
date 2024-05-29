from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.javascript_transform_type import JavascriptTransformType

T = TypeVar("T", bound="JavascriptTransform")


@_attrs_define
class JavascriptTransform:
    """
    Attributes:
        expr (str):
        type (JavascriptTransformType):
    """

    expr: str
    type: JavascriptTransformType
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expr = self.expr
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        type = JavascriptTransformType(d.pop("type"))

        javascript_transform = cls(
            expr=expr,
            type=type,
        )

        javascript_transform.additional_properties = d
        return javascript_transform

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
