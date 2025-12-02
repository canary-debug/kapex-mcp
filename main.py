# 官方包
from mcp.server.fastmcp import FastMCP


# 二方包
from get_pods.get_pod import *
from create_controllers.create_controller import *
from get_nodes.get_node import *
from update_images.update_image import *
from delete_resources.delete_resource import *
from create_services.create_service import *
from get_services.get_service import *
from get_logs.get_log import *




# 创建实例
mcp = FastMCP("MCP-Server", host="0.0.0.0", port=8000)


# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """加法运算
#
#     Args:
#         a (int): 第一个数
#         b (int): 第二个数
#
#     """
#     return a + b


# 获取指定 namespace 名称空间中的 pod, 默认获取 default 名称空间中的所有 pod.
@mcp.tool()
def get_all_pods(namespace: str = "default") -> list:
    return get_pods(namespace)




@mcp.tool()
def get_all_nodes(name: str) -> list:
    return get_nodes(name)




# 创建所有 k8s 资源.
@mcp.tool()
def create_resources(resource_type: str, name: str, image: str = "nginx:latest", namespace: str = "default", replicas: int = 1, port: int = 80, image_pull: str = "IfNotPresent") -> str:
    return create_all_resources(resource_type, name, image, namespace, replicas, port, image_pull)




# 更新 指定资源 的 service.
@mcp.tool()
def create_services(name="deyun", namespace="default", service_type="NodePort", port=80, targetport=80) -> str:
    return create_all_services(name, namespace, service_type, port, targetport)




@mcp.tool()
def delete_services(name: str, namespace: str = "default") -> str:
    """删除指定 Service"""
    return delete_service(name, namespace)




def get_services(namespace: str = "default") -> list:
    """获取 k8s 中指定的命名空间下的所有的 Service"""
    return get_services(namespace)




def get_logs(name: str, namespace: str = "default", tail: int = None) -> str:
    """获取指定 Pod 的日志"""
    return get_pod_logs(name, namespace, tail)




# 更新 指定资源 的镜像.
@mcp.tool()
def update_all_images(resource_type: str, name: str, new_image: str, namespace: str = "default") -> str:
    """更新指定资源类型的资源的镜像"""
    return update_images(resource_type, name, new_image, namespace)




# 删除 指定 资源.
@mcp.tool()
def delete_all_resources(resource_type: str, name: str, namespace: str = "default") -> str:
    """删除指定资源类型的资源"""
    return delete_resources(resource_type, name, namespace)









if __name__ == "__main__":
    mcp.run(transport="sse")


