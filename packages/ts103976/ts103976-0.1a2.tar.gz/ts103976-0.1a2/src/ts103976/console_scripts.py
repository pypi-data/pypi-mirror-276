import argparse
import sys
import json

from .lea import LEA
from .rps import RPS


def lea_console():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--sendercc", default="XX", help="Sender Country Code")
    parser.add_argument("-u", "--senderid", default="SENDER", help="Sender Unique ID")
    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID")
    parser.add_argument("-t", "--taskref", default="XX-1-234", help="Task Reference (LDID)")
    parser.add_argument("-v", "--vin", default="1G9Y817H34LSP7293", help="VIN to query")
    parser.add_argument("-d", "--deliveryurl", default="https://localhost", help="Delivery URL")
    
    args = parser.parse_args()

    lea = LEA(args.sendercc, args.senderid, args.deliveryurl)
    json_doc = lea.generate_vin_to_comms_id(args.receivercc, args.receiverid, args.taskref, args.vin)
    print(json.dumps(json_doc))


def rps_console():
    parser = argparse.ArgumentParser()

    parser.add_argument("-r", "--receivercc", default="XX", help="Receiver Country Code")
    parser.add_argument("-i", "--receiverid", default="RECEIVER", help="Receiver Unique ID")
    parser.add_argument("-a", "--allowanyid", default=False, help="Parse messages to any Receiver ID")
    parser.add_argument('-j', '--input', type=argparse.FileType('r'), default=sys.stdin, help="Path to input file (if absent, stdin is used)")
    
    args = parser.parse_args()
    instance_doc = json.loads(args.input.read())
    args.input.close()

    rps = RPS(args.receivercc, args.receiverid, args.allowanyid)
    response = rps.respond_to(instance_doc)
    print(response)
