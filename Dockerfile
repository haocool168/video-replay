# 使用轻量化 Python 镜像
FROM python:3.11-slim

# 设置时区为上海（北京时间）
ENV TZ=Asia/Shanghai

# 设置工作目录
WORKDIR /opt/videos


# 拷贝文件
COPY requirements.txt .
COPY app.py .
COPY templates/index.html ./templates/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建视频挂载目录
RUN mkdir -p /mnt/sdb1/jiankang

# 复制入口脚本并赋予执行权限
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 暴露端口
EXPOSE 8383

# 启动容器
ENTRYPOINT ["/entrypoint.sh"]
