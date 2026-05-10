import os
import glob
import shlex  # 用于智能解析多路径字符串

def extract_video_from_jpg(jpg_path, output_folder=None):
    """从封装的 JPG 文件中提取嵌入的 MP4 视频"""
    if not os.path.exists(jpg_path):
        print(f"[-] 错误: 找不到文件 {jpg_path}")
        return

    # 这里的逻辑决定了视频生成在哪里
    file_name = os.path.splitext(os.path.basename(jpg_path))[0]
    if output_folder is None:
        output_folder = os.path.dirname(jpg_path)
    
    output_mp4 = os.path.join(output_folder, f"{file_name}_live_video.mp4")
    HEADER_MARKER = b'ftyp'

    try:
        with open(jpg_path, 'rb') as f:
            data = f.read()
            offset = data.rfind(HEADER_MARKER)

            if offset == -1:
                print(f"[-] 跳过: {os.path.basename(jpg_path)} (未检测到实况数据)")
                return

            video_start = offset - 4
            video_data = data[video_start:]

            with open(output_mp4, 'wb') as out_f:
                out_f.write(video_data)
            
            print(f"[+] 成功: 已提取 -> {os.path.basename(output_mp4)}")

    except Exception as e:
        print(f"[!] 处理 {jpg_path} 时出错: {e}")

def main():
    print("=== 实况照片批量提取工具 ===")
    print("提示：可以直接选中多张图片，或一个文件夹，直接拖入此窗口")
    
    raw_input = input("\n请拖入文件或文件夹并按回车: ").strip()
    
    # 使用 shlex.split 智能拆分用户输入的多个路径
    try:
        # posix=False 是为了兼容 Windows 的反斜杠路径
        paths = shlex.split(raw_input, posix=False)
    except Exception:
        # 如果 shlex 解析失败，回退到简单的引号替换（针对极特殊情况）
        paths = [raw_input.replace('"', '')]

    for path in paths:
        path = path.strip('"') # 再次确保去掉两侧引号
        
        if os.path.isfile(path):
            if path.lower().endswith(('.jpg', '.jpeg')):
                extract_video_from_jpg(path)
        elif os.path.isdir(path):
            print(f"[*] 正在扫描文件夹: {path}")
            # 扫描文件夹下所有 jpg/jpeg
            extensions = ('*.jpg', '*.jpeg')
            files_grabbed = []
            for ext in extensions:
                files_grabbed.extend(glob.glob(os.path.join(path, ext)))
            
            for file in files_grabbed:
                extract_video_from_jpg(file)
        else:
            print(f"[!] 无法识别路径: {path}")

if __name__ == "__main__":
    main()
    print("\n" + "="*30)
    input("全部处理完成，按回车键退出...")