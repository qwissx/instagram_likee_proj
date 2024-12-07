from fastapi import APIRouter, HTTPException
from api.schemas import ArticleBase, ArticleDisplay
from ..db.db_article import articledao
from typing import List

article_router = APIRouter(
    prefix='/article',
    tags=['article'],
)

@article_router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase):
    return articledao.create_article(request)

@article_router.get('/{id}', response_model=ArticleDisplay)
def get_article(id: int):
    return articledao.get_article(id)