from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from modules import entries
# from modules import attachment #TODO
origins = [
    'http://localhost:3000',
    'http://localhost',
]
app = FastAPI(root_path='/api/v1')
app.include_router(entries.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
