import hashlib
import json
from typing import Any
from fastapi import HTTPException, status


class RedisKeyGenerator:
    """
    вообще лучше использовать yaml вместо джейсона но пока пусть будет так
    """
    @staticmethod
    def generate_key(
        repo_name: str, method_name: str, query_data: dict[str, Any]
    ) -> str:
        if not repo_name or not method_name:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Название репозитория и метода не должны быть пустыми.",
            )

        if not isinstance(query_data, dict):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Данные запроса должны быть словарем.",
            )

        try:
            key_base = (
                f"{repo_name}:{method_name}:{json.dumps(query_data, sort_keys=True)}"
            )
        except (TypeError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"ошибка: {e}",
            )

        return hashlib.sha256(key_base.encode("utf-8")).hexdigest()
