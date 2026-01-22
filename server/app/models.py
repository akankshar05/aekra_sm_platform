from pydantic import BaseModel


class FollowRequest(BaseModel):
    follower_id: str
    following_id: str
