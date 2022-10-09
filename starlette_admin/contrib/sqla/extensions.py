from typing import Any, Dict, Type

from pydantic import ValidationError
from sqlmodel import SQLModel
from starlette.requests import Request
from starlette_admin import FileField
from starlette_admin.contrib.sqla.view import ModelView
from starlette_admin.fields import RelationField
from starlette_admin.helpers import pydantic_error_to_form_validation_errors


class SQLModelView(ModelView):
    model: Type[SQLModel]

    async def validate(self, request: Request, data: Dict[str, Any]) -> None:
        """Validate data without relation and file fields"""
        fields_to_exclude = [
            f.name for f in self.fields if isinstance(f, (RelationField, FileField))
        ]
        self.model.validate(
            {k: v for k, v in data.items() if k not in fields_to_exclude}
        )

    def handle_exception(self, exc: Exception) -> None:
        if isinstance(exc, ValidationError):
            raise pydantic_error_to_form_validation_errors(exc)
        return super().handle_exception(exc)  # pragma: no cover
