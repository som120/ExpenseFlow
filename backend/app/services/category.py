import uuid

from sqlalchemy.orm import Session

from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryRead


class CategoryService:
    def __init__(self, db: Session):
        self.categories = CategoryRepository(db)

    def list(self, user_id: uuid.UUID) -> list[CategoryRead]:
        return [CategoryRead.model_validate(item) for item in self.categories.list(user_id)]
