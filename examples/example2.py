import os
import uuid
from os.path import expanduser
from k8s.client.core_v1_api import CoreV1Api


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = expanduser("~/.config/gcloud/legacy_credentials/a.mostapha@obytes.com/adc.json")


def main():

    client = CoreV1Api()

    name = 'nginx-deployment-' + str(uuid.uuid4())

    data = '''
    apiVersion: extensions/v1beta1
    kind: Deployment
    metadata:
      name: %s
      labels:
        app: nginx
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: nginx
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
          - name: nginx
            image: nginx:1.7.9
            ports:
            - containerPort: 80            
    '''

    print("Create deployment in default namespaces :")
    response = client.submit_deployment(data=data % name)
    print("{}".format(response))


if __name__ == '__main__':
    main()
