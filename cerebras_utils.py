import os
from cerebras.cloud.sdk import Cerebras

def get_ai_analysis(ticker1, ticker2=""):
    client = Cerebras(api_key=os.getenv("CEREBRAS_API_KEY"))
    if ticker2:
        prompt = f"Compare {ticker1} and {ticker2} based on their recent performance."
    else:
        prompt = f"Provide an analysis for {ticker1} based on its recent performance."

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3.1-8b",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error fetching analysis: {e}"
