from ..client.JarvisClient import JarvisClient

def chat(nlQuery):
    chat_response = JarvisClient.queryExplain(nlQuery)
    
    if chat_response.status_code != 200:
        # Use single quotes inside the f-string
        raise Exception(f"Chat error. Detail: {chat_response.json()['message']}")
    
    return chat_response.json()["data"]["result"]
