


template_request = {
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
      "CountryCode": "GB",
      "UniqueIdentifier": "TestRPS"
    },
    "TransactionIdentifier": "c02358b2-76cf-4ba4-a8eb-f6436ccaea2e",
    "Timestamp": "2015-09-01T12:00:00.000000Z",
    "Version": {
      "ETSIVersion": "V1.13.1",
      "NationalProfileOwner": "XX",
      "NationalProfileVersion": "v1.0"
    }
  },
  "Payload": {
    "RequestPayload": {
      "ActionRequests": {
        "ActionRequest": [
          {
            "ActionIdentifier": 0,
            "CREATE": {
              "HI1Object": {
                "@xsi:type": "{http://uri.etsi.org/03120/common/2020/09/Task}LDTaskObject",
                "ObjectIdentifier": "2b36a78b-b628-416d-bd22-404e68a0cd36",
                "CountryCode": "XX",
                "OwnerIdentifier": "ACTOR01",
                "AssociatedObjects": {
                  "AssociatedObject": [
                    "7dbbc880-8750-4d3c-abe7-ea4a17646045"
                  ]
                },
                "task:Reference": "XX-ACTOR01-1234",
                "task:RequestDetails": {
                  "task:Type" : {
                      "common:Owner" : "ETSI",
                      "common:Name" : "TS103976RequestType",
                      "common:Value" : "VINtoCommsID"
                  },
                  "task:StartTime": "2019-09-30T12:00:00Z",
                  "task:EndTime": "2019-12-30T12:00:00Z",
                  "task:RequestValues": {
                    "task:RequestValue": [
                      {
                        "task:FormatType": {
                          "task:FormatOwner": "ETSI",
                          "task:FormatName": "VIN"
                        },
                        "task:Value": "1G9Y817H34LSP7293"
                      }
                    ]
                  }
                }
              }
            }
          }]
      }
    }
  }
}

print (template_request)