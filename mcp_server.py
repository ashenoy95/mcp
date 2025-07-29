from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(name="read_doc_contents", description="Read the contents of a document and return it as a string")
def read_document(doc_id: str = Field(description="The ID of the document to read")) -> str:
    """
    Reads the contents of a document by its ID.
    """
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError(f"Document with ID '{doc_id}' not found.")
    
    
@mcp.tool(name="edit_doc", description="Edit a document by replacing a string with another string")
def edit_document(
    doc_id: str = Field(description="The ID of the document to edit"), 
    old_string: str = Field(description="String to replace. Must exactly match, including whitespace."), 
    new_string: str = Field(description="String to replace with.")
):
    """
    Edits a document by replacing an old string with a new string.
    """
    if doc_id in docs:
        if old_string in docs[doc_id]:
            docs[doc_id] = docs[doc_id].replace(old_string, new_string)
            # return f"Document '{doc_id}' updated successfully."
        else:
            raise ValueError(f"String '{old_string}' not found in document '{doc_id}'.")
    else:
        raise ValueError(f"Document with ID '{doc_id}' not found.")

# TODO: Write a resource to return all doc id's
@mcp.resource(uri="docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    """
    Returns a list of all document IDs.
    """
    return list(docs.keys())

# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(uri="docs://documents/{doc_id}", mime_type="text/plain")
def get_doc(doc_id: str) -> str:
    """
    Returns the contents of a document by its ID.
    """
    if doc_id in docs:
        return docs[doc_id]
    else:
        raise ValueError(f"Document with ID '{doc_id}' not found.") 

# TODO: Write a prompt to rewrite a doc in markdown format
@mcp.prompt(name="format", description="Rewrite a document in markdown format")
def format_doc(doc_id: str = Field(description="ID of document to form")) -> list[base.Message]:
    """
    Formats a document in markdown format.
    """
    prompt = f"""
    Your goal is to reformat a document in markdown format.
    The ID of the document is: 
    <document_id>{doc_id}</document_id>

    Add in headers, bullet points, and other markdown formatting as appropriate.
    Use the edit_doc tool to edit the document.
    """
    return [base.UserMessage(prompt)]
    
# TODO: Write a prompt to summarize a doc
if __name__ == "__main__":
    mcp.run(transport="stdio")
