import json

class JsonResponses(object):
    
    @classmethod
    def response(cls, resp_struct):
        return json.dumps(resp_struct)
    
    @classmethod
    def server_error(cls, msg):
        return cls.response({'code': 1,
               'msg': 'There was an internal server error. Please contact the system administrator for assistance.'})
    
    @classmethod
    def already_logged_in(cls, user):
        return cls.response({'code':10,
               'msg': "You are already logged in as %s. Please log out to create a new account."%(user.username)})
    
    @classmethod
    def required_field_missing(cls, field):
        return cls.response({'code':20,
               'msg': "A value for the field [%s] is required but not present in your request."%field})
    
    @classmethod
    def invalid_argument_value(cls, field, value):
        return cls.response({'code':30,
               'msg': "You have provided an invalid value (%s) for the [%s] field."%(value, field)})
    
    @classmethod
    def account_exists(cls, user):
        return cls.response(
            {
                'code': 40,
                'msg': "An account already exists for the user %s"%user
            }
        )
        
    @classmethod
    def invalid_login(cls):
        return cls.response(
            {
                'code': 50,
                'msg': "Invalid username or password. Please try again."
            }
        )

    @classmethod
    def page_not_authorized(cls):
        return cls.response(
            {
                'code': 60,
                'msg': 'You must be logged in to access that page.'
            }
        )

    @classmethod
    def ajax_not_authorized(cls):
        return cls.response(
            {
                'code': 70,
                'msg': 'You must be logged in to access that api.'
            }
        )
    
    @classmethod
    def oauth_get_url_response(cls, url):
        return cls.response(
            {
                'code': 0,
                'msg': 'Url to authorize access to account',
                'url': url
            }
        )
    
    @classmethod
    def oauth_request_response(cls, request_token, request_auth_url):
        return cls.response(
            {
                'code': 80,
                'rt': request_token,
                'rau': request_auth_url
            }
        )
    
    @classmethod
    def as_is(cls, data):
        return cls.response(data)
    
    @classmethod
    def one_object(cls, obj_data):
        return cls.response(
            {
                'code': 5,
                'data': obj_data
            }
        )
    
    @classmethod
    def object_created(cls, obj_name, obj_data):
        return cls.response(
            {
                'code': 0,
                'msg': "%s created successfully"%obj_name,
                'data': obj_data
            }
        )
    
    @classmethod
    def object_count(cls, count):
        return cls.response(
            {
                'code': 1,
                'count': count
             }
        )
    
    @classmethod
    def object_list(cls, olist):
        return cls.response(
            {
                'code': 2,
                'list':olist
            }
        )
    
    @classmethod
    def ok(cls, msg=''):
        return cls.response(
            {
                'code': 0,
                'msg': msg
            }
        )
    
    @classmethod
    def fail(cls, msg):
        return cls.response(
            {
                'code': 90,
                'msg': msg
            }
        )