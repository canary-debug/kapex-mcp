from kubernetes import client, config
from loguru import logger


def update_images(resource_type: str, name: str, new_image: str, namespace: str = "default"):
    logger.info(f"resource_type: {resource_type}")
    logger.info(f"new_image: {new_image}")
    logger.info(f"name: {name}")
    logger.info(f"namespace: {namespace}")
    """更新指定资源类型的镜像"""
    config.load_kube_config()
    v1 = client.AppsV1Api()

    if resource_type == "deployment" or resource_type == "Deployment":
        resource = v1.read_namespaced_deployment(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_deployment
    elif resource_type == "daemonset" or resource_type == "DaemonSet":
        resource = v1.read_namespaced_daemon_set(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_daemon_set
    elif resource_type == "statefulset" or resource_type == "StatefulSet":
        resource = v1.read_namespaced_stateful_set(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_stateful_set
    elif resource_type == "job" or resource_type == "Job":
        resource = v1.read_namespaced_job(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_job
    elif resource_type == "cronjob" or resource_type == "CronJob":
        resource = v1.read_namespaced_cron_job(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_cron_job
    elif resource_type == "replicaset" or resource_type == "ReplicaSet":
        resource = v1.read_namespaced_replica_set(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_replica_set
    elif resource_type == "pod" or resource_type == "Pod":
        resource = v1.read_namespaced_pod(name=name, namespace=namespace)
        update_function = v1.patch_namespaced_pod
    else:
        raise ValueError(f"不支持的资源类型: {resource_type}")

    # 更新镜像
    for container in resource.spec.template.spec.containers:
        container.image = new_image

    # 应用更新
    update_function(name=name, namespace=namespace, body=resource)
    return resource