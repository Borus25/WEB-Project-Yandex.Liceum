import json
from flask import Flask, render_template, redirect, request, abort, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime
from data import db_session
from data.comments import Comment
from data.posts import Post
from data.users import User
from forms.comment import CommentForm
from forms.user import RegisterForm, LoginForm
from forms.post import PostForm
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


pathToImg = "C:/Users/Максим/PycharmProjects/WEB site (Yandex Project)/static/img"
pathToAvatar = pathToImg + "/avatar"


def convertToBinaryData(path, filename):
    with open(path + "/" + filename, 'rb') as file:
        blobData = file.read()
    return blobData


def createImage(path, binary_data):
    if os.path.exists(path + "/" + "1.png"):
        os.remove(path + "/" + "1.png")
        with open(path + "/" + "1.png", "wb") as img:
            img.write(binary_data)
    else:
        with open(path + "/" + "1.png", "wb") as img:
            img.write(binary_data)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/BodyBoost.db")
    app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    return render_template("index.html", posts=posts, title="Главная страница")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.login == form.login.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.name = form.name.data
        user.login = form.login.data
        user.img = convertToBinaryData(pathToAvatar, "defaultava.jpg")
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/example")
def example():
    return render_template("example_html.html")


@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        post = Post()
        user = db_sess.query(User).filter(User.id == current_user.id).first()
        post.creator_name = user.name
        post.creator_surname = user.surname
        post.creator_id = current_user.id
        post.creator_login = user.login
        post.post_name = form.post_title.data
        if form.file.data:
            image = convertToBinaryData(pathToImg, form.file.data)
            print('+')
        else:
            image = convertToBinaryData(pathToImg, "default.jpg")
            print('-')
        post.file = image
        post.text_content = form.text_content.data
        post.is_blog = form.is_blog.data
        post.is_training = form.is_training.data
        post.is_recipe = form.is_recipe.data
        db_sess.add(post)
        db_sess.commit()
        return redirect('/')
    return render_template("add_post.html", form=form, page_title="Создание поста",
                           title="Написание поста")


@app.route("/edit_post/<int:id>", methods=['GET', 'POST'])
def edit_post(id: int):
    form = PostForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        post = db_sess.query(Post).filter(Post.id == id,
                                          (Post.user == current_user) | (Post.user == current_user == 1)).first()
        if post:
            form.post_title.data = post.post_name
            form.text_content.data = post.text_content
            form.file.data = post.file
            form.is_blog.data = post.is_blog
            form.is_recipe.data = post.is_recipe
            form.is_training.data = post.is_training
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.file.data:
            image = convertToBinaryData(pathToImg, form.file.data)
        else:
            image = convertToBinaryData(pathToImg, "default.jpg")
        post = db_sess.query(Post).filter(Post.id == id, (Post.user == current_user) | (Post.user == current_user == 1)).first()
        if post:
            post.post_name = form.post_title.data
            post.file = image
            post.text_content = form.text_content.data
            post.is_blog = form.is_blog.data
            post.is_training = form.is_training.data
            post.is_recipe = form.is_recipe.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template("add_post.html", form=form, page_title="Редактирование поста",
                           title="Редактирование поста")


@app.route('/post_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def job_delete(id: int):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id,
                                     (Post.user == current_user) | (Post.user == current_user == 1)).first()
    if post:
        db_sess.delete(post)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/post_review/<int:id>")
def post_review(id: int):
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id).first()
    createImage(pathToImg, post.file)
    data = [post.is_liked, post.id]
    is_file = True if os.path.exists(pathToImg + "/" + "1.png") else False
    return render_template("post_review.html", post=post, is_file=is_file, data=map(json.dumps, data))


@app.route("/profile/<string:login>")
def profile(login: str):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.login == login).first()
    createImage(pathToAvatar, user.img)
    is_file = True if os.path.exists(pathToAvatar + "/" + "1.png") else False
    return render_template("user_profile.html", user=user, is_file=is_file)


@app.route("/posts/<string:login>")
def posts_of_users(login: str):
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.creator_login == login)
    for post in posts:
        print(post)
    return render_template("posts_of_user.html", posts=posts, title=f"Посты {login}")


@app.route("/comments/<int:id>")
def comments(id):
    db_sess = db_session.create_session()
    comments = db_sess.query(Comment).filter(Comment.post_id == id).all()
    if comments:
        return render_template("comments.html", id=id, comments=comments, message="")
    else:
        return render_template("comments.html", id=id, comments=comments, message="Пока нет никаких комментариев")
    

@app.route("/comments/<int:id>/add_comment", methods=["GET", "POST"])
def add_comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        comment = Comment()
        post = db_sess.query(Post).filter(Post.id == id).first()
        comment.author_name = post.creator_name
        comment.author_surname = post.creator_surname
        comment.post_id = id
        comment.author_login = post.creator_login
        comment.text = form.text.data
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/comments/{id}')
    return render_template("add_comment.html", form=form, page_title="Комментарий к посту",
                           title="Написание комментария")


if __name__ == '__main__':
    main()
