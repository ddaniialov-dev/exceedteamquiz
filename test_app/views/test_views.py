from fastapi import Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from user_app.crud import UserManager

from user_app.models import User

from quiz_project.database import get_session

from test_app.crud import TestManager
from test_app.schemas import GetTest, CreateTest, UpdateTest
from test_app.checks.common import check_if_holder, check_if_exists

test_router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)


@test_router.get("/", status_code=200, response_model=list[GetTest])
async def get_user_tests(
    request: Request,
    database_session: AsyncSession = Depends(get_session)
) -> list[GetTest]:
    async with TestManager(database_session) as manager:
        tests = await manager.get_user_tests(request.user.id)
    return tests


@test_router.get("/all/", status_code=200, response_model=list[GetTest])
async def get_all_tests(
    database_session: AsyncSession = Depends(get_session),
) -> list[GetTest]:
    async with TestManager(database_session) as manager:
        tests = await manager.get_tests()
        return tests


@test_router.post("/", status_code=201, response_model=GetTest)
async def create_test(
    test: CreateTest,
    request: Request,
    database_session: AsyncSession = Depends(get_session),
) -> GetTest:
    if not request.user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You need to be an administrator to create tests!",
        )
    async with TestManager(database_session) as manager:
        test.holder_id = request.user.id
        result = await manager.create_test(test)
        if not result:
            raise HTTPException(status_code=400, detail="Test wat not created")
        return result


@test_router.get("/{test_id}/", response_model=GetTest, status_code=200)
async def get_test(test_id: int, database_session: AsyncSession = Depends(get_session)):
    async with TestManager(database_session) as manager:
        test = await manager.get_test(test_id)
        await check_if_exists(test)
        return test


@test_router.put("/{test_id}/", response_model=UpdateTest, status_code=200)
async def update_test(
    test_id: int,
    test: UpdateTest,
    request: Request,
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as manager:
        test_object = await get_test(test_id, database_session)
        await check_if_holder(request.user.id, test_object.holder_id)
        test = await manager.update_test(
            test_id, test.dict(exclude={"holder_id"}, exclude_unset=True)
        )
        return test


@test_router.delete(
    "/{test_id}/",
    status_code=204,
)
async def delete_test(
    test_id: int,
    request: Request,
    database_session: AsyncSession = Depends(get_session)
) -> Response:
    async with TestManager(database_session) as manager:
        test_object = await get_test(test_id, database_session)
        await check_if_holder(request.user.id, test_object.holder_id)
        await manager.delete_test(request.user, test_id)
        return Response(status_code=204)
