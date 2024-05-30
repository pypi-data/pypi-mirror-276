import polars as pl
from polars_list_helpers import closest_elem_index

df = pl.DataFrame({
    'a': [[22100.00,22200.00,22300.00,22400.00], [22100.00,22200.00,22300.00,22400.00], [22100.00,22200.00,22300.00,22400.00], [22100.00,22200.00,22300.00,22400.00]],
    'b': [22130.0,22230.0,22330.0,22370.0] 
})
result = df.with_columns(closest_elem_index('a', 'b').alias('closest_elem_index'))
print(result)

