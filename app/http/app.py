from fastapi import Depends, FastAPI

from app.http.api.activity import activity_router
from app.http.api.building import building_router
from app.http.api.infra import infra_router
from app.http.api.organization import organizations_router
from app.http.api_key import OrgzXAuth
from app.http.lifespan import LifespanContext
from app.settings import ORGZ_API_KEY_HEADER_NAME

orgz_x_auth = OrgzXAuth(name=ORGZ_API_KEY_HEADER_NAME)

app = FastAPI(title='Organizations Zero Two', lifespan=LifespanContext(), dependencies=[Depends(orgz_x_auth)])

app.include_router(organizations_router)

app.include_router(activity_router)

app.include_router(building_router)

app.include_router(infra_router)
