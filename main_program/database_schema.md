# change 3

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

analytics_monitored_area
    {
        "analytics_monitored_area_id":                # primary key  boudingbox_encoding
        "description":                                # secondary key
        "list_points":
        "flow_item_id_collection"      
    }


# this will not be implemented because of the timezone issue
# this particular way of grouping could only keep track/update on a particular timezone
# since the related function TrafficData.update_analytics_traffic_pattern() runs really fast,
# we are going to drop this implementation
#   analytics_traffic_pattern
#       {
#           "analytics_traffic_pattern_id":            # primary key
#           "date_timestamp"                           # secondary key
#           "analytics_monitored_area_id":                # secondary key
#           "traffic_pattern": [
#               {
#               "date_specific_timestamp":             # 1:00
#               "average_JF":
#               },
#               {
#               "date_specific_timestamp":             # 2:00
#               "average_JF":
#               }
#           ]
#       }

analytics_traffic_pattern
    {   
        "crawled_batch_id":                       # compound index
        "analytics_traffic_pattern_id":           # primary key
        "crawled_timestamp":                      
        "average_JF":
        "analytics_monitored_area_id":            # compound index
    }  