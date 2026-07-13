from fastapi import APIRouter, File, UploadFile, status

from app.api.deps import CurrentUser, DbSession
from app.schemas.ocr import OCRRead
from app.services.bot_transaction import BotTransactionService
from app.services.ocr import OCRService


router = APIRouter()


@router.post("/receipt", response_model=OCRRead, status_code=status.HTTP_201_CREATED)
async def upload_receipt(file: UploadFile = File(...), db: DbSession = None, current_user: CurrentUser = None):
    file_bytes = await file.read()
    service = OCRService()
    extracted_text = service.extract_text(file_bytes)
    parsed = service.parse_receipt(extracted_text)

    if not parsed:
        return OCRRead(extracted_text=extracted_text, message="Receipt text extracted, but transaction could not be inferred.")

    BotTransactionService(db).create_transaction_from_parsed(parsed, current_user.id)
    return OCRRead(
        extracted_text=extracted_text,
        message="Receipt processed and transaction saved.",
        parsed=parsed.model_dump(mode="json"),
    )
