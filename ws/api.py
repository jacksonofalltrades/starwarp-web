import uuid
import json
from thirdparty.ua_parser import user_agent_parser
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponse, Http404
from armutils.jsonresponse import JsonResponses
from serverapp.api.models import User, Device, DeviceSession

class ApiMessageList(object):
    def __init__(self):
        self.msgs = []
        
    def add(self, code, msg):
        self.msgs.append({'code':code, 'msg':msg})
                
    def get(self):
        return self.msgs
    
class ApiBase(object):
    OK = 200
    BADREQ = 400
    UNAUTH = 403
    SERVERR = 500
    
    ERRCODE_UNKNOWN_METHOD = -10
    ERRCODE_INVALID_SESSION = -20
    ERRCODE_SESSION_INTEGRITY = -30
    ERRCODE_UNKNOWN_DEVICE = -40
    ERRCODE_MISSING_TOKEN = -50
    ERRCODE_ALREADY_LOGGED_IN = -60
    ERRCODE_AUTH_FAILED = -70
    ERRCODE_MISSING_FIELDS = -80
    ERRCODE_SESSION_NOT_FOUND = -90
    ERRCODE_DEVICE_INTEGRITY = -100
    ERRCODE_FIELD_ERR = -120
    ERRCODE_NO_UNASS_CLIENT = -130
    
    KEY_SESS = 'sess'
    KEY_USERNAME = 'u'
    KEY_PASSWORD = 'p'
    KEY_DEV_ID = 'd'
    KEY_SECTOKEN = 'sectoken'
    KEY_ACT_LIST = 'acts'
                
    @classmethod
    def create_msglist(cls, code=None, msg=None):
        msglist = ApiMessageList()
        if code and msg:
            msglist.add(code, msg)
        return msglist

    @classmethod
    def create_field_errors(cls, field_err_msglist):
        msglist = cls.create_msglist()
        
        for msg in field_err_msglist:
            msglist.add(ApiBase.ERRCODE_FIELD_ERR, msg)
            
        return msglist
    
    @classmethod
    def resp(cls, status, msglist=None, **otherargs):
        r = {'status': status}
        if msglist:
            r['msgs'] = msglist
        for key, val in otherargs.items():
            r[key] = val
        return r
    
    @classmethod
    def gen_sectoken(cls):
        sectoken = uuid.uuid4()
        return sectoken.get_hex()

    @classmethod
    def validate_required(cls, inputdata, req_keylist):
        notfound = []
        for key in req_keylist:
            if key not in inputdata:
                notfound.append(key)
        return notfound
    
    @classmethod
    def create_device(cls, request, user, dev_uid):
        user_agent_str = request.META['HTTP_USER_AGENT']
        result_dict = user_agent_parser.Parse(user_agent_str)
        ua_os = result_dict['os']['family']
        
        major = result_dict['os']['major']
        minor = result_dict['os']['minor']
        if major and minor:
            ua_osver = "%s.%s"%(major, minor)
        else:
            ua_osver = 'n/a'
        
        device = Device(user=user, device_unique_id=dev_uid, os=ua_os, os_version=ua_osver, user_agent=user_agent_str)
        device.save()
        return device
    
    # Returns tuple of (status code, response json, structured input)
    # If status code is not OK, response json is present and structured input is None
    # Otherwise, response json is None and structured input is present
    @classmethod
    def initialize(cls, request, requires_auth=True):
        inputdata = {}
        if request.method == 'POST':
            # Post data should always be json
            inputdata = json.loads(request.raw_post_data)
        elif request.method == 'GET':
            inputdata = request.REQUEST
        else:
            msglist = cls.create_msglist(cls.ERRCODE_UNKNOWN_METHOD, "Invalid rest method.")
            return (cls.SERVERR, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
        
        # Check auth
        if requires_auth:
            # Look for required params for checking auth in input data
            sectoken = None
            dev_uid = None
            if cls.KEY_SECTOKEN in inputdata:
                sectoken = inputdata[cls.KEY_SECTOKEN]
            if cls.KEY_DEV_ID in inputdata:
                dev_uid = inputdata[cls.KEY_DEV_ID]
            
            if sectoken and dev_uid:
                # Try to find the device
                try:
                    device = Device.objects.get(device_unique_id=dev_uid)
                    # Try to find the existing session
                    try:
                        dev_sess = DeviceSession.objects.get(device=device, security_token=sectoken)
                        inputdata[cls.KEY_SESS] = dev_sess
                    except DeviceSession.DoesNotExist, dee:
                        logging.info("Could not find session for dev_uid=[%s] and sectoken=[%s]"%(dev_uid, sectoken))
                        msglist = cls.create_msglist(cls.ERRCODE_INVALID_SESSION, "Invalid session")
                        return (cls.UNAUTH, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
                    except MultipleObjectsReturned, me:
                        logging.error("Found multiple sessions for dev_uid=[%s] and sectoken=[%s]. This is bad-ditty-bad-bad. Fuck."%(dev_uid, sectoken))
                        msglist = cls.create_msglist(cls.ERRCODE_SESSION_INTEGRITY, "Internal server error validating your session. Please logout and log back in.")
                        return (cls.SERVERR, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
                except Device.DoesNotExist, ee:
                    logging.warn("Problem finding device for dev_uid=[%s]"%dev_uid)
                    msglist = cls.create_msglist(cls.ERRCODE_UNKNOWN_DEVICE, "Could not find session for specified device.")
                    return (cls.BADREQ, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
                except MultipleObjectsReturned, devmor:
                    logging.error("Found multiple devices for dev_uid=[%s]. This is bad-ditty-bad-bad. Fuck."%(dev_uid))
                    msglist = cls.create_msglist(cls.ERRCODE_DEVICE_INTEGRITY, "Internal server error validating your session. Please logout and log back in.")
                    return (cls.SERVERR, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
            else:
                logging.warn("Missing sectoken and/or dev_uid. Cannot attempt to validate session.")
                msglist = cls.create_msglist(cls.ERRCODE_MISSING_TOKEN, "Invalid login.")
                return (cls.BADREQ, JsonResponses.as_is(cls.resp(0, msglist=msglist.get())), None)
    
        return (cls.OK, None, inputdata)