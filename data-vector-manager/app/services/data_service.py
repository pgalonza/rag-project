from langchain_core.documents import Document

def prepare_documents(df):
    documents = []
    for row in df:
        metadata = row['metadata']
        # Создаем объект Document вместо обычного словаря
        content = row['content']
        doc = Document(
            page_content=content,
            metadata=metadata
        )
        documents.append(doc)
    return documents