from various import *
from data import db_session
import blueprint
import resources
import main_page
import login
import topic
from flask_ngrok import run_with_ngrok

login_manager.init_app(app)
run_with_ngrok(app)
if __name__ == "__main__":
    db_session.global_init("db/blogs.sqlite")
    app.register_blueprint(blueprint.blueprint)
    api.add_resource(resources.TopicListResource, '/api/topics/')
    api.add_resource(resources.TopicResource, '/api/topics/<int:topic_id>')
    api.add_resource(resources.LikeResource, '/api/topics/<int:topic_id>/likes/<int:user_id>')
    api.add_resource(resources.CommentResource, '/api/comments/<int:comment_id>')
    api.add_resource(resources.CommentListResource, '/api/topics/<int:topic_id>/comments/')
    app.run()
