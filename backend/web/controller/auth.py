from flask import Blueprint, request, g
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError

from core.facade.user import UserFacade
from core.model.user import User
from web.controller.util import bad_request, TOKEN_SECURITY, BAD_REQUEST_SCHEMA, error_into_message
from web.service.database import get_db_session
from sqlalchemy.orm.exc import NoResultFound
from flasgger import swag_from

from core.service.auth.token import TokenService
from web.service.injector import get_injector, inject
from web.view import UserView, UserAndTokenView
import functools

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.route('/register', methods=('POST',))
@error_into_message
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
    facade = inject(UserFacade)
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    user = facade.register(email, pwd)
    token = facade.get_token(user)
    try:
        get_db_session().commit()
    except IntegrityError:
        return bad_request('This email is already registered')
    return UserAndTokenView().dump({'user': user, 'token': token})


@auth.route('/login', methods=('POST',))
@error_into_message
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
    facade = inject(UserFacade)
    email = request.form['email']
    pwd = request.form['pwd']
    user = facade.login(email, pwd)
    token = facade.get_token(user)
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
        injector = get_injector()
        token_service = injector.get(TokenService)
        try:
            g.user = token_service.decode_token(token)
        except NoResultFound:
            return bad_request('User not found')
        except ExpiredSignatureError:
            return bad_request('Token expired')
        except InvalidTokenError:
            return bad_request('Invalid token')
        injector.provide(User, g.user)
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
