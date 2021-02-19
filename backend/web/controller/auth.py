from flask import Blueprint, request, session, g

from core.service.password import PasswordService
from web.controller.util import bad_request, ok_request
from web.service.database import get_db_session
from core.model.user import User
from sqlalchemy.orm.exc import NoResultFound
from flasgger import swag_from
from web.view import UserView, MessageView
import functools

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db_session = get_db_session()
        try:
            g.user = db_session.query(User).filter(User.id == user_id).one()
        except NoResultFound:
            session.pop('user_id')
            g.user = None


@auth.route('/register', methods=('POST',))
@swag_from({
    'tags': ['Auth'],
    'parameters': [
        {
            'name': 'email',
            'in': 'formData',
            'description': 'New user email. Empty for an anonymous user.',
            'required': False,
            'type': 'string'
        },
        {
            'name': 'pwd',
            'in': 'formData',
            'description': 'Set a password. Required for a registered user.',
            'required': False,
            'type': 'string'
        },
    ],
    'responses': {
        200: {
            'description': 'Successfully registered',
            'schema': UserView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def register():
    email = request.form.get('email')
    user = User(email=email)

    if email is not None:
        pwd = request.form.get('pwd')
        password_service = PasswordService(user)
        if not password_service.is_valid(pwd):
            return bad_request('Please choose a different password')
        password_service.set_password(pwd)

    db_session = get_db_session()
    db_session.add(user)
    db_session.commit()
    session['user_id'] = user.id

    return UserView().dump(user)


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
        {
            'name': 'pwd',
            'in': 'formData',
            'description': 'Password',
            'required': True,
            'type': 'string'
        },
    ],
    'responses': {
        200: {
            'description': 'Successfully logged int',
            'schema': UserView
        },
        400: {
            'description': 'Bad request',
            'schema': MessageView
        }
    }
})
def login():
    email = request.form['email']
    db_session = get_db_session()
    try:
        user: User = db_session.query(User).filter(User.email == email).one()
    except NoResultFound:
        return bad_request('No user found')

    password_service = PasswordService(user)
    if not password_service.check_password(request.form['pwd']):
        return bad_request('Wrong password')

    session.clear()
    session['user_id'] = user.id
    return UserView().dump(user)


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
    return ok_request('Logged out')


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
