from foundry_local_sdk import Configuration, FoundryLocalManager

config = Configuration(app_name="rag-asistan")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

model = manager.catalog.get_model("phi-3.5-mini")
model.download()
model.load()

client = model.get_chat_client()

prompt = """Use the context below to answer the question.

Context:
Fourier Series represents periodic signals.

Question: What is Fourier series?
"""

print("Cevap: ", end="", flush=True)
for chunk in client.complete_streaming_chat([{"role": "user", "content": prompt}]):
    if not chunk.choices:
        continue
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
print()

model.unload()