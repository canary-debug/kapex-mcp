# Apex MCP Server：说话的方式管理你的k8s集群

[TOC]

## 一、为什么使用Apex MCP Server

- 自然语言交互：通过`Claude`、Cursor等支持`MCP`的AI助手，用户可以使用自然语言与`Kubernetes`集群进行交互。
- 降低学习门槛：即使不熟悉`Kubernetes API`或者命令操作，也能轻松管理资源。
- 高效问题诊断：AI助手可以帮助分析集群状态，提供问题解决建议。
- 流程自动化：通过对话式界面自动执行多步骤操作。

## 二、快速上手指南

### 前提条件

- 已部署`Kubernetes`集群
- 拿到`ls ${HOME}/.kube/config`配置文件

### 部署的两种方式

- `1`、单独领出来一台服务器使用`Docker`部署`Apex MCP`，通过暴露的`API`接口进行调用。
- `2`、直接部署到你的`Kubenetes`集群当中进行使用。

### 2.1、Docker部署

- 把`Master`节点的`config`配置文件放在运行`MCP`服务器的`/root/.kube`目录下。

```bash
# config 配置文件目录
[root@apex_mcp ~]# mkdir /root/.kube

# 集群 config 配置文件
[root@master ~]# ls /root/.kube/config 
/root/.kube/config

# 拉取 MCP docker 镜像(公共)
[root@apex_mcp ~]# docker pull registry.cn-hangzhou.aliyuncs.com/images-wzh/apex_k8s_mcp:v1

# 运行镜像
[root@apex_mcp ~]# docker run -d -p 8000:8000 --name apex_k8s_mcp -v /root/.kube/config:/root/.kube/config -v /app_log:/app_log registry.cn-hangzhou.aliyuncs.com/images-wzh/apex_k8s_mcp:v1
```

- 如下日志回显表示`MCP`运行成功

```bash
[root@apex_mcp ~]# docker logs apex_k8s_mcp 
INFO:     Started server process [9]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 2.2、Kubernetes部署

```bash
# 创建工作目录
[root@master ~]# mkdir apex_k8s_mcp
[root@master ~]# cd apex_k8s_mcp/
```

```bash
# 创建命名空间
[root@master apex_k8s_mcp]# kubectl create ns apex-k8s-mcp
```

```bash
# 创建 configmap 的 k8s 的配置文件
[root@master ~]# kubectl create configmap apex-mcp --from-file=k8s-config=/root/.kube/config -n apex-k8s-mcp
```

```yaml
# 创建所需 Pod
---
# 创建 Pod
apiVersion: "apps/v1"
kind: Deployment
metadata:
  name: apex-k8s-mcp
  namespace: apex-k8s-mcp
  labels:
    mcp: apex
spec:
  # 根据公司业务调整 pod 数量
  replicas: 1
  selector:
    matchLabels:
      mcp: apex
  # 用于将现有Pod替换为新Pod的部署策略
  strategy:
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      name: apex
      labels:
        mcp: apex
    spec:
      containers:
      - name: apex
        image: registry.cn-hangzhou.aliyuncs.com/images-wzh/apex_k8s_mcp:v1
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 8000
        volumeMounts:
        - name: mcp-log
          mountPath: /app_log
        # 就绪探针
        readinessProbe:
          tcpSocket:
            port: 8000
          initialDelaySeconds: 150
          periodSeconds: 5
          failureThreshold: 5
        # 存活探针
        livenessProbe:
          tcpSocket:
            port: 8000
          initialDelaySeconds: 150
          periodSeconds: 10
          failureThreshold: 5
      # 创建一个卷
      volumes:
        - name: mcp-log
          # emptyDir是一个空目录，用于临时存储数据。{}表示使用默认配置
          # 生产环境仔细考虑日志是否需要持久化
          emptyDir: {}
---
# 创建 Service Type ClusterIP
apiVersion: "v1"
kind: Service
metadata:
  name: apex-k8s-mcp
  namespace: apex-k8s-mcp
  labels:
    mcp: apex
spec:
  selector:
    mcp: apex
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
---
# 创建路由
apiVersion: "networking.k8s.io/v1"
kind: Ingress
metadata:
  name: apex-k8s-mcp
  namespace: apex-k8s-mcp
  labels:
    mcp: apex
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: "/"
spec:
  ingressClassName: nginx
  rules:
  - host: mcp.k8s.com.cn
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: apex-k8s-mcp
            port:
              number: 8000
---
```

```bash
# 部署资源
[root@master apex_k8s_mcp]# kubectl apply -f apec_k8s_mcp.yaml
```

- 如下日志回显表示`MCP`运行成功

```bash
[root@master apex_k8s_mcp]# kubectl logs -n apex-k8s-mcp apex-k8s-mcp-589cd49d4f-dvjgh 
INFO:     Started server process [9]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 三、MCP客户端调用MCP服务器端

- 下载`Cherry studio`MCP客户端：`https://file-cdn.gitcode.com/5007375/releases/untagger_9cc7b6a6bd9e44b9ab9f33c9ef31aa46/Cherry-Studio-1.5.6-x64-setup.exe?auth_key=1755738425-eb35b89bb66c4ac89b16b8a0ffb2ae90-0-9bc4a16f94d2abca80776397ca15a6acb95a2e8584f0d8406c98eec350ab5890`

### 3.1、调整客户端配置

- 所需的`key`需要用自己的。




![image-20250821095450051](https://github.com/canary-debug/kapex-mcp/blob/main/images/image-20250821094944957.png)
![image-20250821095621018](https://github.com/canary-debug/kapex-mcp/blob/main/images/image-20250821095354947.png)

![image-20250821095621018](https://github.com/canary-debug/kapex-mcp/blob/main/images/image-20250821095450051.png)

### 3.2、API调用

- 问：`获取node节点信息`

![image-20250821094944957](https://github.com/canary-debug/kapex-mcp/blob/main/images/image-20250821095621018.png)

- 问：`在default命名空间中创建一个deployment，名字为wzh，image使用默认的，对外暴露80端口`

![image-20250821100003397](https://github.com/canary-debug/kapex-mcp/blob/main/images/image-20250821100003397.png)

```bash
# 通过集群任意控制平面查看是否创建资源
# 通过以下内容可以看出没有任何问题
[root@master1 ~]# kubectl get pod -n default wzh-6bc76ccd5b-5zx75 -o wide
NAME                   READY   STATUS    RESTARTS   AGE   IP              NODE    NOMINATED NODE   READINESS GATES
wzh-6bc76ccd5b-5zx75   1/1     Running   0          13m   10.244.104.37   node2   <none>           <none>
[root@master1 ~]# curl -I http://10.244.104.37
HTTP/1.1 200 OK
Server: nginx/1.21.5
Date: Thu, 21 Aug 2025 02:01:15 GMT
Content-Type: text/html
Content-Length: 615
Last-Modified: Tue, 28 Dec 2021 15:28:38 GMT
Connection: keep-alive
ETag: "61cb2d26-267"
Accept-Ranges: bytes
```


