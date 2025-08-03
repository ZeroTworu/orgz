from typing import Optional

from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader

from app.settings import ORGZ_API_KEY


class OrgzXAuth(APIKeyHeader):

    @staticmethod
    def check_api_key(api_key: Optional[str], auto_error: bool) -> Optional[str]:  # noqa: WPS602
        if api_key != ORGZ_API_KEY:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

