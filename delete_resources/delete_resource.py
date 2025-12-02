from kubernetes import client, config
from loguru import logger


def delete_resources(resource_type: str, name: str, namespace: str = "default"):

    logger.info(f"Deleting Resource: {name}")
    logger.info(f"name: {name}")
    logger.info(f"Namespace: {namespace}")

    """删除指定资源类型的资源"""
    config.load_kube_config()
    v1 = client.AppsV1Api()

    if resource_type == "deployment" or resource_type == "Deployment":
        resource = v1.delete_namespaced_deployment(name=name, namespace=namespace)
    elif resource_type == "daemonset" or resource_type == "DaemonSet":
        resource = v1.delete_namespaced_daemon_set(name=name, namespace=namespace)
    elif resource_type == "statefulset" or resource_type == "StatefulSet":
        resource = v1.delete_namespaced_stateful_set(name=name, namespace=namespace)
    elif resource_type == "job" or resource_type == "Job":
        resource = v1.delete_namespaced_job(name=name, namespace=namespace)
    elif resource_type == "cronjob" or resource_type == "CronJob":
        resource = v1.delete_namespaced_cron_job(name=name, namespace=namespace)
    elif resource_type == "replicaset" or resource_type == "ReplicaSet":
        resource = v1.delete_namespaced_replica_set(name=name, namespace=namespace)
    elif resource_type == "pod" or resource_type == "Pod":
        resource = v1.delete_namespaced_pod(name=name, namespace=namespace)
    else:
        raise ValueError(f"不支持的资源类型: {resource_type}")
    return resource


def delete_service(name: str, namespace: str = "default"):
    logger.info(f"Deleting Service: {name}")
    logger.info(f"name: {name}")
    logger.info(f"Namespace: {namespace}")

    """删除指定 Service"""
    config.load_kube_config()
    v1 = client.CoreV1Api()
    resource = v1.delete_namespaced_service(name=name, namespace=namespace)
    return resource