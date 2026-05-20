from fastapi import FastAPI
from pydantic import BaseModel
from openai import AzureOpenAI
import os

app = FastAPI()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

class Mail(BaseModel):
    fra: str
    emne: str
    tekst: str

@app.post("/generer-svar")
def generer_svar(mail: Mail):
    svar = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du hjælper med at skrive interne mailsvar. Vær venlig og professionel."},
            {"role": "user", "content": f"Skriv et svar til denne mail:\n\n{mail.tekst}"}
        ]
    )
    return {"udkast": svar.choices[0].message.content}
