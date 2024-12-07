from fastapi import FastAPI
from .router.user import user_router
from .router.article import article_router
from .db import models
from .db import postgres

models.Base.metadata.create_all(postgres.postgre_db._engine)

app = FastAPI(docs_url='/')
app.include_router(user_router)
app.include_router(article_router)