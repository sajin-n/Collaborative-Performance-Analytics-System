from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, SignupForm

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_teacher():
            return redirect(url_for("dashboard.admin_dashboard"))
        else:
            return redirect(url_for("dashboard.student_dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Account is inactive", "warning")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_has_allowed_host_and_scheme(next_page):
            if user.is_teacher():
                next_page = url_for("dashboard.admin_dashboard")
            else:
                next_page = url_for("dashboard.student_dashboard")

        return redirect(next_page)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.student_dashboard"))

    form = SignupForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken", "danger")
            return redirect(url_for("auth.signup"))

        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered", "danger")
            return redirect(url_for("auth.signup"))

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            role="student",  # Default role is student
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


def url_has_allowed_host_and_scheme(url):
    from urllib.parse import urlparse

    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc == request.host
