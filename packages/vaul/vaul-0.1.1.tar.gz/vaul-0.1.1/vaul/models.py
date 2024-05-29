from __future__ import annotations

from .helpers import remove_keys_recursively
from .enums import RequestMethod

from pydantic import BaseModel, Extra, validate_arguments, create_model, ValidationError
from typing import Callable, Any, Dict, get_type_hints


class BaseAction(BaseModel):
    class Config:
        extra = Extra.allow


class Action:
    def __init__(self, func: Callable, path: str, method: RequestMethod):
        self.func = func
        self.validate_func = validate_arguments(func)
        self.method = method
        self.path = self._normalize_path(path, func.__name__)
        self.openapi_schema = self._generate_openapi_schema()

    @staticmethod
    def _normalize_path(path: str, func_name: str) -> str:
        return path if path != '/' else f'/{func_name.strip("/").replace("/", "_").replace(" ", "_")}'

    def _generate_openapi_schema(self) -> Dict[str, Any]:
        model_fields = {k: (v, ...) for k, v in get_type_hints(self.func).items() if k != 'return'}
        if model_fields:
            DynamicModel = create_model('DynamicModel', **model_fields)
            input_schema = self._clean_schema(DynamicModel.schema())
        else:
            input_schema = {}

        response_schema = self._create_output_schema()
        operation = {
            "operationId": self.func.__name__,
            "summary": (self.func.__doc__ or f"API generated for {self.func.__name__}").strip(),
            "responses": {
                "200": {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {"schema": response_schema}
                    }
                }
            }
        }

        if model_fields:
            operation["requestBody"] = {
                "required": True,
                "content": {
                    "application/json": {"schema": input_schema}
                }
            }

        return {
            self.path: {
                self.method.lower(): operation
            }
        }

    def _clean_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        relevant_properties = {
            k: v for k, v in schema["properties"].items() if k not in {"v__duplicate_kwargs", "args", "kwargs"}
        }
        schema["properties"] = relevant_properties
        schema["required"] = sorted(k for k, v in relevant_properties.items() if "default" not in v)
        schema = remove_keys_recursively(schema, "additionalProperties")
        schema = remove_keys_recursively(schema, "title")
        return schema

    def _create_output_schema(self) -> Dict[str, Any]:
        return_type = get_type_hints(self.func).get('return', Any)
        if return_type and issubclass(return_type, BaseModel):
            return return_type.schema()
        temp_model = create_model('TempModel', result=(return_type, ...))
        return temp_model.schema()["properties"]["result"]

    def run(self, arguments=None):
        if arguments is None:
            arguments = {}
        try:
            return self.validate_func(**arguments)
        except (ValidationError, TypeError) as e:
            raise ValueError(f"Invalid request body: {str(e)}")
