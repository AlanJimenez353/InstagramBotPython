from moviepy.editor import VideoClip, TextClip, CompositeVideoClip

def generate_video_with_facts(facts, output_path):
    clips = []
    for fact in facts:
        text_clip = TextClip(fact, fontsize=24, color='white', size=(1280, 720)).set_duration(5)
        clips.append(text_clip)
    video = CompositeVideoClip(clips)
    video.write_videofile(output_path, fps=24)
