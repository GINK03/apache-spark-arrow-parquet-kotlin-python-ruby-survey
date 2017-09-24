import sys
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa


def pandas_parquest():
  df = pd.DataFrame( {'a':[i for i in range(1000)], 'axa':[i*i for i in range(1000)], 'axastr':[str(i*i) for i in range(1000)], 'axabool':[ i%2 == 0 for i in range(1000)], 'axadouble':[ i/10.0 for i in range(1000)] } )
  print( df.head() )

  arrow_table = pa.Table.from_pandas(df)

  pq.write_table(arrow_table, 'local.pq', use_dictionary=False, compression=None)

def parquest_pandas():
  table = pq.read_table('local.pq', nthreads=16)
  df = table.to_pandas()
  print( df.head() )
  print( table.schema )


if '__main__' == __name__:
  if '--save' in sys.argv:
    pandas_parquest()

  if '--load' in sys.argv:
    parquest_pandas()
