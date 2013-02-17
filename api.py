import functools
import requests
import logging




from config import APP_ID

class MASError(Exception):
    """
    Base Exception thrown by the MAS Object when there is an error with the
    API.
    """

class MASRespoinse(object):
    """
    Response from a MAS Request
    """

class MAS(object):
    base_url = "http://academic.research.microsoft.com/json.svc/search"

    error_messages = (
        "The request is succeeded",
        "The AppID has no access rights to the MAS API",
        "Parameters are invalid",
        "The MAS service is temporarily unavailable",
        "The search condition is not supported yet",
    )

    result_objects = (
        "Author",
        "Publication",
        "Conference",
        "Journal",
        "Domain",
        "Organization",
        "Keyword",
    )

    def __getattr__(self, k):
        try:
            print "1111111"
            return object.__getattr__(self, k)
        except AttributeError:
            k = k.capitalize()
            assert k in self.result_objects

            def function(obj_type, **params):
                params['ResultObjects'] = obj_type
                return self.request(params)

            return functools.partial(function, k)

    def __init__(self, app_id):
        self.app_id = app_id

    def request(self, params):
        params['AppId'] = self.app_id
        print ("PARAMS {0}").format(params) # FIXME logging
        result_objects = params['ResultObjects']
        resp = requests.request("GET", self.base_url, params=params)
        try:
           # resp_data = resp.json['d']
           resp_data = resp.json()['d']
           #pprint.pprint(resp_data['d'])
        except:
            print ("The json response has no 'd' key")
            print ("Response TEXT {0}").format(resp.text)
            print ("Response JSON {0}").format(resp.json)
            raise

        # Check that the request is successfull
        try:
            result_code = resp_data['ResultCode']
            assert result_code == 0
        # Print meaningful error message
        except AssertionError:
            print (self.error_messages[result_code])
        return resp_data[result_objects]

class MASFacade(object):
    def __init__(self, app_id):
        self.api = MAS(app_id)

    def author(self, author_id):
        resp = self.api.author({"AuthorID": author, "StartIdx": 1, "EndIdx": 1})
        try:
            return resp['Author']['Result'][0]
        except IndexError:
            print("No Author found with the specified AuthorID {0}").fortmat(author_id)
            raise
        except: # KeyError should never happen
            print ("Unexplainable Error")
            raise

api = MAS(APP_ID)
