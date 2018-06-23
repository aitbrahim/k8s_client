import os
from os.path import expanduser
from k8s.client.core_v1_api import CoreV1Api


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = expanduser("~/.config/gcloud/legacy_credentials/a.mostapha@obytes.com/adc.json")


def main():

    client = CoreV1Api()
    print("Listing pods for all namespace :")
    resp = client.list_pod_for_all_namespaces()

    for i in resp.get('items'):
        print("%s\t%s\t%s" %
              (i['status']['podIP'], i['metadata']['namespace'], i['metadata']['name']))


if __name__ == '__main__':
    main()
