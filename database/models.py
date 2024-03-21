from sqlalchemy import DateTime, String, Text, Float, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now()) # Вказуємо що поле created має бути типу DateTime, default=func.now() - це значення яке буде встановлено за замовчуванням при створенні запису
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now()) # Вказуємо що поле updated має бути типу DateTime, default=func.now() - це значення яке буде встановлено за замовчуванням при створенні запису, onupdate=func.now() - це значення яке буде встановлено при оновленні запису



class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False) # Вказуємо що поле name не може бути пустим (nullable=False), String(150) - це максимальна довжина тексту який може бути в цьому полі
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False) # Вказуємо що поле price не може бути пустим (nullable=False), Float(asdecimal=True) - це тип поля, який приймає дробові числа
    image: Mapped[str] = mapped_column(String(150))

