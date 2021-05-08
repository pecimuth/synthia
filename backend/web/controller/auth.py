from flask import Blueprint, request, g
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.exc import IntegrityError

from core.facade.user import UserFacade
from core.model.user import User
from core.service.auth.password import PasswordService
from web.controller.util import bad_request, TOKEN_SECURITY, BAD_REQUEST_SCHEMA, error_into_message, validate_json, \
    patch_from_json, EMAIL_ALREADY_REGISTERED
from web.service.database import get_db_session
from sqlalchemy.orm.exc import NoResultFound
from flasgger import swag_from

from core.service.auth.token import TokenService
from web.service.injector import get_injector, inject
from web.view import UserView, UserAndTokenView, UserWrite
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
    db_session = get_db_session()
    facade = inject(UserFacade)
    email = request.form.get('email')
    pwd = request.form.get('pwd')
    user = facade.register(email, pwd)
    try:
        db_session.flush()
        token = facade.get_token(user)
        db_session.commit()
    except IntegrityError:
        return bad_request(EMAIL_ALREADY_REGISTERED)
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


@auth.route('/user/<id>', methods=('PATCH',))
@login_required
@validate_json(UserWrite)
@error_into_message
@swag_from({
    'tags': ['Auth'],
    'security': TOKEN_SECURITY,
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'description': 'User ID',
            'required': True,
            'type': 'integer'
        },
        {
            'name': 'user',
            'in': 'body',
            'description': 'User content',
            'required': True,
            'schema': UserWrite
        }
    ],
    'responses': {
        200: {
            'description': 'Return the patched user and issue a new token',
            'schema': UserAndTokenView
        },
        400: BAD_REQUEST_SCHEMA
    }
})
def patch_user(id):
    if g.user.id != int(id):
        return bad_request('Cannot patch user other than self')
    patch_from_json(g.user, 'email')
    pwd_attr = 'pwd'
    if pwd_attr in request.json:
        password_service = PasswordService(g.user)
        password_service.set_password(request.json[pwd_attr])
    facade = inject(UserFacade)
    token = facade.get_token(g.user)
    try:
        get_db_session().commit()
    except IntegrityError:
        return bad_request(EMAIL_ALREADY_REGISTERED)
    return UserAndTokenView().dump({'user': g.user, 'token': token})
