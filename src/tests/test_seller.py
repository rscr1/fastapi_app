import pytest
from fastapi import status
from sqlalchemy import select

from src.models import books, sellers


# Тест создания продавца
@pytest.mark.asyncio
async def test_create_seller(async_client):
    data = {"first_name": "rs", "last_name": "cr", "email": "link49@gmail.com", "password": "1223"}
    response = await async_client.post("/api/v1/seller/", json=data)
    assert response.status_code == status.HTTP_201_CREATED
    result_data = response.json()
    assert result_data ==  {"first_name": "rs", "last_name": "cr", "email": "link49@gmail.com", "id": 6}


# Тест на ручку получения списка продавцов
@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = sellers.Seller(first_name="rs", last_name="cr", email="llama@gmail.com", password="0007")
    seller_2 = sellers.Seller(first_name="cr", last_name="rs", email="llamachain@gmail.com", password="0001")
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()
    response = await async_client.get("/api/v1/seller/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["sellers"]) == 2
    assert response.json() == {
        "sellers": [
            {'first_name': "rs", 'last_name': "cr", 'email': "llama@gmail.com", 'id': seller_1.id},
            {'first_name': "cr", 'last_name': "rs", 'email': "llamachain@gmail.com", 'id': seller_2.id}
        ]
    }


# Тест на ручку получения одного продавца
@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller_1 = sellers.Seller(first_name="rs", last_name="cr", email="llama@gmail.com", password="0007")
    seller_2 = sellers.Seller(first_name="cr", last_name="rs", email="llamachain@gmail.com", password="0001")
    db_session.add_all([seller_1, seller_2])
    await db_session.flush()
    book = books.Book(author="Face", title="Burger", year=2017, count_pages=2, seller_id=seller_1.id)
    db_session.add_all([book])
    await db_session.flush()
    response = await async_client.post("/api/v1/token/", json={"email": "llama@gmail.com", "password": "0007"})
    response = await async_client.get(f"/api/v1/seller/{seller_1.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": seller_1.id,
        "first_name": "rs",
        "last_name": "cr",
        "email": "llama@gmail.com",
        "books": [{"title": "Burger", "author": "Face", "year": 2017, "id": book.id, "count_pages": 2}],
    }


# Тест на ручку удаления продавца
@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller_1 = sellers.Seller(first_name="rs", last_name="cr", email="llama@gmail.com", password="0007")
    db_session.add(seller_1)
    await db_session.flush()
    response = await async_client.delete(f"/api/v1/seller/{seller_1.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    await db_session.flush()
    all_books = await db_session.execute(select(books.Book))
    res = all_books.scalars().all()
    assert len(res) == 0


# Тест на ручку обновления продавцов
@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller_1 = sellers.Seller(first_name="rs", last_name="cr", email="llama@gmail.com", password="0007")
    db_session.add(seller_1)
    await db_session.flush()
    response = await async_client.put(
        f"/api/v1/seller/{seller_1.id}",
        json={"first_name": "Igor", "last_name": "Link", "email": "igrlnk@gmail.com", "id": seller_1.id},
    )
    assert response.status_code == status.HTTP_200_OK
    await db_session.flush()
    res = await db_session.get(sellers.Seller, seller_1.id)
    assert res.first_name == "Igor"
    assert res.last_name == "Link"
    assert res.email == "igrlnk@gmail.com"
    assert res.id == seller_1.id