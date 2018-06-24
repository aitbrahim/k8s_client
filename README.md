# Kubernetes Python Client

Python client for the [kubernetes](http://kubernetes.io/) API.

## Installation

From source:

```
git clone https://github.com/aitbrahim/k8s_client

python setup.py install
```

## Example

list all pods:

```python

client = CoreV1Api()

print("Listing pods for all namespace :")
resp = client.list_pods()

for i in resp.get('items'):
    try:
        print("%s\t%s\t%s" %
              (i['status']['podIP'], i['metadata']['namespace'], i['metadata']['name']))
    except KeyError:
        continue
```
