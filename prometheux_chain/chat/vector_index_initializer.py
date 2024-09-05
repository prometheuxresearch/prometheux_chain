from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Neo4jVector
import os
from ..config import config

class VectorIndexInitializer:
    vector_index = None
    
    @classmethod
    def init_vector_index(cls):
        os.environ["OPENAI_API_KEY"] = config['OPENAI_API_KEY']
        os.environ["NEO4J_URI"] = config['NEO4J_URI']
        os.environ["NEO4J_USERNAME"] = config['NEO4J_USERNAME']
        os.environ["NEO4J_PASSWORD"] = config['NEO4J_PASSWORD']
        print("Initializing Vector Index")
        
        # Initialize embedding model
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large"
        )
        
        # Setup vector index
        VectorIndexInitializer.vector_index = Neo4jVector.from_existing_graph(
            embeddings,
            search_type="vector",
            node_label="OUTPUT",
            text_node_properties=["verbalization"],
            embedding_node_property="embedding"
        )
        
        return 'Vector index initialized successfully'
