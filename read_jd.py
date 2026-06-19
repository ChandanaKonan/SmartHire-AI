from docx import Document

print("Reading Job Description...")

doc = Document(
    "data/job_description.docx"
)

jd_text = ""

for para in doc.paragraphs:

    if para.text.strip():

        jd_text += (
            para.text + "\n"
        )

print("\n" + "=" * 80)
print("JOB DESCRIPTION")
print("=" * 80)

print(jd_text)

print("\n" + "=" * 80)
print(
    f"Total Characters: {len(jd_text)}"
)
print("=" * 80)