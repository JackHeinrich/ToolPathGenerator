import pinecone

#api key
pinecone.init(api_key="9b59c2cf-d638-4f91-a12b-2c793a1997e6", environment="us-west1-gcp-free")

#creating an index
#pinecone.create_index("quickstart", dimension=8, metric="euclidean")

#retrieving indexes
print(pinecone.list_indexes())

index = pinecone.Index("testindex")

print(pinecone.describe_index("testindex"))

index.upsert( vectors=[
        {
        'id':'Cat', 
        'values':[0.1, 0.2, 0.3, 0.4,0.5,0.6,0.7,0.8], 
        'metadata':{'genre': 'animals'},
           'sparse_values':
           {'indices': [10, 45, 16],
           'values':  [0.5, 0.5, 0.2]}},
        {'id':'Frog', 
        'values':[0.2, 0.3, 0.4, 0.5,0.6,0.7,0.8,0.9], 
        'metadata':{'genre': 'action'},
           'sparse_values':
           {'indices': [15, 40, 11],
           'values':  [0.4, 0.5, 0.2]}}
    ])

#print(index.describe_index_stats())

query_response = index.query(
    vector=[0.2, 0.3, 0.4, 0.5,0.6,0.7,0.8,0.9],
    top_k=1,
    include_values=True
)

print(query_response)

#prints name of queried index.
#print(queried_index['matches'][0]['id'])

#deletes index
# pinecone.delete_index("quickstart")

# print(pinecone.list_indexes())