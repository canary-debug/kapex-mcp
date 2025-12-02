from kubernetes import client, config
from loguru import logger
import subprocess




def get_pod_logs(name: str, namespace: str = "default", tail: int = None) -> str:
    """获取指定 Pod 的日志"""
    try:
        # 构建 kubectl 命令
        command = f"kubectl logs {name} -n {namespace}"

        # 如果指定了行数，添加 --tail 选项
        if tail is not None:
            command += f" --tail={tail}"

        # 执行命令并获取输出
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 使用更宽容的编码方式（如 latin-1）避免解码错误
        return result.stdout.decode('latin-1')
    except subprocess.CalledProcessError as e:
        # 如果命令执行失败，返回错误信息
        return f"Error: {e.stderr.decode('latin-1')}"
    except Exception as e:
        # 捕获其他异常
        return f"Unexpected error: {str(e)}"