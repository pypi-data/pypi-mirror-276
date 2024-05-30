import logging
from copy import deepcopy
from datetime import datetime
from uuid import uuid4

from validator import TS103120Validator
from create import template_request

from rps import RPS

from rich import print as rprint

logging.basicConfig(level=logging.WARN)



template_response = {
  "@xmlns": "http://uri.etsi.org/03120/common/2019/10/Core",
  "@xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
  "@xmlns:common": "http://uri.etsi.org/03120/common/2016/02/Common",
  "@xmlns:task": "http://uri.etsi.org/03120/common/2020/09/Task",
  "Header": {
    "SenderIdentifier": {
      "CountryCode": "XX",
      "UniqueIdentifier": "ACTOR01"
    },
    "ReceiverIdentifier": {
      "CountryCode": "XX",
      "UniqueIdentifier": "ACTOR02"
    },
    "TransactionIdentifier": "c02358b2-76cf-4ba4-a8eb-f6436ccaea2e",
    "Timestamp": "2015-09-01T12:00:00.000000Z",
    "Version": {
      "ETSIVersion": "V1.13.1",
      "NationalProfileOwner": "XX",
      "NationalProfileVersion": "v1.0"
    }
  },
  "Payload" : {
      "ResponsePayload": {
        "ErrorInformation" : {
            "ErrorCode" : 3007,
            "ErrorDescription" : ""
        }          
      }
  }
}

v = TS103120Validator("../tcli/")
junk_input = {"wrong" : "won't work"}

def respond_to (req : dict):
    errors = v.validate(req)
    if len(errors) > 0:
        print ("Request failed validation")
        error_str = ""
        for error in errors:
            print(error)
            error_str += str(error)
        response = deepcopy(template_response)
        d = datetime.now(datetime.now().astimezone().tzinfo)
        response['Header']['Timestamp'] = d.isoformat()
        response['Header']['TransactionIdentifier'] = uuid4
        response['Payload']['ResponsePayload']['ErrorInformation']['ErrorDescription'] = error_str
        return response
    response = deepcopy(template_response)
    response['Header'] = deepcopy(req['Header'])
    d = datetime.now(datetime.now().astimezone().tzinfo)
    response['Header']['Timestamp'] = d.isoformat()
    response['Payload'] = {}
    response['Payload']['ResponsePayload'] = {
        "ActionResponses" : {
            "ActionResponse" : [
                {
                    "ActionIdentifier" : 0,
                    "CREATEResponse" : {
                        "Identifier" : req['Payload']['RequestPayload']['ActionRequests']['ActionRequest'][0]['CREATE']['HI1Object']['ObjectIdentifier']
                    }
                }
            ]
        }
    }
    print ("Request passed validation")
    return response




# r = respond_to(template_request)
# r_errors = v.validate(r)

rps = RPS( ReceiverCC="GB", ReceiverID="TestRPS")
j = rps.respond_to(template_request)
rprint(j)