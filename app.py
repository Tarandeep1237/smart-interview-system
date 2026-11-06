import os
from flask import Flask
from dotenv import load_dotenv

from backend.routes.main_routes import main_routes
from backend.routes.auth_routes import auth_routes
from backend.routes.profile_routes import profile_routes
from backend.routes.resume_routes import resume_routes
from backend.routes.skill_routes import skill_routes
from backend.routes.interview_routes import interview_routes
from backend.routes.dashboard_routes import dashboard_routes
from backend.routes.results_routes import results_routes


app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static"
)

load_dotenv()
app.secret_key = os.getenv("FLASK_SECRET_KEY")


app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(profile_routes)
app.register_blueprint(resume_routes)
app.register_blueprint(skill_routes)
app.register_blueprint(interview_routes)
app.register_blueprint(dashboard_routes)
app.register_blueprint(results_routes)


if __name__ == "__main__":
    app.run(debug=True)