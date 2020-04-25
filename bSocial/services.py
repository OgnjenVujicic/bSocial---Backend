from flask import jsonify
import datetime
from bSocial import app, db, argon2
from bSocial.models import User, Post, Comment, Followers
from sqlalchemy import exc


def except_msg(e):
    print(str(e.__dict__['orig']))
    return jsonify({"error": "something went wrong"}), 400

def save_changes(model):
    db.session.add(model)
    db.session.commit()

def insert_user(data):
    if User.query.filter_by(email = data['email']).first():
        return jsonify({"error": "email already exists"}), 400
    hashed_pass = argon2.generate_password_hash(data['password'])
    user = User(first_name=data['first_name'], last_name=data['last_name'],
                username=data['username'], email=data['email'], password=hashed_pass)              
    try:   
        save_changes(user)
        return jsonify({'message': 'registered successfully'})
    except exc.SQLAlchemyError as e:
        return except_msg(e)
        
def insert_post(data, current_user):
    try:
        post = Post(title=data['title'], content=data['content'], author=current_user)
        save_changes(post)
        return post.serialize
    except exc.SQLAlchemyError as e:
        return except_msg(e)

       
def insert_comment(data, current_user):
    try:
        comment = Comment(post_id=data['post_id'],content=data['content'])
        save_changes(comment)
        return comment.serialize
    except exc.SQLAlchemyError as e:
        return except_msg(e)

   
def insert_follower(data, current_user):
    try:
        fol = Followers(followed_id=data['user_id'],follow_id=current_user.id)
        save_changes(fol)
        return jsonify({'message': 'Followed successfully'})
    except exc.SQLAlchemyError as e:
        return except_msg(e)

def get_commments(post_id):
    try:
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_time).all()
        return jsonify(comments_list=[i.serialize for i in comments])
    except exc.SQLAlchemyError as e:
        return except_msg(e)

def get_feed(current_user,page):
    try:
        followers_ids = Followers.query.with_entities(Followers.followed_id.label('id'))\
            .filter_by(follow_id=current_user.id)
            
        ids_incuding_own = followers_ids.union(User.query.with_entities(User.id)\
            .filter_by(id=current_user.id))

        posts = Post.query.filter(Post.user_id.in_(ids_incuding_own))\
            .order_by(Post.date_time.desc())\
            .paginate(page=page,per_page=3)
        return jsonify(total=posts.total,total_pages=posts.pages, page=page, next_page=posts.next_num, prev_page=posts.prev_num, posts_list=[i.serialize for i in posts.items])
    except exc.SQLAlchemyError as e:
        return except_msg(e)