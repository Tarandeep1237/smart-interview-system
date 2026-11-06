from flask import Blueprint, render_template, session, redirect


main_routes = Blueprint(
    "main_routes",
    __name__
)


@main_routes.route("/")
def home():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template(
        "index.html"
    )


@main_routes.route("/register")
def register_page():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template(
        "register.html"
    )


@main_routes.route("/login")
def login_page():

    if "user_id" in session:
        return redirect("/dashboard")

    return render_template(
        "login.html"
    )


@main_routes.route("/logout")
def logout():

    session.clear()

    return redirect("/")


@main_routes.route("/profile")
def profile_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "profile.html"
    )


@main_routes.route("/resume")
def resume_page():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "resume.html"
    )