import pypandoc
from download import download_audio
from audiototext import audio_to_text
from summarize import textbook_summary
from addimages import insert_images

url=input("enter url: ")
audio_path=download_audio(url)

audio_to_text(audio_path,'transcript.txt')
with open("transcript.txt", "r", encoding="utf-8") as f:
    transcript_text = f.read()

summary = textbook_summary(transcript_text)
with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)
print("Summary written to summary.txt")


with open("summary.txt", "r", encoding="utf-8") as f:
    summary = f.read()
updated_summary = insert_images(summary)
with open("sumfinal.md", "w", encoding="utf-8") as f:
    f.write(updated_summary)
print("Summary with images saved as sumfinal.md")


input_md = "sumfinal.md"
output_pdf = "summary.pdf"
pypandoc.convert_file(input_md, 'pdf', outputfile=output_pdf)
print(f"PDF saved as {output_pdf}")