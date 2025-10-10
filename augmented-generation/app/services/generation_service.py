from langchain_core.prompts import ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate
from yandex_cloud_ml_sdk import YCloudML


def create_message(user_text, system_text, context):
    prompt_template = ChatPromptTemplate(
        [
            SystemMessagePromptTemplate.from_template(system_text),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    prompt = prompt_template.invoke({"question": user_text, "context":context}).to_messages()

    messages = []
    for msg in prompt:
        msg.type = 'user' if msg.type == 'human' else msg.type

        messages.append(
            {
                "role": msg.type,
                "text": msg.content
            }
        )

    return messages

def send_message(messages, folder_id, model_name, temperature):
    sdk = YCloudML(folder_id=folder_id)
    result = (
        sdk.models.completions(model_name=model_name, model_version="latest").configure(temperature=temperature).run(messages)
    )

    return result
