from flask import Flask, render_template, jsonify, send_from_directory, request
import os
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

VIDEO_ROOT = "/mnt/sdb1/jiankang"

if not os.path.exists(VIDEO_ROOT):
    print(f"⚠️ 视频目录不存在: {VIDEO_ROOT}")
else:
    print(f"✅ 视频目录: {VIDEO_ROOT}")

# ------------------ 获取设备 ------------------
def get_devices():
    if not os.path.exists(VIDEO_ROOT):
        return []
    return [d for d in os.listdir(VIDEO_ROOT)
            if os.path.isdir(os.path.join(VIDEO_ROOT, d))]

# ------------------ 获取视频 ------------------

def get_videos(device, date_str):
    path = os.path.join(VIDEO_ROOT, device)
    if not os.path.exists(path):
        print(f"⚠️ 目录不存在: {path}")
        return []

    videos = []
    for f in os.listdir(path):
        if not f.lower().endswith(".mp4"):
            continue

        full = os.path.join(path, f)
        # 文件修改时间（北京时间 UTC+8）
        mtime = datetime.fromtimestamp(os.path.getmtime(full), timezone(timedelta(hours=8)))
        file_date = mtime.strftime("%Y-%m-%d")

        # 只返回当天的视频
        if file_date != date_str:
            continue

        videos.append({
            "name": f,
            "url": f"/video/{device}/{f}",
            "time": mtime.strftime("%Y-%m-%d %H:%M:%S"),  # 北京时间字符串
            "hour": mtime.hour,
            "minute": mtime.minute,
            "start_sec": mtime.hour*3600 + mtime.minute*60 + mtime.second
        })

    # 按 start_sec 排序，更适合前端播放头映射
    videos.sort(key=lambda x: x["start_sec"])

    print(f"找到 {len(videos)} 个视频: {[v['name'] for v in videos]}")
    return videos


# ------------------ 路由 ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/devices")
def api_devices():
    return jsonify(get_devices())

@app.route("/api/videos/<device>")
def api_videos(device):
    date_str = request.args.get("date", datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d"))
    return jsonify(get_videos(device, date_str))

@app.route("/video/<device>/<filename>")
def serve_video(device, filename):
    return send_from_directory(os.path.join(VIDEO_ROOT, device), filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8383, debug=True)
