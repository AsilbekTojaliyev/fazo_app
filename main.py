import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.user import users_router
from routes.login import login_router
from routes.telephone import router_phones
from routes.planshet import router_planshets
from routes.laptop import router_laptops
from routes.file import router_files
from routes.category import router_category
from routes.cart import router_carts
from routes.like import router_likes
from routes.buy import router_buy
from routes.incomit import router_incomes

app = FastAPI(docs_url="/")

app.include_router(login_router)
app.include_router(users_router)
app.include_router(router_category)
app.include_router(router_laptops)
app.include_router(router_planshets)
app.include_router(router_phones)
app.include_router(router_files)
app.include_router(router_likes)
app.include_router(router_carts)
app.include_router(router_buy)
app.include_router(router_incomes)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get('/files/{fileName}')
async def get_file(fileName: str):
    path = f"./files/{fileName}"
    if os.path.isfile(path):
        return FileResponse(path)
    else:
        raise HTTPException(400, "Not Found")
