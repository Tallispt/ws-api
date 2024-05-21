import firebase_admin
from firebase_admin import credentials


class Firebase_Bucket:

    def init_app(self, app):
        cred = credentials.Certificate(app.config["CRED_PATH"])
        firebase_admin.initialize_app(cred, {"storageBucket": app.config["BUCKET_URI"]})


firebase = Firebase_Bucket()
