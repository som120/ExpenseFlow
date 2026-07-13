from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.category import Category


DEFAULT_CATEGORIES = [
    "Food",
    "Groceries",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Rent",
    "Healthcare",
    "Education",
    "Travel",
    "Subscriptions",
    "Salary",
    "Freelance",
    "Investment",
    "Gift",
    "Refund",
    "Others",
]


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name(self, name: str, user_id=None) -> Category | None:
        stmt = (
            select(Category)
            .where(Category.name == name)
            .where(or_(Category.user_id == user_id, Category.is_system.is_(True)))
        )
        return self.db.scalar(stmt)

    def seed_defaults(self) -> None:
        existing = {
            name for name, in self.db.execute(select(Category.name).where(Category.is_system.is_(True)))
        }
        missing = [Category(name=name, is_system=True) for name in DEFAULT_CATEGORIES if name not in existing]
        if missing:
            self.db.add_all(missing)
            self.db.commit()

    def list(self, user_id) -> list[Category]:
        stmt = (
            select(Category)
            .where(or_(Category.user_id == user_id, Category.is_system.is_(True)))
            .order_by(Category.name.asc())
        )
        return list(self.db.scalars(stmt).all())
