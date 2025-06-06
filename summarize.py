import tiktoken
from groq import Groq
import textwrap

MODEL   = "llama3-70b-8192"
API_KEY = "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"
client  = Groq(api_key=API_KEY)

PROMPT = textwrap.dedent("""\
    Summarize the following lecture transcript into a textbook chapter. Include:
    - A chapter title
    - A 1-paragraph introduction
    - Headings and sub-headings
    - Bullet points using dashes (-)
    - Code blocks formatted with triple backticks (```python ... ```)
    - Concluding summary of main takeaways
    - Mention where images or diagrams should be inserted with placeholders like $$[Main_topic,diagram_explanation]$$
    """)

def count_tokens(text):
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def summarize(text, instr):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system",
             "content": "You are an expert textbook writer."},
            {"role": "user",
             "content": instr + "\n\n" + text}
        ],
        temperature=0.4,
    )
    return resp.choices[0].message.content.strip()

def textbook_summary(transcript, chunk_tokens=3000):
    if count_tokens(transcript) < 8000:
        # one-shot
        return summarize(transcript, PROMPT)
    
    # map–reduce
    chunks, cur = [], []
    for paragraph in transcript.split("\n"):
        cur.append(paragraph)
        if count_tokens("\n".join(cur)) >= chunk_tokens:
            chunks.append("\n".join(cur)); cur=[]
    if cur: chunks.append("\n".join(cur))
    
    partials = [summarize(c, PROMPT) for c in chunks]
    merged   = "\n\n".join(partials)
    return summarize(merged,"Combine these sectional notes into a single textbook-style chapter.")


# with open("transcript.txt", "r", encoding="utf-8") as f:
#     transcript_text = f.read()

# summary = textbook_summary(transcript_text)

# with open("summary.txt", "w", encoding="utf-8") as f:
#     f.write(summary)

# print("Summary written to summary.txt")
