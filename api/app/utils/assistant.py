from dotenv import load_dotenv
from openai import OpenAI

from api.app.utils import EventHandler

load_dotenv()
client = OpenAI()

assistant = client.beta.assistants.create(
    name="Navigi Analyst Assistant",
    instructions="You are an expert analyst. Use your knowledge base to answer questions about audited financial statements.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
)


vector_store = client.beta.vector_stores.create(name="Navigi Statements")
file_paths = "Navigi.json"
file_streams = [open(file_paths, "rb")]

print(file_streams)
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
vector_store_id=vector_store.id, files=file_streams
)

print(file_batch.status)
print(file_batch.file_counts)


assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

thread = client.beta.threads.create()

def run_assistant(msg: str):
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role="user",
      content=msg,
    )
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
    message_content = messages[0].content[0].text
    # # annotations = message_content.annotations
    # # citations = []
    # # for index, annotation in enumerate(annotations):
    # #     message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
    # #     if file_citation := getattr(annotation, "file_citation", None):
    # #         cited_file = client.files.retrieve(file_citation.file_id)
    # #         citations.append(f"[{index}] {cited_file.filename}")

    print("assistant: ", message_content.value)
    return message_content.value
    # # print("\n".join(citations))
    # with client.beta.threads.runs.stream(
    #     thread_id=thread.id,
    #     assistant_id=assistant.id,
    #     event_handler=EventHandler(),
    # ) as stream:
    #     stream.until_done()
    # yield stream