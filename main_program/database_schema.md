# before 
crawled_data    #(table)
    {
        "crawled_matrix_encoding":
        "crawled_timestamp":
        "id":                       #(primary key)
    }

original_data (table)
    {
        "CREATED_TIMESTAMP":
        "RWS":
        "id": (primary key)
        "crawled_batch_id"
    }
flow_data  (table)
    {
        "CF":
        "CUSTOM": {
            "crawled_batch_id":
            "created_timestamp":
            "original_data_id":
            "parent_DE":
        }
        "SHP":
        "TMC":
        "id":                       #(primary key)
    },

road_data (table)
    {
        "FC":
        "crawled_batch_id":
        "created_timestamp":
        "flow_data_id":
        "geometry"
        "id": (primary key)
        "value":
    }

# after
crawled_data (table)
    {
        "crawled_matrix_encoding":
        "crawled_timestamp":
        "id":                       #(primary key)
    }

original_data (table)
    {
        "CREATED_TIMESTAMP":
        "RWS":
        "id": (primary key)
        "crawled_batch_id"
    }
flow_data  (table)
    {
        "CF": {
            "{{crawled_batch_id}}": [
                {
                    "CN":
                    "JF":
                    ...
                    "crawled_batch_id":
                    "created_timestamp":
                    "original_data_id":
                },
            ]
        }
        "SHP":
        "TMC":
        "id":                   #(primary key)  a TMC_encoding 
    },

road_data (table)
    {
        "FC":
        "flow_data_id":
        "geometry":
        "id":                     #(primary key) a geometry_encoding
        "value":                    
    }