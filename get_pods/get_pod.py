from kubernetes import client, config
from loguru import logger


def get_pods(namespace: str = "default") -> list:

    logger.info(f"namespace: {namespace}")

    """获取 k8s 中指定的命名空间下的所有的 Pod"""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace)
    return [pod.metadata.name for pod in pods.items]