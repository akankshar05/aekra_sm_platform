from fastapi import APIRouter
from .models import FollowRequest
from .storage import followers, following

router = APIRouter()


@router.post("/follow")
def follow_user(payload: FollowRequest):
    followers.setdefault(payload.following_id, set()).add(payload.follower_id)
    following.setdefault(payload.follower_id, set()).add(payload.following_id)

    return {"message": "followed"}


@router.post("/unfollow")
def unfollow_user(payload: FollowRequest):
    followers.get(payload.following_id, set()).discard(payload.follower_id)
    following.get(payload.follower_id, set()).discard(payload.following_id)

    return {"message": "unfollowed"}


@router.get("/followers/{user_id}")
def get_followers(user_id: str):
    return {"followers": list(followers.get(user_id, []))}


@router.get("/following/{user_id}")
def get_following(user_id: str):
    return {"following": list(following.get(user_id, []))}
