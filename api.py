import flask
from data import db_session
from data.users import User
from data.news import News
from flask.json import jsonify
from flask import make_response, request
from main import app

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


blueprint = flask.Blueprint('news_api', __name__, 
                            template_folder='templates')


@blueprint.route('/api/news')
def get_news():
    session = db_session.create_session()
    news = session.query(News).all()
    return jsonify(
        {
            'news':
                [item.to_dict(only=('news_tittle', 'news', 'user.name')) 
                 for item in news]
        }
    )


@blueprint.route('/api/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'news': news.to_dict(only=('news_tittle', 'news', 'user.name'))
        }
    )

@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in 
                 ['news_tittle', 'news', 'user_id', 'usered']):
        return jsonify({'error': 'Bad request'})
    session = db_session.create_session()
    news = News(
        news_tittle=request.json['news_tittle'],
        news=request.json['news'],
        user_id=request.json['user_id'],
        usered=request.json['usered']
    )
    session.add(news)
    session.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        return jsonify({'error': 'Not found'})
    session.delete(news)
    session.commit()
    return jsonify({'success': 'OK'})