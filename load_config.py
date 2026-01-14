import requests as req
import json

def get_metadata():
    with open('./conf/metadata.json') as fl:
        metadata = json.loads(fl.read())
        # print(metadata)
        schema_url = metadata['distribution'][2]['describedBy']
        data_url = metadata['distribution'][2]['downloadURL']
        
    return schema_url, data_url

def get_schema(url):
    print("Downloading schema...")
    res = req.get(url, stream=True)
    res.raise_for_status()
    
    with open('./schema/schema.json', 'wb') as fl:
        for chunk in res.iter_content(chunk_size=4096):
            fl.write(chunk)
    print("Schema downloaded successfully.")
    
def get_data(url):
    print("Downloading data...")
    res = req.get(url, stream=True)
    res.raise_for_status()
    
    with open('./data/vehicle_data.json', 'wb') as fl:
        for chunk in res.iter_content(chunk_size=4096):
            fl.write(chunk)
    print("Vehicle data downloaded successfully.")
    
def main():
    schema_url, data_url = get_metadata()
    get_schema(schema_url)
    get_data(data_url)
    
if __name__ == '__main__':
    main()