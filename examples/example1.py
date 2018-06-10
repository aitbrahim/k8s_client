import os
from os.path import expanduser
from k8s.client.core_v1_api import CoreV1Api


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = expanduser("~/.config/gcloud/legacy_credentials/a.mostapha@obytes.com/adc.json")


def main():

    client = CoreV1Api()
    print("Listing pods for all namespace :")
    client.list_pod_for_all_namespaces()


if __name__ == '__main__':
    main()
