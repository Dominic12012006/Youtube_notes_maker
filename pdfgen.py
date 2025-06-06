import pypandoc

input_md = "sumfinal.md"
output_pdf = "summary.pdf"

pypandoc.convert_file(input_md, 'pdf', outputfile=output_pdf)
print(f"PDF saved as {output_pdf}")
