from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return f'Video(name={name}, views={views}, likes={likes})'

# db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video required", required=True)
video_put_args.add_argument("views", type=int, help="Views on the video required", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video required", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str)
video_update_args.add_argument("views", type=int)
video_update_args.add_argument("likes", type=int)

resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video id not found...")
        return video

    @marshal_with(resource_fields)
    def put(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if video:
            abort(409, message="Video id already exists...")

        args = video_put_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        video = VideoModel.query.filter_by(id=video_id).first()
        if not video:
            abort(404, message="Video id not found...")
        
        args = video_update_args.parse_args()
        if len(args) <= 0:
            print(args)
            abort(400, message="At least one of name, views or likes is required...")

        for key, val in args.items():
            if val:
                setattr(video, key, val)
        db.session.commit()
        return video

    def delete(self, video_id):
        VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
