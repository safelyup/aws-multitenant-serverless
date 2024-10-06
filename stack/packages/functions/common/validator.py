import json
import jsonpickle
import simplejson
from enum import Enum
from aws_lambda_powertools.utilities.validation import validate
from functools import wraps

def input(schema):
    '''Decorator for validating api endpoint input'''
    def decorator(func):
        @wraps(func)
        def f_wrapper(*args, **kwargs):
            try:
                if args[0].get('body', None) is None:
                    raise Exception("")
                validate(event=args[0], schema=schema, envelope="powertools_json(body)")
            except Exception as e:
                return resp_failure("invalid input")
            return func(*args, **kwargs)
        return f_wrapper
    return decorator

class StatusCodes(Enum):
    SUCCESS   = 200
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_INPUT = 400

def resp_failure(message):
    return {
        "statusCode": StatusCodes.BAD_INPUT.value,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": json.dumps({
            "message": message
        }),
    }

def resp_success(message):
    return {
        "statusCode": StatusCodes.SUCCESS.value,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": json.dumps({
            "message": message
        }),
    }

def resp_forbidden():
    return {
        "statusCode": StatusCodes.FORBIDDEN.value,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": json.dumps({
            "message": "Forbidden"
        }),
    }

def resp_notfound(message):
    return {
        "statusCode": StatusCodes.NOT_FOUND.value,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": json.dumps({
            "message": message
        }),
    }

def resp(inputObject):
    # TODO: gzip compression
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers" : "Content-Type, Origin, X-Requested-With, Accept, Authorization, Access-Control-Allow-Methods, Access-Control-Allow-Headers, Access-Control-Allow-Origin",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT"
        },
        "body": encode_to_json_object(inputObject),
    }

def encode_to_json_object(inputObject):
    jsonpickle.set_encoder_options('simplejson', use_decimal=True, sort_keys=True)
    jsonpickle.set_preferred_backend('simplejson')
    return jsonpickle.encode(inputObject, unpicklable=False, use_decimal=True)
