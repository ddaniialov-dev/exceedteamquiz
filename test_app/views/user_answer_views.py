from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Request

from test_app.crud.session_crud import SessionManager
from test_app.crud.user_answer_crud import UserAnswerManager
from test_app.schemas.user_answer_schemas import CreateUserAnswer, GetUserAnswer
from quiz_project.database import get_session
from test_app.checks.common import check_if_exists


user_answer_router = APIRouter(
    prefix="/sessions/{session_id}/user_answers",
    tags=["user_answers"],
)


@user_answer_router.post(
    "/",
    status_code=201,
    response_model=GetUserAnswer,
)
async def create_user_answer(
    session_id: int,
    user_answer: CreateUserAnswer,
    request: Request,
    database_session: AsyncSession = Depends(get_session),
):
    async with SessionManager(database_session) as manager:
        session_object = await manager.get_session(request.user.id, session_id)
        await check_if_exists(session_object)
        if not session_object.questions:
            raise HTTPException(
                status_code=404, detail="No questions for this session")
        async with UserAnswerManager(database_session) as manager:
            user_answer_object = await manager.create_user_answer(
                session_object, user_answer.dict()
            )
            return user_answer_object
