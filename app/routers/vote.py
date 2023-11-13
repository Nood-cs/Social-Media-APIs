from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), curr_user : int = Depends(oauth2.get_current_user)):

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == curr_user.id)
    
    found_vote = vote_query.first()
    if(vote.dir == 1):
        if(found_vote):
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                             detail=f"cannot like post twice!")
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = curr_user.id  ,**vote.dict())
    
            db.add(new_vote)
            db.commit()
            return {"message": "you liked the post!"}
    else:
        if(found_vote is None):
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found!")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)