from datetime import datetime

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun

from docmesh_core.db.neo.entity import (
    follow_entity,
    list_follows,
    list_popular_entities,
    list_recent_reading_papers,
)
from docmesh_agent.tools.base import BaseAgentTool, BaseAgentNoInputTool


class FollowEntityToolInput(BaseModel):
    name: str = Field(description="entity name")


class FollowEntityTool(BaseAgentTool):
    name: str = "follow_entity"
    description: str = "uesful when you need to follow an entity"
    args_schema: Optional[Type[BaseModel]] = FollowEntityToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        name = self._preporcess_input(name)
        follow_entity(self.entity_name, name)
        return f"\nSuccessfully follow entity {name}\n"


class ListFollowsTool(BaseAgentNoInputTool):
    name: str = "list_follows"
    description: str = "useful when you need to list all you follows"
    args_schema: Optional[Type[BaseModel]] = None
    handle_tool_error: bool = True

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        df = list_follows(entity_name=self.entity_name)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListPopularEntitiesToolInput(BaseModel):
    n: int = Field(description="number of entities")


class ListPopularEntitiesTool(BaseAgentTool):
    name: str = "list_popular_entities"
    description: str = "useful when you need to list popular entities"
    args_schema: Optional[Type[BaseModel]] = ListPopularEntitiesToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = list_popular_entities(n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"


class ListRecentReadingPapersToolInput(BaseModel):
    date_time: str = Field(description="reading date time")


class ListRecentReadingPapersTool(BaseAgentTool):
    name: str = "list_recent_reading_papers"
    description: str = "useful when you need to find out all reading papers from a given date"
    args_schema: Optional[Type[BaseModel]] = ListRecentReadingPapersToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        date_time: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        date_time = self._preporcess_input(date_time)
        try:
            datetime.strptime(date_time, "%Y-%m-%d")
        except Exception:
            self._raise_tool_error(
                "Input argument `date_time` should be written in format `YYYY-MM-DD`, "
                "please check your input, valid input can be 1995-03-01, 2024-01-01.\n"
            )

        df = list_recent_reading_papers(entity_name=self.entity_name, date_time=date_time)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
