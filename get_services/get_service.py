from kubernetes import client, config
from loguru import logger


def get_services(namespace: str = "default") -> list:

    logger.info(f"namespace: {namespace}")

    """获取 k8s 中指定的命名空间下的所有的 Service"""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    services = v1.list_namespaced_service(namespace=namespace)
    return [service.metadata.name for service in services.items]
