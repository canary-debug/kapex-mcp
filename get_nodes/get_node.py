from kubernetes import client, config
from loguru import logger


def get_nodes(name: str):

    logger.info(f"name: {name}")

    """获取 k8s 所有 node"""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    nodes = v1.list_node()
    return nodes.items
