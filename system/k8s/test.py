import urllib3
from pprint import pprint
from kubernetes import client
from os import path
import yaml


class K8sApi(object):
    def __init__(self):
        # self.config = config.kube_config.load_kube_config()
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.configuration = client.Configuration()
        self.configuration.host = "https://192.168.100.111:6443"
        self.configuration.api_key[
            'authorization'] = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJkYXNoYm9hcmQtYWRtaW4tdG9rZW4tZnhyNHYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGFzaGJvYXJkLWFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiYmI1ZjVjMjAtZDNiOS00MDUzLWJkMjMtOTBhNjlmNGNlNzhlIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmRhc2hib2FyZC1hZG1pbiJ9.lPv9QAexhmKol3AJzZ5oesf9JKF-mQCsVgho9mUqcyMzMxVqmw9_1Z1Xl8cewHMI4nyUf4NxTqDeIzDAPhzvVoxz60oln9NXtB-qZT7uRclsCH9ItPDrmgvzOHkEakH3CXnEX2KjtlxSq3rXdoW_bG9iXDPjIoXzYYQUbValhA-kmAi4o8teLl8vuyj_AWfWywdRlxCXs-0IfMFU7SpHqGNWN7VxHG9Wk9ArSMh88NcFk-wx0th0H2v1XOiMznOFoEyQYIPAtHWvIOwx0-p-k6kxQ_ZWwzBBy4fhAjWu0wvOGOfzjuA_N4yr1yDMPUts-r9Xptjwd_xTV1uc2hnekA'
        self.configuration.verify_ssl = False
        self.k8s_apps_v1 = client.AppsV1Api(client.ApiClient(self.configuration))
        self.Api_Instance = client.CoreV1Api(client.ApiClient(self.configuration))
        self.Api_Instance_Extensions = client.ExtensionsV1beta1Api(client.ApiClient(self.configuration))

    ####################################################################################################################

    def list_deployment(self, namespace="default"):
        api_response = self.k8s_apps_v1.list_namespaced_deployment(namespace)
        return api_response

    def read_deployment(self, name="nginx-deployment", namespace="default"):
        api_response = self.k8s_apps_v1.read_namespaced_deployment(name, namespace)
        return api_response

    def create_deployment(self, file="deploy-nginx.yaml"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            resp = self.k8s_apps_v1.create_namespaced_deployment(
                body=dep, namespace="default")
            return resp

    def replace_deployment(self, file="deploy-nginx.yaml", name="nginx-deployment", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            resp = self.k8s_apps_v1.replace_namespaced_deployment(name, namespace,
                                                                  body=dep)
            return resp

    def delete_deployment(self, name="nginx-deployment", namespace="default"):
        api_response = self.k8s_apps_v1.delete_namespaced_deployment(name, namespace)
        return api_response

    ####################################################################################################################

    def list_namespace(self):
        api_response = self.Api_Instance.list_namespace()
        return api_response

    def read_namespace(self, name="default"):
        api_response = self.Api_Instance.read_namespace(name)
        return api_response

    def create_namespace(self, file="pod-nginx.yaml"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance.create_namespace(body=dep)
            return api_response

    def replace_namespace(self, file="pod-nginx.yaml", name="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
        api_response = self.Api_Instance.replace_namespace(name, body=dep)
        return api_response

    def delete_namespace(self, name="default"):
        api_response = self.Api_Instance.delete_namespace(name)
        return api_response

    ####################################################################################################################

    def list_node(self):
        api_response = self.Api_Instance.list_node()
        data = {}
        for i in api_response.items:
            data[i.metadata.name] = {"name": i.metadata.name,
                                     "status": i.status.conditions[-1].type if i.status.conditions[
                                                                                   -1].status == "True" else "NotReady",
                                     "ip": i.status.addresses[0].address,
                                     "kubelet_version": i.status.node_info.kubelet_version,
                                     "os_image": i.status.node_info.os_image,
                                     }
        return data

    def list_pod(self):
        api_response = self.Api_Instance.list_pod_for_all_namespaces()
        data = {}
        for i in api_response.items:
            data[i.metadata.name] = {"ip": i.status.pod_ip, "namespace": i.metadata.namespace}
        return data

    def read_pod(self, name="nginx-pod", namespace="default"):
        api_response = self.Api_Instance.read_namespaced_pod(name, namespace)
        return api_response

    def create_pod(self, file="pod-nginx.yaml", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance.create_namespaced_pod(namespace, body=dep)
            return api_response

    def replace_pod(self, file="pod-nginx.yaml", name="nginx-pod", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance.replace_namespaced_pod(name, namespace, body=dep)
        return api_response

    def delete_pod(self, name="nginx-pod", namespace="default"):
        api_response = self.Api_Instance.delete_namespaced_pod(name, namespace)
        return api_response

    ####################################################################################################################

    def list_service(self):
        api_response = self.Api_Instance.list_service_for_all_namespaces()
        return api_response

    def read_service(self, name="", namespace="default"):
        api_response = self.Api_Instance.read_namespaced_service(name, namespace)
        return api_response

    def create_service(self, file="service-nginx.yaml", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance.create_namespaced_service(namespace, body=dep)
            return api_response

    def replace_service(self, file="pod-nginx.yaml", name="hequan", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance.replace_namespaced_service(name, namespace, body=dep)
        return api_response

    def delete_service(self, name="hequan", namespace="default"):
        api_response = self.Api_Instance.delete_namespaced_service(name, namespace)
        return api_response

    ####################################################################################################################

    def list_ingress(self):
        api_response = self.Api_Instance_Extensions.list_ingress_for_all_namespaces()
        return api_response

    def read_ingress(self, name="", namespace="default"):
        api_response = self.Api_Instance_Extensions.read_namespaced_ingress(name, namespace)
        return api_response

    def create_ingress(self, file="ingress-nginx.yaml", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance_Extensions.create_namespaced_ingress(namespace, body=dep)
            return api_response

    def replace_ingress(self, name="", file="ingress-nginx.yaml", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.Api_Instance_Extensions.replace_namespaced_ingress(name=name, namespace=namespace,
                                                                                   body=dep)
            return api_response

    def delete_ingress(self, name="hequan", namespace="default"):
        api_response = self.Api_Instance_Extensions.delete_namespaced_ingress(name, namespace)
        return api_response

    #####################################################################################################################

    def list_stateful(self):
        api_response = self.k8s_apps_v1.list_stateful_set_for_all_namespaces()
        return api_response

    def read_stateful(self, name="nginx-deployment", namespace="default"):
        api_response = self.k8s_apps_v1.read_namespaced_stateful_set(name, namespace)
        return api_response

    def create_stateful(self, file="deploy-nginx.yaml"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            resp = self.k8s_apps_v1.create_namespaced_stateful_set(
                body=dep, namespace="default")
            return resp

    def replace_stateful(self, file="deploy-nginx.yaml", name="nginx-deployment", namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            resp = self.k8s_apps_v1.replace_namespaced_stateful_set(name, namespace,
                                                                    body=dep)
            return resp

    def delete_stateful(self, name="nginx-deployment", namespace="default"):
        api_response = self.k8s_apps_v1.delete_namespaced_stateful_set(name, namespace)
        return api_response

    ####################################################################################################################


if __name__ == '__main__':
    def test():
        obj = K8sApi()
        ret = obj.list_deployment()
        pprint(ret)


    test()
