from __future__ import annotations

from urllib.parse import urlparse, urljoin

from flask import Flask, abort, redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user

from . import create_app as _create_app, db
from .forms import LoginForm, SignupForm, PostForm
from .models import User, Post


def is_safe_url(target: str) -> bool:
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


def register_routes(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500
    @app.route("/")
    def index():
        posts = Post.get_all()
        return render_template("index.html", posts=posts)

    @app.route("/post/<slug>/")
    def post_detail(slug: str):
        post = Post.get_by_slug(slug)
        if not post:
            abort(404)
        return render_template("post_detail.html", post=post)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_url = request.args.get("next")
                if next_url and is_safe_url(next_url):
                    return redirect(next_url)
                return redirect(url_for("index"))
            flash("Invalid credentials", "error")
        return render_template("login_form.html", form=form)

    @app.route("/signup/", methods=["GET", "POST"])
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = SignupForm()
        if form.validate_on_submit():
            if User.get_by_email(form.email.data):
                form.email.errors.append("Email already registered")
            else:
                try:
                    user = User(username=form.username.data, email=form.email.data)
                    user.set_password(form.password.data)
                    user.save()
                    login_user(user)
                    return redirect(url_for("index"))
                except Exception as ex:
                    # fallback: surface generic error
                    flash("Could not create account", "error")
        return render_template("admin/signup_form.html", form=form)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/admin/post/", methods=["GET", "POST"])
    @login_required
    def create_post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(
                user_id=current_user.id,
                title=form.title.data,
                content=form.content.data,
                category=form.category.data,
                slug="",
            )
            post.save()
            return redirect(post.public_url())
        return render_template("admin/post_form.html", form=form)

    @app.route("/admin/post/<slug>/edit/", methods=["GET", "POST"])
    @login_required
    def edit_post(slug: str):
        post = Post.get_by_slug(slug)
        if not post:
            abort(404)
        
        # Verificar que el usuario actual es el autor del post
        if post.user_id != current_user.id:
            flash("No tienes permisos para editar este post", "error")
            return redirect(url_for("post_detail", slug=slug))
        
        form = PostForm(obj=post)
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.category = form.category.data
            # Regenerar slug si el título cambió
            if post.title != form.title.data:
                post.slug = ""
            post.save()
            flash("Post actualizado exitosamente", "success")
            return redirect(post.public_url())
        return render_template("admin/post_form.html", form=form, post=post, is_edit=True)

    @app.route("/admin/post/<slug>/delete/", methods=["POST"])
    @login_required
    def delete_post(slug: str):
        post = Post.get_by_slug(slug)
        if not post:
            abort(404)
        
        # Verificar que el usuario actual es el autor del post
        if post.user_id != current_user.id:
            flash("No tienes permisos para eliminar este post", "error")
            return redirect(url_for("post_detail", slug=slug))
        
        try:
            db.session.delete(post)
            db.session.commit()
            flash("Post eliminado exitosamente", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error al eliminar el post", "error")
        
        return redirect(url_for("index"))

    @app.route("/admin/users/")
    @login_required
    def admin_users():
        """Vista de administración para ver usuarios (solo para desarrollo)."""
        users = User.query.all()
        return render_template("admin/users_list.html", users=users)


def create_app() -> Flask:
    app = _create_app()
    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

