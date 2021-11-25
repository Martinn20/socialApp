from fastapi import status, HTTPException, Depends, APIRouter
from ..schemas import Vote
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import get_db

router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:Vote, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    vote_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not vote_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user {current_user.id} does not have vote on post {vote.post_id}")
        db.delete(found_vote)
        db.commit()
        return {"message": "Vote removed successfully"}