import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from routes.users import users_router
from routes.login import login_router
from routes.phones import router_phones
from routes.tablets import router_planshets
from routes.laptops import router_laptops
from routes.files import router_files
from routes.categories import router_category
from routes.trades import router_trades
from routes.likes import router_likes
from routes.carts import router_carts
from routes.incomes import router_incomes
from routes.main_page import router_main

app = FastAPI(docs_url="/")

app.include_router(router_main)
app.include_router(login_router)
app.include_router(users_router)
app.include_router(router_category)
app.include_router(router_laptops)
app.include_router(router_planshets)
app.include_router(router_phones)
app.include_router(router_likes)
app.include_router(router_carts)
app.include_router(router_trades)
app.include_router(router_incomes)
app.include_router(router_files)

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
