"""SQL queries for the extract cell module."""

# noinspection SqlNoDataSourceInspection
empty_query = """
SELECT EXISTS(
SELECT 1
 FROM {{grid_table | sqlsafe}} as gt
   INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
   INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
 WHERE TRUE
  AND gt.cell_x = {{cell_x}}
  AND gt.cell_y = {{cell_y}}
  AND dst.mobile_type = 'Class A'

  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}
  );
"""

# TODO: Query design not finalized, confirm what is needed.
# noinspection SqlNoDataSourceInspection
meta_query = """
SELECT avg(gt.draught) as avg_draught
FROM depth.fact_depth_50m as gt
INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND cell_x = 83176
  AND cell_y = 64038
  AND dst.mobile_type = 'Class A'
  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %};
"""

# noinspection SqlNoDataSourceInspection
ship_query = """
SELECT ds.mmsi,
       ds.name,
       dst.ship_type,
       count(*) as num_trips,
       min(draught) as min_draught,
       max(draught) as max_draught
FROM {{grid_table | sqlsafe}} AS gt
  INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND cell_x = {{cell_x}}
  AND cell_y = {{cell_y}}
  AND mobile_type = 'Class A'

  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}

GROUP BY mmsi,
         ds.name,
         dst.ship_type
ORDER BY ds.mmsi;
"""

# noinspection SqlNoDataSourceInspection
draught_query = """
SELECT draught, count(*) as cnt
FROM {{grid_table | sqlsafe}} as gt
  INNER JOIN public.dim_ship AS ds ON gt.ship_id = ds.ship_id
  INNER JOIN public.dim_ship_type AS dst ON gt.ship_type_id = dst.ship_type_id
WHERE TRUE
  AND gt.cell_x = {{cell_x}}
  AND gt.cell_y = {{cell_y}}
  AND dst.mobile_type = 'Class A'
  {% if from_date and to_date %}
  AND gt.date_id BETWEEN {{from_date}} AND {{to_date}}
  {% endif %}
GROUP BY draught
ORDER BY draught DESC;
"""
