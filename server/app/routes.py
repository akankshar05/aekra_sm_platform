from fastapi import APIRouter, HTTPException, status
from .models import FollowRequest
from .storage import followers, following

router = APIRouter()


@router.post("/follow", status_code=status.HTTP_201_CREATED)
def follow_user(payload: FollowRequest):
    if payload.follower_id == payload.following_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot follow yourself")

    if payload.follower_id in followers.get(payload.following_id, set()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="already following")

    followers.setdefault(payload.following_id, set()).add(payload.follower_id)
    following.setdefault(payload.follower_id, set()).add(payload.following_id)

    return {"message": "followed"}


@router.post("/unfollow")
def unfollow_user(payload: FollowRequest):
    if payload.follower_id == payload.following_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot unfollow yourself")

    if payload.follower_id not in followers.get(payload.following_id, set()):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="follow relationship not found")

    followers.get(payload.following_id, set()).discard(payload.follower_id)
    following.get(payload.follower_id, set()).discard(payload.following_id)

    return {"message": "unfollowed"}


@router.get("/followers/{user_id}")
def get_followers(user_id: str):
    return {"followers": list(followers.get(user_id, []))}


@router.get("/following/{user_id}")
def get_following(user_id: str):
    return {"following": list(following.get(user_id, []))}
