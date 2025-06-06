import os
from groq import Groq

# Initialize Groq API client
groq_client = Groq(api_key="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")  # Replace with your actual key

def audio_to_text(audio_path, output_path=None):
    try:
        with open(audio_path, "rb") as f:
            transcription = groq_client.audio.transcriptions.create(
                file=("audio.wav", f.read()),
                model="whisper-large-v3"
            )

        # Determine output file path
        if not output_path:
            base = os.path.splitext(audio_path)[0]
            output_path = base + ".txt"

        # Write to text file
        with open(output_path, "w", encoding="utf-8") as out_file:
            out_file.write(transcription.text)

        print(f"Transcription written to: {output_path}")
        return transcription.text

    except Exception as e:
        print("Error during transcription:", e)
        return None

# audio_to_text(r'downloads\Bubble sort in 2 minutes.wav','a.txt')