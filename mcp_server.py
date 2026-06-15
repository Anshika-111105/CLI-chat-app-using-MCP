from pydoc import doc

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name="read_doc",
    description="Reads the contents of a document given its ID."
)

def read_documments(
    doc_id: str = Field(..., description="The ID of the document to read.")
):
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError("Document not found.")
    
# TODO: Write a tool to edit a doc
@mcp.tool(
    name="edit_doc",
    description="Edits the contents of a document given its ID and new content."
)
def edit_document(
    doc_id: str = Field(..., description="The ID of the document to edit."),
    new_content: str = Field(..., description="The new content for the document.")
):
    if doc_id in docs:
        docs[doc_id] = new_content
        return f"Document '{doc_id}' updated."
    else:
        raise ValueError("Document not found.")

# TODO: Write a resource to return all doc id's
@mcp.resource(
    name="list_docs",
    description="Returns a list of all available document IDs."
)
def list_documents():
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    name="get_doc",
    description="Returns the contents of a specific document."
)
def get_document(doc_id: str = Field(..., description="The ID of the document to retrieve.")):
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError("Document not found.")

@mcp.resource(
    "doc//:documents",
    mime_type="application/json"
)

def list_docs()-> List[str]:
    return list(docs.keys())

@mcp.resource(
    "doc//:document/{doc_id}/{doc_type}",
    mime_type="text/plain"
)


def fetch_doc(doc_id: str, doc_type: str) -> str:
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError("Document not found.")


# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(
    name = "format",
    description = "Rewrites the contents of a documents into markdown format."
)

def format_document(
    doc_id : str = Field(description="Id of the document")
)-> list[base.Message]:
    prompt = f''' Your goal is to reformat a document to be written with markdown syntax. 

    The id of the document that needs to be reformated is:
    <document_id>
    { doc_id }
    <document_id>

    Add headers , bullets , tables ,etc as necessary. Feel free to add extra fields.doc
    Use the 'edit_document' tool to edit the documents.After the document has been submitted.
    
    ''' 

    return [base.UserMessage(prompt)]




# TODO: Write a prompt to summarize a doc

if __name__ == "__main__":
    mcp.run(transport="stdio")
