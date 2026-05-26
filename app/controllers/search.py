from starlette import status

import app.model.user_account as user_account_model
import app.type.queryRecord as query_record_type
import app.type.search as search_type
from app.controllers import query_record as query_record_controller
from app.services.llm_client import LlmError
from app.services.search_tools import run_tool_phase, synthesize_answer
from app.type.queryRecord import QueryType
from app.type.response import ApiResponse


def naturalLanguageSearch(body: search_type.NaturalSearchBody) -> ApiResponse:
    if user_account_model.getUserAccountByID(body.user_id) is None:
        return ApiResponse(
            success=False,
            code=status.HTTP_404_NOT_FOUND,
            message="User not found",
            data=None,
        )

    try:
        raw_results = run_tool_phase(body.query)
        answer = synthesize_answer(body.query, raw_results)
    except LlmError as exc:
        return ApiResponse(
            success=False,
            code=status.HTTP_502_BAD_GATEWAY,
            message=str(exc),
            data=None,
        )
    except Exception as exc:
        return ApiResponse(
            success=False,
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Search failed: {exc}",
            data=None,
        )

    record_resp = query_record_controller.uploadQueryRecord(
        query_record_type.CreateQueryRecordBody(
            user_id=body.user_id,
            query_type=QueryType.natural_language,
            query_text=body.query,
            answer=answer,
        )
    )
    if not record_resp.success or record_resp.data is None:
        return ApiResponse(
            success=False,
            code=record_resp.code,
            message=record_resp.message or "Failed to save query record",
            data=None,
        )

    return ApiResponse(
        success=True,
        code=status.HTTP_200_OK,
        message=None,
        data=search_type.NaturalSearchData(
            answer=answer,
            raw_results=raw_results,
            query_record=record_resp.data,
        ).model_dump(mode="json"),
    )
