import psycopg2
import json

def db_connection():
    connection = psycopg2.connect(user="integration", password="secret_123", database="usa_analysis", port="5432", host="localhost")
    cursor = connection.cursor()
    
    return connection, cursor

# def insert_data(data):

def read_schema():
    with open('./schema/schema.json', 'r') as fl:
        schema = json.loads(fl.read())
    
    fields = []
    for f in schema:
        fields.append({'fieldName': f['fieldName'], 'dataTypeName': f['dataTypeName'], 'desc': f['description']})
    return fields
    
def read_data():
    with open('./data/vehicle_data.json', 'r') as fl:
        data = json.loads(fl.read())
    
    fields = []
    for f in data['meta']['view']['columns']:
        if 'flags' not in f:
            fields.append({'name': f['fieldName'], 'dataTypeName': f['dataTypeName']})

    all_data = data['data']
    
    for all in all_data:
        for i in range(0,8):
            all.pop(i)
    
    return all_data

def main():
    data = read_data()
    conn, cur = db_connection()
    
    cur.executemany("""INSERT INTO public.raw_vehicles (vin_1_10, county, city, state, zip_code, model_year, make, model, ev_type, cafv_type, electric_range, legislative_district, dol_vehicle_id, geocoded_column, electric_utility, _2020_census_tract, omputed_region_x4ys_rtnd, computed_region_fny7_vc3j, computed_region_8ddd_yn5v) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", data)
    
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == '__main__':
    main()