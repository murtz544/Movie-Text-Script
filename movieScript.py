import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

input_video = "./video.mp4"
output_video = "./final_output1.mp4"
main_text = "It is a period of civil wars in the galaxy. A brave alliance of underground freedom fighters has challenged the tyranny and oppression of the awesome GALACTIC EMPIRE."

subtext1 = "Star Wars"
subtext2 = "A New Hope"

font = "Arial-Bold"
text_color = "white"

video = VideoFileClip(input_video)
w, h = video.size
main_font_size = int(h * 0.07)
subtitle_font_size = int(h * 0.04)

# Define max constraints
max_chars_per_line = 10
max_lines = 7
line_height = main_font_size * 1.2

# Split main_text into lines
words = main_text.split()
formatted_main_text = []
line = ""

for word in words:
    if len(line) + len(word) <= max_chars_per_line:
        line += (word + " ")
    else:
        formatted_main_text.append(line.strip())
        line = word + " "

if line:
    formatted_main_text.append(line.strip())

# Define the text clip duration
text_clip_duration = video.duration

# Create the main text clip with scrolling behavior
if len(formatted_main_text) > max_lines:
    main_text_clip = (TextClip("\n".join(formatted_main_text), fontsize=main_font_size, color=text_color,
                                font=font, method='caption', size=(w * 0.8, None),
                                stroke_color="black", stroke_width=3)
                      .set_position(lambda t: ('center', h * 0.5 - (h * 0.5 / (text_clip_duration - 2)) * t))  # Scrolls from mid to top
                      .set_duration(text_clip_duration)
                      .crossfadeout(2))
else:
    main_text_clip = (TextClip("\n".join(formatted_main_text), fontsize=main_font_size, color=text_color,
                                font=font, method='caption', size=(w * 0.8, None),
                                stroke_color="black", stroke_width=3)
                      .set_position(('center', h * 0.25))  # Static position in the upper half if within 7 lines
                      .set_duration(text_clip_duration)
                      .crossfadeout(2))

# Place subtitles at the bottom 30% of the screen
subtext1_clip = (TextClip(subtext1, fontsize=subtitle_font_size, color=text_color,
                          font=font, method='caption', size=(w * 0.6, None),
                          stroke_color="black", stroke_width=2)
                 .set_position(('center', h * 0.72))  # Line 8
                 .set_duration(text_clip_duration)
                 .crossfadeout(2))

subtext2_clip = (TextClip(subtext2, fontsize=subtitle_font_size, color=text_color,
                          font=font, method='caption', size=(w * 0.6, None),
                          stroke_color="black", stroke_width=2)
                 .set_position(('center', h * 0.78))  # Line 9
                 .set_duration(text_clip_duration)
                 .crossfadeout(2))

# Combine all clips
clips = [video, main_text_clip, subtext1_clip, subtext2_clip]
final_video = CompositeVideoClip(clips)
final_video.write_videofile(output_video, codec="libx264", fps=video.fps or 24)
