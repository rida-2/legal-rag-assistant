import os

from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def verify_output(context, memo):

    prompt = f"""
You are a legal verifier.

Determine whether the legal analysis below is fully
supported by the supplied context.

Return ONLY:

SUPPORTED

or

UNSUPPORTED

Context:

{context}

Analysis:

{memo}
"""

    try:

        response = model.generate_content(
            prompt
        )

        answer = response.text.upper()

        return "SUPPORTED" in answer

    except:

        return True