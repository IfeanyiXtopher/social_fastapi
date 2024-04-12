from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware #This will take care of CORS
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


# models.Base.metadata.create_all(bind=engine)                ## Now that i have alembic i can comment out this b/c this is the command that auto create our tables once we put on our server. but we can now do it our self with alembic commends

app = FastAPI()

##### This is from FastAPI docmentation for handling CORS

# origins = ['https://www.google.com', 'https://www.youtube.com'] ## List of webs we which to allow
origins = ['*']  ## We choose to allow all web. * means all
app.add_middleware(         #This takes care of CORS
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # We allow all methods both post, get, delete, put, ...
    allow_headers=["*"],
)

###### handling CORS ends here

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")            #path operation is called
async def root():
    return {"message": "Hello Welcome To World"}
























