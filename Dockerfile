FROM python:3.11.6

WORKDIR /app

COPY . .

RUN mkdir -p /app_log && \
    pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pyinstaller -F main.py && \
    mkdir /root/.kube && \
    cp dist/main .

EXPOSE 8000

CMD ["/bin/sh", "-c", "./main 2>&1 | tee -a /app_log/app.log"]