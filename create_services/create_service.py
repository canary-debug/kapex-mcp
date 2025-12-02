from kubernetes import client, config
from loguru import logger


# 只加载一次 kubeconfig（可以是 in-cluster 或本地 kubeconfig）
try:
    config.load_incluster_config()  # 如果你在集群内运行
except config.config_exception.ConfigException:
    config.load_kube_config()  # 如果你在本地运行


def create_all_services(name="deyun", namespace="default", service_type="NodePort", port=80, targetport=80):
    """
    创建 Kubernetes Service（支持 NodePort / ClusterIP / LoadBalancer）

    参数说明：
    - name: Service 名称
    - namespace: 命名空间，默认 default
    - service_type: Service 类型，如 NodePort / ClusterIP / LoadBalancer
    - port: Service 对外暴露的端口
    - targetport: Pod 中容器监听的端口
    """

    logger.info(f"Creating Service: {name}")
    logger.info(f"Namespace: {namespace}")
    logger.info(f"Service Type: {service_type}")
    logger.info(f"Port: {port}")
    logger.info(f"Target Port: {targetport}")

    try:
        # 确保 port 和 targetport 是整数类型
        port = int(port)
        targetport = int(targetport)
    except (TypeError, ValueError) as e:
        logger.error(f"Port or targetport is not a valid integer: {e}")
        raise

    v1 = client.CoreV1Api()

    service_port = client.V1ServicePort(
        port=port,
        target_port=targetport
    )

    body = client.V1Service(
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1ServiceSpec(
            selector={"app": name},
            ports=[service_port],
            type=service_type
        )
    )

    try:
        response = v1.create_namespaced_service(namespace=namespace, body=body)
        logger.info(f"Service '{name}' created successfully in namespace '{namespace}'")
        return response
    except client.rest.ApiException as e:
        logger.error(f"Kubernetes API error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
