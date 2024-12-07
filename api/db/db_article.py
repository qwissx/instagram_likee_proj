from api.schemas import ArticleBase
from sqlalchemy.orm.session import Session
from .models import DbArticle
from . import postgres

class ArticleDAO:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_article(self, request: ArticleBase):
        new_article = DbArticle(
            title=request.title,
            content=request.content,
            published=request.published,
            creater_id=request.creater_id
        )
        self.db.add(new_article)
        self.db.commit()
        self.db.refresh(new_article)
        return new_article

    def get_article(self, id: int):
        article = self.db.query(DbArticle).filter(DbArticle.id == id).first()
        return article
    
articledao = ArticleDAO(postgres.postgre_db.get_db())