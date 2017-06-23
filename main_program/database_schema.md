# before 
crawled_batch    #(table)
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

# change 1

crawled_batch (table)
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


# change 2

crawled_batch (table)
    {
        "crawled_matrix_encoding":
        "crawled_timestamp":                     # secondary timestamp key
        "crawled_data_id":                       #(primary key)
    }

original_data (table)
    {
        "CREATED_TIMESTAMP":
        "RWS":
        "original_data_id": (primary key)
        "crawled_batch_id"
    }

flow_item  (table)
    {
        "TMC":
        "flow_item_id":                   #(primary key)  a TMC_encoding 
    },

road_data (table)
    {
        "FC":
        "flow_item_id":                     # secondary key
        "geometry":                         # secondary geospatial key
        "road_data_id":                     #(primary key) a geometry_encoding
        "value":                    
    }

flow_data (table)
{
    "crawled_batch_id":                  # compound index
    "flow_item_id":                      # compound index
    "created_timestamp":
    "CN":
    "JF":
    ...
    "original_data_id":
    "flow_data_id":                    #(primary key)
}