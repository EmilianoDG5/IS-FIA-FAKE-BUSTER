import os
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://fakebuster:fakebuster@localhost/fakebuster_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "fakebuster-secret-key"
SCORE_THRESHOLD = 0.7


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads", "posts")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
