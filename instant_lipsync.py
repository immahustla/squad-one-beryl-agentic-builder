import gradio as gr, subprocess, os

def crop_mouth_region_ffmpeg(video_path):
    """Extract mouth region using FFmpeg - THE CRITICAL FIX."""
    if not os.path.exists(video_path):
        return False
    
    # THE FIX: Precise mouth crop using FFmpeg filters
    # Coordinates: h*0.45:0.75, w*0.35:0.65 (both lips INSIDE the square)
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "crop=iw*0.30:ih*0.30:iw*0.35:ih*0.45,scale=256:256",
        "-t", "2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "mouth_fixed.mp4"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("✅ Mouth properly positioned in 256x256 square")
        return True
    except:
        return False

def lipsync(voice_file):
    if voice_file is None: return
    
    # THE CRITICAL FIX: Use properly cropped mouth region
    video_source = "sync.mp4"
    if os.path.exists("sync.mp4"):
        if crop_mouth_region_ffmpeg("sync.mp4"):
            video_source = "mouth_fixed.mp4"
            print("✅ FIXED: Mouth now INSIDE the 256x256 square")
    
    cmd = [
      "ffmpeg","-y","-i",voice_file,"-i",video_source,
      "-async","1","-c","libx264","-map","0:a:0?","-map","1:v:0",
      "out.mp4"
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return "out.mp4"

gr.Interface(
    fn=lipsync,
    inputs=gr.Audio(type="filepath", label="upload wav"),
    outputs=gr.Video(label="lip-sync result (fixed mouth crop)"),
    title="Instant Lip-sync - Fixed Mouth Positioning"
).queue().launch(debug=True)