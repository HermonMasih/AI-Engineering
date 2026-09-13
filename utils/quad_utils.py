from qdrant_client import QdrantClient
from qdrant_client.models import (Distance, VectorParams, PointStruct,PayloadSchemaType)
import os
import logging

def quadrant_client():
    quad_client = QdrantClient(
    url=os.getenv('QDRANT_CLUSTER_KEY'),
    api_key=os.getenv('QDRANT_API_KEY'),
    cloud_inference=True)
    return quad_client

def create_collections(quad_client, collection_name):
    if quad_client.collection_exists(collection_name=collection_name):
        quad_client.delete_collection(collection_name=collection_name)
    
    quad_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    logging.info(f'collection with name: {collection_name} created successfully.')

    quad_client.create_payload_index(
    collection_name=collection_name,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD,
)

def create_collection_points(
    quad_client, 
    collection_name,
    embed_documents,
    documents
    ):
    points = []
    for i, embed_doc in enumerate(embed_documents):
        point = PointStruct(
            id=i+1,
            vector=embed_doc,
            payload={
                'text': documents[i]
            }
        )
        points.append(point)

    logging.info('Points created for each knowledge. Inserting them into collections.....')

    try:
        quad_client.upsert(
        collection_name=collection_name,
        points=points,
        )
        logging.info('Points inserted into collection successfully.')
    except Exception as e:
        raise e
    