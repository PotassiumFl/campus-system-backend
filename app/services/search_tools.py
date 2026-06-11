from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from app.controllers import building as building_controller
from app.controllers import campus as campus_controller
from app.controllers import course as course_controller
from app.controllers import event as event_controller
from app.controllers import facility as facility_controller
from app.controllers import teach as teach_controller
from app.controllers import teacher as teacher_controller
from app.services.llm_client import chat_completion, chat_with_tools
from app.type import building as building_type
from app.type import campus as campus_type
from app.type import course as course_type
from app.type import event as event_type
from app.type import facility as facility_type
from app.type import teach as teach_type
from app.type import teacher as teacher_type
from app.type.response import ApiResponse

MAX_TOOL_ROUNDS = 5

SYSTEM_PROMPT = """你是校园数据库查询助手。根据用户的自然语言问题，调用合适的查询工具获取数据。

规则：
- search_* 工具使用模糊匹配（LIKE），适合关键词搜索
- filter_* 工具使用精确多值匹配（IN），适合按已知值筛选
- 可以多次调用不同工具，按需组合查询
- 只调用查询工具，不要编造数据
- building_type 可选值：教学楼、宿舍楼、办公楼、实验楼、体育馆、食堂、图书馆、其他
- facility_type 可选值：餐厅、水吧、自习室、办公室、卫生间、教室、寝室、其他
- teach role 可选值：教师、助教
"""

SYNTHESIS_PROMPT = """你是校园数据库查询助手。根据用户问题和已执行的查询结果，用简洁清晰的中文回答用户。
- 直接回答问题，不要提及工具或 API
- 若查询无结果，如实说明
- 适当整理列表，便于阅读
"""

ToolHandler = Callable[[BaseModel], ApiResponse]


def _tool(
    name: str,
    description: str,
    parameters: dict[str, Any],
    handler: ToolHandler,
    body_cls: type[BaseModel],
) -> tuple[dict[str, Any], str, ToolHandler, type[BaseModel]]:
    spec = {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": parameters,
        },
    }
    return spec, name, handler, body_cls


_TOOL_SPECS: list[tuple[dict[str, Any], str, ToolHandler, type[BaseModel]]] = [
    _tool(
        "search_campus",
        "模糊搜索校区，可按名称或地址",
        {
            "type": "object",
            "properties": {
                "campus_name": {"type": "string", "description": "校区名称关键词"},
                "campus_address": {"type": "string", "description": "校区地址关键词"},
            },
        },
        campus_controller.searchCampus,
        campus_type.SearchCampusBody,
    ),
    _tool(
        "filter_campus",
        "精确筛选校区，名称或地址为多值 IN 匹配",
        {
            "type": "object",
            "properties": {
                "campus_name": {"type": "array", "items": {"type": "string"}},
                "campus_address": {"type": "array", "items": {"type": "string"}},
            },
        },
        campus_controller.filterCampus,
        campus_type.FilterCampusBody,
    ),
    _tool(
        "search_building",
        "模糊搜索建筑，可按校区名或建筑名",
        {
            "type": "object",
            "properties": {
                "campus_name": {"type": "string"},
                "building_name": {"type": "string"},
            },
        },
        building_controller.searchBuilding,
        building_type.SearchBuildingBody,
    ),
    _tool(
        "filter_building",
        "精确筛选建筑",
        {
            "type": "object",
            "properties": {
                "campus_name": {"type": "array", "items": {"type": "string"}},
                "building_name": {"type": "array", "items": {"type": "string"}},
                "building_type": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["教学楼", "宿舍楼", "办公楼", "实验楼", "体育馆", "食堂", "图书馆", "其他"],
                    },
                },
            },
        },
        building_controller.filterBuilding,
        building_type.FilterBuildingBody,
    ),
    _tool(
        "search_facility",
        "模糊搜索设施，可按建筑名或设施名",
        {
            "type": "object",
            "properties": {
                "building_name": {"type": "string"},
                "facility_name": {"type": "string"},
            },
        },
        facility_controller.searchFacility,
        facility_type.SearchFacilityBody,
    ),
    _tool(
        "filter_facility",
        "精确筛选设施",
        {
            "type": "object",
            "properties": {
                "building_name": {"type": "array", "items": {"type": "string"}},
                "facility_name": {"type": "array", "items": {"type": "string"}},
                "facility_type": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["餐厅", "水吧", "自习室", "办公室", "卫生间", "教室", "寝室", "其他"],
                    },
                },
                "open_time": {"type": "array", "items": {"type": "string"}},
            },
        },
        facility_controller.filterFacility,
        facility_type.FilterFacilityBody,
    ),
    _tool(
        "search_course",
        "模糊搜索课程，可按课程名或院系",
        {
            "type": "object",
            "properties": {
                "course_id": {"type": "string"},
                "course_name": {"type": "string"},
                "department": {"type": "string"},
            },
        },
        course_controller.searchCourse,
        course_type.SearchCourseBody,
    ),
    _tool(
        "filter_course",
        "精确筛选课程",
        {
            "type": "object",
            "properties": {
                "course_id": {"type": "array", "items": {"type": "string"}},
                "course_name": {"type": "array", "items": {"type": "string"}},
                "department": {"type": "array", "items": {"type": "string"}},
                "credit": {"type": "array", "items": {"type": "number"}},
            },
        },
        course_controller.filterCourse,
        course_type.FilterCourseBody,
    ),
    _tool(
        "search_event",
        "模糊搜索活动，可按建筑名、活动名或组织者",
        {
            "type": "object",
            "properties": {
                "building_name": {"type": "string"},
                "event_name": {"type": "string"},
                "organizer": {"type": "string"},
            },
        },
        event_controller.searchEvent,
        event_type.SearchEventBody,
    ),
    _tool(
        "filter_event",
        "精确筛选活动",
        {
            "type": "object",
            "properties": {
                "building_name": {"type": "array", "items": {"type": "string"}},
                "event_name": {"type": "array", "items": {"type": "string"}},
                "organizer": {"type": "array", "items": {"type": "string"}},
            },
        },
        event_controller.filterEvent,
        event_type.FilterEventBody,
    ),
    _tool(
        "search_teacher",
        "模糊搜索教师，可按姓名、院系或邮箱",
        {
            "type": "object",
            "properties": {
                "teacher_name": {"type": "string"},
                "department": {"type": "string"},
                "email": {"type": "string"},
            },
        },
        teacher_controller.searchTeacher,
        teacher_type.SearchTeacherBody,
    ),
    _tool(
        "filter_teacher",
        "精确筛选教师",
        {
            "type": "object",
            "properties": {
                "teacher_name": {"type": "array", "items": {"type": "string"}},
                "department": {"type": "array", "items": {"type": "string"}},
                "email": {"type": "array", "items": {"type": "string"}},
            },
        },
        teacher_controller.filterTeacher,
        teacher_type.FilterTeacherBody,
    ),
    _tool(
        "search_teach",
        "模糊搜索授课记录，可按教师姓名、课程名、课程号、学期或教学班",
        {
            "type": "object",
            "properties": {
                "teacher_name": {"type": "string"},
                "course_name": {"type": "string"},
                "course_id": {"type": "string"},
                "semester": {"type": "string"},
                "section_no": {"type": "string"},
            },
        },
        teach_controller.searchTeach,
        teach_type.SearchTeachBody,
    ),
    _tool(
        "filter_teach",
        "精确筛选授课记录，可按教师姓名、课程名、学期",
        {
            "type": "object",
            "properties": {
                "teacher_name": {"type": "string"},
                "course_name": {"type": "string"},
                "semester": {"type": "string"},
            },
        },
        teach_controller.filterTeach,
        teach_type.FilterTeachBody,
    ),
]

SEARCH_TOOLS: list[dict[str, Any]] = [spec for spec, _, _, _ in _TOOL_SPECS]
_TOOL_BY_NAME: dict[str, tuple[ToolHandler, type[BaseModel]]] = {
    name: (handler, body_cls) for _, name, handler, body_cls in _TOOL_SPECS
}


def execute_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name not in _TOOL_BY_NAME:
        raise ValueError(f"Unknown tool: {name}")
    handler, body_cls = _TOOL_BY_NAME[name]
    body = body_cls.model_validate(args)
    response = handler(body)
    return {
        "tool": name,
        "params": args,
        "response": response.model_dump(mode="json"),
    }


def _message_to_dict(message: Any) -> dict[str, Any]:
    out = message.model_dump(exclude_none=True)
    out["role"] = "assistant"
    keep = ("role", "content", "tool_calls", "reasoning_content")
    return {key: value for key, value in out.items() if key in keep}


def run_tool_phase(query: str) -> list[dict[str, Any]]:
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query},
    ]
    raw_results: list[dict[str, Any]] = []

    for _ in range(MAX_TOOL_ROUNDS):
        message = chat_with_tools(messages, SEARCH_TOOLS)
        if not message.tool_calls:
            break

        messages.append(_message_to_dict(message))
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments or "{}")
            result = execute_tool(tool_call.function.name, args)
            raw_results.append(result)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result["response"], ensure_ascii=False),
                }
            )

    return raw_results


def _fallback_answer(raw_results: list[dict[str, Any]]) -> str:
    if not raw_results:
        return "未能查询到相关数据。"
    parts: list[str] = []
    for item in raw_results:
        resp = item.get("response") or {}
        data = resp.get("data")
        if data:
            parts.append(f"{item['tool']}: 找到 {len(data) if isinstance(data, list) else 1} 条记录")
        else:
            parts.append(f"{item['tool']}: 无结果")
    return "查询完成。" + "；".join(parts)


def synthesize_answer(query: str, raw_results: list[dict[str, Any]]) -> str:
    if not raw_results:
        return "未能查询到相关数据，请尝试换一种问法。"

    messages = [
        {"role": "system", "content": SYNTHESIS_PROMPT},
        {
            "role": "user",
            "content": (
                f"用户问题：{query}\n\n"
                f"查询结果：\n{json.dumps(raw_results, ensure_ascii=False, default=str)}"
            ),
        },
    ]
    try:
        return chat_completion(messages)
    except Exception:
        return _fallback_answer(raw_results)
