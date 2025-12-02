from kubernetes import client, config
from loguru import logger


def create_all_resources(resource_type: str, name: str, image: str = "nginx:latest", namespace: str = "default", replicas: int = 1, port: int = 80, image_pull: str = "IfNotPresent"):

    logger.info(f"Creating Service: {name}")
    logger.info(f"Image: {image}")
    logger.info(f"Namespace: {namespace}")
    logger.info(f"replicas: {replicas}")
    logger.info(f"Port: {port}")
    logger.info(f"Image_pull: {image_pull}")

    """创建 k8s 所有资源类型"""
    if resource_type == "deployment" or resource_type == "Deployment":
        config.load_kube_config()
        v1 = client.AppsV1Api()
        body = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1DeploymentSpec(
                replicas=replicas,
                selector=client.V1LabelSelector(
                    match_labels={"app": name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": name}),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=name,
                                image=image,
                                image_pull_policy=image_pull,
                                ports=[client.V1ContainerPort(container_port=port)]
                            )
                        ]
                    )
                )
            )
        )
        v1.create_namespaced_deployment(body=body, namespace=namespace)
        return body
    elif resource_type == "daemonset" or resource_type == "DaemonSet":
        config.load_kube_config()
        v1 = client.AppsV1Api()
        body = client.V1DaemonSet(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1DaemonSetSpec(
                selector=client.V1LabelSelector(
                    match_labels={"app": name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": name}),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=name,
                                image=image,
                                image_pull_policy=image_pull,
                                ports=[client.V1ContainerPort(container_port=port)]
                            )
                        ]
                    )
                )
            )
        )
        v1.create_namespaced_daemon_set(body=body, namespace=namespace)
        return body
    elif resource_type == "statefulset" or resource_type == "StatefulSet":
        config.load_kube_config()
        v1 = client.AppsV1Api()
        body = client.V1StatefulSet(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1StatefulSetSpec(
                replicas=replicas,
                selector=client.V1LabelSelector(
                    match_labels={"app": name}
                ),
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": name}),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=name,
                                image=image,
                                image_pull_policy=image_pull,
                                ports=[client.V1ContainerPort(container_port=port)]
                            )
                        ]
                    )
                )
            )
        )
        v1.create_namespaced_stateful_set(body=body, namespace=namespace)
        return body
    elif resource_type == "job" or resource_type == "Job":
        config.load_kube_config()
        v1 = client.BatchV1Api()
        body = client.V1Job(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1JobSpec(
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": name}),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=name,
                                image=image,
                                image_pull_policy=image_pull,
                                ports=[client.V1ContainerPort(container_port=port)]
                            )
                        ]
                    )
                )
            )
        )
        v1.create_namespaced_job(body=body, namespace=namespace)
        return body
    elif resource_type == "cronjob" or resource_type == "CronJob":
        config.load_kube_config()
        v1 = client.BatchV1Api()
        body = client.V1CronJob(
            metadata=client.V1ObjectMeta(name=name),
            spec=client.V1CronJobSpec(
                schedule="*/1 * * * *",
                job_template=client.V1JobTemplateSpec(
                    spec=client.V1JobSpec(
                        template=client.V1PodTemplateSpec(
                            metadata=client.V1ObjectMeta(labels={"app": name}),
                            spec=client.V1PodSpec(
                                containers=[
                                    client.V1Container(
                                        name=name,
                                        image=image,
                                        image_pull_policy=image_pull,
                                        ports=[client.V1ContainerPort(container_port=port)]
                                    )
                                ]
                            )
                        )
                    )
                )
            )
        )
        v1.create_namespaced_cron_job(body=body, namespace=namespace)
        return body