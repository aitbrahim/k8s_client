from k8s.client.core_v1_api import CoreV1Api
from k8s.config.configuration import load_config


def main():

    load_config()
    import pdb;pdb.set_trace()

    client = CoreV1Api()
    print("Listing pods for all namespace :")
    client.list_pod_for_all_namespaces()




if __name__ == '__main__':
    main()
