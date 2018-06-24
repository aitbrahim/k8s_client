import os
from os.path import expanduser
from k8s.client.core_v1_api import CoreV1Api


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = expanduser("~/.config/gcloud/legacy_credentials/a.mostapha@obytes.com/adc.json")


def display(data):
    for i in data.get('items'):
        try:
            print("%s\t%s\t%s" %
                  (i['status']['podIP'], i['metadata']['namespace'], i['metadata']['name']))
        except KeyError:
            continue


def main():

    client = CoreV1Api()

    print("Listing pods for all namespace :")
    resp = client.list_pods()
    display(resp)

    print("Listing pods for specific namespace :")
    resp = client.list_pods(namespace='fugoki-monolith')
    display(resp)


if __name__ == '__main__':
    main()
