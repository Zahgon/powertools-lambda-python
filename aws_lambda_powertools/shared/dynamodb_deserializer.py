from __future__ import annotations

from decimal import Clamped, Context, Decimal, Inexact, Overflow, Rounded, Underflow
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

# NOTE: DynamoDB supports up to 38 digits precision
# Therefore, this ensures our Decimal follows what's stored in the table
DYNAMODB_CONTEXT = Context(
    Emin=-128,
    Emax=126,
    prec=38,
    traps=[Clamped, Overflow, Inexact, Rounded, Underflow],
)


class TypeDeserializer:
    """
    Deserializes DynamoDB types to Python types.

    It's based on boto3's [DynamoDB TypeDeserializer](https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/dynamodb/types.html).

    The only notable difference is that for Binary (`B`, `BS`) values we return Python Bytes directly,
    since we don't support Python 2.
    """

    def deserialize(self, value: dict) -> Any:
        """Deserialize DynamoDB data types into Python types.

        Parameters
        ----------
        value: Any
            DynamoDB value to be deserialized to a python type


            Here are the various conversions:

            DynamoDB                                Python
            --------                                ------
            {'NULL': True}                          None
            {'BOOL': True/False}                    True/False
            {'N': Decimal(value)}                   Decimal(value)
            {'S': string}                           string
            {'B': bytes}                            bytes
            {'NS': [str(value)]}                    set([str(value)])
            {'SS': [string]}                        set([string])
            {'BS': [bytes]}                         set([bytes])
            {'L': list}                             list
            {'M': dict}                             dict

        Parameters
        ----------
        value: Any
            DynamoDB value to be deserialized to a python type

        Returns
        --------
        any
            Python native type converted from DynamoDB type
        """

        dynamodb_type = list(value.keys())[0]
        deserializer: Callable | None = getattr(self, f"_deserialize_{dynamodb_type}".lower(), None)
        if deserializer is None:
            raise TypeError(f"Dynamodb type {dynamodb_type} is not supported")

        return deserializer(value[dynamodb_type])

    def _deserialize_null(self, value: bool) -> None:
        pass

    def _deserialize_bool(self, value: bool) -> bool:
        pass

    def _deserialize_n(self, value: str) -> Decimal:
        # value is None or "."? It's zero
        # then return early
        pass

    def _deserialize_s(self, value: str) -> str:
        pass

    def _deserialize_b(self, value: bytes) -> bytes:
        pass

    def _deserialize_ns(self, value: Sequence[str]) -> set[Decimal]:
        pass

    def _deserialize_ss(self, value: Sequence[str]) -> set[str]:
        pass

    def _deserialize_bs(self, value: Sequence[bytes]) -> set[bytes]:
        pass

    def _deserialize_l(self, value: Sequence[dict]) -> Sequence[Any]:
        pass

    def _deserialize_m(self, value: dict) -> dict:
        pass
