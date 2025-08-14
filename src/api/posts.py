from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.db.database import get_db
from src.models.post import Post, Like, Comment
from src.schemas.post import PostCreate, PostResponse
from src.schemas.comment import CommentCreate, CommentResponse
from src.api.dependencies import get_current_user

router = APIRouter()

# Create Post
@router.post("/", response_model=PostResponse)
def create_post(post_data: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_post = Post(title=post_data.title, content=post_data.content, author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Get all posts
@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()

# Get single post by ID
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Update post
@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    post.title = post_data.title
    post.content = post_data.content
    db.commit()
    db.refresh(post)
    return post

# Delete post
@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}

# Like a post
@router.post("/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing_like = db.query(Like).filter(Like.post_id == post.id, Like.user_id == current_user.id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="Already liked")

    new_like = Like(post_id=post.id, user_id=current_user.id)
    db.add(new_like)
    db.commit()
    return {"detail": "Post liked"}

# Add comment to a post
@router.post("/{post_id}/comment", response_model=CommentResponse)
def add_comment(post_id: int, comment_data: CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(content=comment_data.content, post_id=post.id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Get comments for a post
@router.get("/{post_id}/comments", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return db.query(Comment).filter(Comment.post_id == post.id).all()
