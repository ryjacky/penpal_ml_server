from typing import Annotated

from PIL.Image import Image
from modules.auth.authorization import validate_session_with_supabase
from modules.ocr.ocr_client import OCRClient
from modules.ocr.prototype_ocr_client import PrototypeOCRClient
from modules.ocr.types import ImageContent
from fastapi import APIRouter, UploadFile, Depends, HTTPException

from modules.ocr.preprocessing import pre_process_image

ocr_router = APIRouter(prefix="/ocr")
client: OCRClient = PrototypeOCRClient()

@ocr_router.post("/text")
async def get_text(
        file: UploadFile,
        credentials: Annotated[str, Depends(validate_session_with_supabase)]) -> ImageContent:
    """
    Receives an image file that is cropped to the bounds of the document page.
    Returns a JSON object containing the file contents.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type, only images are allowed")

    print(f"Reading image...")
    b_image = await file.read()

    print(f"Preprocessing image...")
    image: Image = pre_process_image(b_image)
    image.save("runtime_image.jpg")
    print(f"Preprocessing complete. Detecting text...")

    # word_segs = get_word_segments(image)
    # print(f"Found {len(word_segs)} words.")

    # line_segs = get_line_segments(image, word_segs)
    # print(f"Found {len(line_segs)} lines.")

    # result = ImageContent(content="")

    # for line_seg in line_segs:
    #     result.content += f" {recognize_text(line_seg.image)}"
    #     print(f"Recognized text: {recognize_text(line_seg.image)}")

    return ImageContent(content=client.extract_writing(image))