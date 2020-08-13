from flask import Blueprint, request, session, g
from app.service.database import get_db_session
from app.model.user import User
from sqlalchemy.orm.exc import NoResultFound
from flasgger import swag_from
from app.view import UserView, MessageView
import functools

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db_session = get_db_session()
        g.user = db_session.query(User).filter(User.id == user_id).one()


@auth.route('/register', methods=('POST',))
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'email',
            'in': 'formData',
            'description': 'New user email',
            'required': True,
            'type': 'string'
        },
    ],
    'responses': {
        200: {
            'description': 'Successfully registered',
            'schema': MessageView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def register():
    email = request.form['email']
    if not email:
        return {
            'result': 'error',
            'message': 'Email is required'
        }, 400
    
    db_session = get_db_session()
    count = db_session.query(User).filter(User.email == email).count()
    if count:
        return {
            'result': 'error',
            'message': 'User with this email already exists'
        }, 400

    user = User(email=email)
    db_session.add(user)
    db_session.commit()
    session['user_id'] = user.id

    return {
        'result': 'ok',
        'message': 'User registered'
    }


@auth.route('/login', methods=('POST',))
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'email',
            'in': 'formData',
            'description': 'User email',
            'required': True,
            'type': 'string'
        },
    ],
    'responses': {
        200: {
            'description': 'Successfully logged int',
            'schema': MessageView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def login():
    if 'email' not in request.form:
        return {
            'result': 'error',
            'message': 'Email is required'
        }, 400
    email = request.form['email']
    db_session = get_db_session()
    try:
        user: User = db_session.query(User).filter(User.email == email).one()
    except NoResultFound:
        db_session.close()
        return {
            'result': 'error',
            'message': 'No user found'
        }, 400

    session.clear()
    session['user_id'] = user.id
    return {
        'result': 'ok',
        'message': 'Logged in'
    }


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return MessageView().dump({
                'result': 'error',
                'message': 'Login is required'
            }), 400
        return view(**kwargs)
    return wrapped_view


@auth.route('/logout', methods=('POST',))
@login_required
@swag_from({
    'tags': ['Auth'],
    'responses': {
        200: {
            'description': 'Successfully logged out',
            'schema': MessageView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def logout():
    session.clear()
    return {
        'result': 'ok',
        'message': 'Logged out'
    }


@auth.route('/user')
@login_required
@swag_from({
    'tags': ['Auth'],
    'responses': {
        200: {
            'description': 'Return logged in user',
            'schema': UserView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def get_user():
    return UserView().dump(g.user)
