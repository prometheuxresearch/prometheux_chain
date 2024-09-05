from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from ..config import config

from .vector_index_initializer import VectorIndexInitializer
import os


class QueryHandler:
    def __init__(self):
        os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']

    def query_explain(self, question):
        vector_index = VectorIndexInitializer.vector_index

        if vector_index is None:
            print("Vector index is not initialized")
            initializer = VectorIndexInitializer()
            print(initializer.init_vector_index())
            vector_index = VectorIndexInitializer.vector_index

        model = config['OPENAI_MODEL']
        llm = ChatOpenAI(model=model, temperature=0)

        retriever = vector_index.as_retriever(
            search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
        )

        prompt_template = """Given the question below and the following context featuring some logic facts that were retrieved, please filter in only the logic facts or fact that answer the question.
          If no fact useful to answer the question was retrieved, please return 'None'. Do not add introductory phrases or additional context. 
                          
        Context: {context}
      
        Question: {question}
        """
        PROMPT = PromptTemplate(template=prompt_template,
                                input_variables=["context", "question"])
        chain_type_kwargs = {"prompt": PROMPT}

        print("prompt "+str(PROMPT))
        qa_graph_chain = RetrievalQA.from_chain_type(llm,
                                                     retriever=retriever,
                                                     verbose=True,
                                                     return_source_documents=True,
                                                     chain_type_kwargs=chain_type_kwargs)

        result = qa_graph_chain({"query": question})
        print("result " + str(result))
        response = {"result": result["result"]}

        facts_to_explain = []
        for doc in result['source_documents']:
            content = doc.metadata.get('fact')
            if content:
                facts_to_explain.append(content)

        response["facts"] = facts_to_explain
        return response
