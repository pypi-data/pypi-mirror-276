from PIL import Image
from moviepy.editor import VideoFileClip


# 等比例抽帧
def get_frame(video_path, frame_num: int, outpath='.', name0='frame_'):
    # 打开视频文件
    with VideoFileClip(video_path) as video:
        # 计算抽帧的时间点
        frame_times = [video.duration * i / frame_num for i in range(frame_num)]  # 在视频总时长内均匀抽帧
        # 抽帧
        frames = [video.get_frame(t) for t in frame_times]
        # 保存抽帧
        for i, frame in enumerate(frames):
            frame_image_path = f"{outpath}/{name0}{i}.jpg"
            frame_image = Image.fromarray(frame)  # 将帧转换为图像
            frame_image.save(frame_image_path)
