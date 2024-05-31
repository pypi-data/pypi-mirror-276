import os

from typing import Type, Optional
from langchain.pydantic_v1 import BaseModel, Field

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyMuPDFLoader

from docmesh_core.db.neo.entity import mark_paper_read, list_latest_reading_papers
from docmesh_core.db.neo.paper import get_paper, add_paper
from docmesh_core.utils.semantic_scholar import get_paper_id
from docmesh_agent.tools.base import BaseAgentTool


class AddPaperToolInput(BaseModel):
    paper: str = Field(description="paper title or arxiv id")


class AddPaperTool(BaseAgentTool):
    name: str = "add_paper"
    description: str = "useful when you need to add a paper using title or arxiv id"
    args_schema: Optional[Type[BaseModel]] = AddPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper = self._preporcess_input(paper)
        paper_id = get_paper_id(paper=paper)

        if paper_id is None:
            self._raise_tool_error(f"Cannot find paper id for {paper}, you may end execution.")

        try:
            add_paper(paper_id=paper_id)
            msg = f"Successfully add paper {paper} with id {paper_id} into database."
        except Exception as e:
            msg = f"Failed to add paper {paper} into database with error: {e}."

        return f"\n{msg}\n"


class GetPaperIdToolInput(BaseModel):
    paper: str = Field(description="paper title")


class GetPaperIdTool(BaseAgentTool):
    name: str = "get_paper_id"
    description: str = "useful when you need to find a paper id"
    args_schema: Optional[Type[BaseModel]] = GetPaperIdToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper = self._preporcess_input(paper)
        paper_id = get_paper_id(paper=paper)

        if paper_id is None:
            self._raise_tool_error(f"Cannot find paper id for {paper}, you may end execution.")

        try:
            paper_id = get_paper(paper=paper_id).paper_id
            msg = f"Successfully find paper id {paper_id} for {paper}."
        except Exception as e:
            msg = f"Failed to find paper id for {paper} with error: {e}."

        return f"\n{msg}\n"


class GetPaperPDFToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class GetPaperPDFTool(BaseAgentTool):
    name: str = "get_paper_pdf_link"
    description: str = "useful when you need to find the pdf of a paper"
    args_schema: Optional[Type[BaseModel]] = GetPaperPDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)

        try:
            paper = get_paper(paper=paper_id)
        except Exception:
            self._raise_tool_error(
                "Input argument `paper_id` should be a valid paper id, please check your input. "
                "Pay attention that the paper id is not arxiv id."
            )

        if paper.pdf is None:
            msg = "Unable to find the pdf link for provided paper."
        else:
            msg = paper.pdf

        return f"\n{msg}\n"


class ReadWholePDFToolInput(BaseModel):
    pdf_link: str = Field(description="pdf link of paper")


class ReadWholePDFTool(BaseAgentTool):
    name: str = "read_whole_pdf"
    description: str = "useful when you need to read the whole PDF content, use if with cautions"
    args_schema: Optional[Type[BaseModel]] = ReadWholePDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        pdf_link: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        pdf_link = self._preporcess_input(pdf_link)

        try:
            loader = PyMuPDFLoader(pdf_link)
            pages = loader.load()
            msg = "\n".join([page.page_content for page in pages])
        except Exception:
            msg = "Failed to read the PDF content."

        return f"\n{msg}\n"


class ReadPartialPDFToolInput(BaseModel):
    pdf_link: str = Field(description="pdf link of paper")
    query: str = Field(description="search query")


class ReadPartialPDFTool(BaseAgentTool):
    name: str = "read_partial_pdf"
    description: str = "useful when you need to read partial PDF content with query"
    args_schema: Optional[Type[BaseModel]] = ReadPartialPDFToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        pdf_link: str,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        pdf_link = self._preporcess_input(pdf_link)

        try:
            loader = PyMuPDFLoader(pdf_link)
            pages = loader.load()

            faiss_index = FAISS.from_documents(
                pages,
                OpenAIEmbeddings(
                    base_url=os.getenv("OPENAI_EMBEDDING_API_BASE"),
                    api_key=os.getenv("OPENAI_EMBEDDING_API_KEY"),
                    model=os.getenv("OPENAI_EMBEDDING_MODEL"),
                ),
            )
            similar_pages = faiss_index.similarity_search(query, k=2)
            msg = "\n".join([f"Paragraph: {i + 1}\n{page.page_content}" for i, page in enumerate(similar_pages)])
        except Exception:
            msg = "Failed to read the PDF content."
        return f"\n{msg}\n"


class MarkPaperReadToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class MarkPaperReadTool(BaseAgentTool):
    name: str = "mark_paper_read"
    description: str = "useful when you need to mark a paper read"
    args_schema: Optional[Type[BaseModel]] = MarkPaperReadToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        mark_paper_read(entity_name=self.entity_name, paper_id=paper_id)
        msg = f"Successfully mark paper {paper_id} read."
        return f"\n{msg}\n"


class PaperSummaryToolInput(BaseModel):
    paper_id: str = Field(description="paper id")


class PaperSummaryTool(BaseAgentTool):
    name: str = "paper_summary"
    description: str = (
        "useful when you need to genearte the paper summary, return a short summary for a given paper id."
    )
    args_schema: Optional[Type[BaseModel]] = PaperSummaryToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        paper_id: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        paper_id = self._preporcess_input(paper_id)
        try:
            paper = get_paper(paper=paper_id)
        except Exception:
            self._raise_tool_error(
                "Input argument `paper_id` should be a paper id, please check your input. "
                "Pay attention that paper_id is not arxiv id."
            )
        msg = paper.summary
        return f"\n{msg}\n"


class ListLatestPaperToolInput(BaseModel):
    n: int = Field(description="number of papers")


class ListLatestPaperTool(BaseAgentTool):
    name: str = "list_latest_papers"
    description: str = (
        "useful when you need to find out latest reading papers, "
        "return a list of paper ids and titles for a given number."
    )
    args_schema: Optional[Type[BaseModel]] = ListLatestPaperToolInput
    handle_tool_error: bool = True

    def _run(
        self,
        n: int,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        n = self._preporcess_input(n)
        df = list_latest_reading_papers(entity_name=self.entity_name, n=n)
        msg = self._dataframe_to_msg(df)
        return f"\n{msg}\n"
