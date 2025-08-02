from fastapi import Header, HTTPException, status

from app.settings import ORGZ_API_KEY


async def verify_api_key(x_api_key: str = Header(..., alias='X-ORGZ-Key')):  # noqa: WPS404
    if x_api_key != ORGZ_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API Key',
        )
