from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db



router = APIRouter(     #this is becouse we dont have access to app again. so we define router and link it to app on main.py
    prefix="/post",     #since all our path starts with /post we dont have to be repeating. so we will remove /post from the request.
    tags= ['Post']         #This is just to group our API in the /docs
    )



# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM post """) #Note to use raw sql, you should remove the dependency i.e db Session = Depends(get_db)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #the limit inside is 10. just like we defined in get_post function

    posts_with_votes = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    return posts_with_votes




# @router.get("/{id}", response_model=schemas.Post)
@router.get("/{id}", response_model=schemas.PostWithVotes)
def get_post(id: int, db: Session = Depends(get_db)): 
    # cursor.execute("""SELECT * FROM post WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post_with_vote = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} dont exist")
    return post_with_vote


   # @router.post("/posts")
# def creat_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"tittle": f"{payload['tittle']}", "content": f"{payload['content']}"}




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def creat_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)): # the function of {current_user: int=Depends(oauth2.get_current_user)} is to prtect this route as defined on the auth.py and oauth2.py. you can add it to all the router you need to protect
    # cursor.execute("""INSERT INTO post (title, content, published) VALUES(%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # new_post = models.Post(**post.dict()) #This will reduce the stress of typing as in line 78
    new_post = models.Post(owner_id=current_user.id, **post.model_dump()) #VScode suggested i use model_dump in place of .dict and it also worked. The ** is to dismountile what is being gotten from post.model and covert it to dictionary. The current_user.id which was equated to owner_id(a new colum added to posts table) is to retrive the id of the current user from current_user. 
    
    db.add(new_post)
    db.commit()

    db.refresh(new_post) #this will make it possible for post man to retrieve the newly added post. just like RETURNING in SQL

    return new_post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM post WHERE id = %s RETURNING * """,(str(id),))
    # deleted_post = cursor.fetchone()

    post_to_delete = db.query(models.Post).filter(models.Post.id == id)

    post = post_to_delete.first()

    if post == None: #this checks if post exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} dont exist")
    
    if post.owner_id != current_user.id: # this checks and make sure the user trying to delete a post is the aurth of the post.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") 

    post_to_delete.delete(synchronize_session=False)
    # conn.commit()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post_update_from_frontend: schemas.PostCreate, db: Session = Depends(get_db), current_user: int=Depends(oauth2.get_current_user)): #the reason for adding post(this is what we are getting from front end user) and making it PostCreate(the schema we defined to control our input type) is to control what the users are sending back to us as it was declared class (BaseModel). it is call shema
    # cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id),))

    # post_to_update = cursor.fetchone()

    post_to_update = db.query(models.Post).filter(models.Post.id == id)

    post = post_to_update.first()
 
    if post == None: #this checks if the post esixt
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} dont exist") 
    

    if post.owner_id != current_user.id: #this checks if the user updating is the owner
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_to_update.update(post_update_from_frontend.model_dump(), synchronize_session=False) #the post_update_from_frontend in (post_update_from_frontend.model_dump) is the one we are getting from front end i.e postman as define in line 114
    # conn.commit()
    db.commit()
    return post_to_update.first()