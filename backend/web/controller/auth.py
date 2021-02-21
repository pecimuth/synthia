from flask import Blueprint, request, g, current_app
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError

from core.service.password import PasswordService
from web.controller.util import bad_request, TOKEN_SECURITY, BAD_REQUEST_SCHEMA
from web.service.database import get_db_session
from core.model.user import User
from sqlalchemy.orm.exc import NoResultFound
from flasgger import swag_from

from web.service.token import TokenService
from web.view import UserView, UserAndTokenView
import functools

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


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
            'schema': UserAndTokenView
        },
        400: BAD_REQUEST_SCHEMA
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
    try:
        db_session.commit()
    except IntegrityError:
        return bad_request('This email is already registered')

    token_service = TokenService(current_app.config['SECRET_KEY'], user)
    token = token_service.create_token()

    return UserAndTokenView().dump({'user': user, 'token': token})


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
            'description': 'Successfully logged in',
            'schema': UserAndTokenView
        },
        400: BAD_REQUEST_SCHEMA
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

    token_service = TokenService(current_app.config['SECRET_KEY'], user)
    token = token_service.create_token()

    return UserAndTokenView().dump({'user': user, 'token': token})


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return bad_request('No authorization header')
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return bad_request('Bad bearer token format')
        token_service = TokenService(current_app.config['SECRET_KEY'])
        try:
            g.user = token_service.decode_token(token)
        except NoResultFound:
            return bad_request('User not found')
        except ExpiredSignatureError:
            return bad_request('Token expired')
        except InvalidTokenError:
            return bad_request('Invalid token')
        return view(**kwargs)
    return wrapped_view


@auth.route('/user')
@login_required
@swag_from({
    'tags': ['Auth'],
    'security': TOKEN_SECURITY,
    'responses': {
        200: {
            'description': 'Return logged in user',
            'schema': UserView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def get_user():
    return UserView().dump(g.user)
