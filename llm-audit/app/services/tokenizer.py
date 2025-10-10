from flask import current_app
from yandex_cloud_ml_sdk import YCloudML


def get_tokens(messages, folder_id, model_name,):
    sdk = YCloudML(folder_id=folder_id)
    model =  sdk.models.completions(model_name=model_name, model_version="latest")

    result = model.tokenize(messages)
    current_app.logger.info("Tokens: %s", len(result))
    return result
