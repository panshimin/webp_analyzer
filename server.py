from flask import Flask, request, render_template
from PIL import Image

app = Flask(__name__)

def calculate_webp_memory_size(file_stream):
    with Image.open(file_stream) as img:
        mode = img.mode
        frame_count = getattr(img, "n_frames", 1)

        if img.format == "WEBP":
            if "alpha" in img.info:
                mode = "RGBA"
            else:
                mode = "RGB"

        bytes_per_pixel = {
            "L": 1, "RGB": 3, "RGBA": 4, "P": 1
        }.get(mode, 4)

        total_memory_size = 0
        output = [f"图片格式：{img.format}", f"模式：{mode}"]

        for frame in range(frame_count):
            img.seek(frame)
            width, height = img.size
            row_bytes = width * bytes_per_pixel
            frame_memory_size = row_bytes * height
            total_memory_size += frame_memory_size
            output.append(f"帧 {frame + 1}: 分辨率 {width}x{height}, 内存大小: {frame_memory_size / 1024:.2f} KB")

        output.append(f"动图总帧数: {frame_count}")
        output.append(f"动图真实总内存大小: {total_memory_size / (1024 * 1024):.2f} MB")
        return "\n".join(output)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return "没有找到上传文件", 400
    file = request.files["image"]
    return calculate_webp_memory_size(file.stream)

if __name__ == "__main__":
    app.run(debug=True)
