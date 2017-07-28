# change 4

crawled_batch (table)
    {
        "crawled_matrix_encoding":
        "crawled_timestamp":                     # secondary timestamp key
        "crawled_batch_id":                       #(primary key)
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

route_cached (table)
    {
        "route_cached_id":
        "geojson_road_id_collection":
    }

analytics_monitored_area
    {
        "analytics_monitored_area_id":                # primary key  boudingbox_encoding
        "description":                                # secondary key
        "list_points":
        "flow_item_id_collection"      
    }

analytics_traffic_pattern
    {   
        "crawled_batch_id":                       # compound index
        "analytics_traffic_pattern_id":           # primary key
        "crawled_timestamp":                      
        "average_JF":
        "analytics_monitored_area_id":            # compound index
    }  