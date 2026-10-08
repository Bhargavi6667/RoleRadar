import io
from typing import Dict, Any, List
import pymupdf as fitz

class PdfService:
    @staticmethod
    def extract_text_from_bytes(file_bytes: bytes) -> str:
        """Extract clean text from PDF bytes using PyMuPDF."""
        text_parts = []
        try:
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    text = page.get_text("text")
                    if text:
                        text_parts.append(text.strip())
            return "\n\n".join(text_parts)
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

    @staticmethod
    def extract_metadata(file_bytes: bytes) -> Dict[str, Any]:
        """Extract PDF metadata such as page count, author, and creation date."""
        try:
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                metadata = doc.metadata or {}
                return {
                    "pages": len(doc),
                    "author": metadata.get("author", ""),
                    "title": metadata.get("title", ""),
                    "format": metadata.get("format", "PDF"),
                }
        except Exception:
            return {"pages": 1, "format": "PDF"}

pdf_service = PdfService()
