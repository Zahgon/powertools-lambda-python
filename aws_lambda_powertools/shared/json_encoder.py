import decimal
import json
import math

from aws_lambda_powertools.shared.functions import dataclass_to_dict, is_dataclass, is_pydantic, pydantic_to_dict


class Encoder(json.JSONEncoder):
    """Custom JSON encoder to allow for serialization of Decimals, Pydantic and Dataclasses.

    It's similar to the serializer used by Lambda internally.
    """

    def default(self, obj):
        pass
