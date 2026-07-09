from foundry_local_sdk import Configuration, FoundryLocalManager

def main():
    config = Configuration(app_name="rag-asistan")
    FoundryLocalManager.initialize(config)
    manager = FoundryLocalManager.instance

    model = manager.catalog.get_model("phi-3.5-mini")
    model.download()
    model.load()

    client = model.get_chat_client()
    response = client.complete_chat([
        {"role": "user", "content": "Merhaba, nasılsın?"}
    ])

    print(response.choices[0].message.content)

    model.unload()

if __name__ == "__main__":
    main()