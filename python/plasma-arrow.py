import numpy as np
import os
import random
import signal
import subprocess
import time
import sys
import pyarrow as pa
import pyarrow.plasma as plasma
import pandas as pd

client = plasma.connect("/tmp/plasma", "", 0)

# Create an object and seal
def seal():
  object_id = plasma.ObjectID(20 * b'b')
  object_size = 1000
  buffer = memoryview(client.create(object_id, object_size))

  # Write to the buffer.
  for i in range(1000):
    buffer[i] = i%128

  # Seal the object making it immutable and available to other clients.
  client.seal(object_id)

def get_seal():
  # Create a different client. Note that this second client could be
  # created in the same or in a separate, concurrent Python session.
  client2 = plasma.connect("/tmp/plasma", "", 0)
  # Get the object in the second client. This blocks until the object has been sealed.
  object_id2 = plasma.ObjectID(20 * b'b')
  [buffer2] = client2.get_buffers([object_id2])
  view2 = memoryview(buffer2)
  for i in range(200):
    print( view2[i] )

## put and getting 
def put_get():
  # Create a python object.
  object_id = client.put('hello, plasma')
  print( object_id )
  # Get the object.
  data = client.get(object_id)
  print( data )

def write_pandas_plasma():
  import pyarrow as pa
  import pandas as pd

  # Create a Pandas DataFrame
  d = {'one' : pd.Series([1., 2., 3.], index=['a', 'b', 'c']),
     'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
  df = pd.DataFrame(d)

  # Convert the Pandas DataFrame into a PyArrow RecordBatch
  record_batch = pa.RecordBatch.from_pandas(df)

  # Create the Plasma object from the PyArrow RecordBatch. Most of the work here
  # is done to determine the size of buffer to request from the object store.
  
  # object_id = plasma.ObjectID(np.random.bytes(20))
  object_id = plasma.ObjectID(b'az'*10)
  mock_sink = pa.MockOutputStream()
  stream_writer = pa.RecordBatchStreamWriter(mock_sink, record_batch.schema)
  stream_writer.write_batch(record_batch)
  stream_writer.close()
  data_size = mock_sink.size()
  buf = client.create(object_id, data_size)

  # Write the PyArrow RecordBatch to Plasma
  stream = pa.FixedSizeBufferWriter(buf)
  stream_writer = pa.RecordBatchStreamWriter(stream, record_batch.schema)
  stream_writer.write_batch(record_batch)
  stream_writer.close()
  client.seal(object_id)


def read_pandas_plasma():
  object_id = plasma.ObjectID(b'az'*10)
  [data] = client.get_buffers([object_id])  # Get PlasmaBuffer from ObjectID
  buffer = pa.BufferReader(data)
  # Convert object back into an Arrow RecordBatch
  reader = pa.RecordBatchStreamReader(buffer)
  record_batch = reader.read_next_batch()
  object_id = plasma.ObjectID(b'az'*10)
  # Convert back into Pandas
  result = record_batch.to_pandas()
  print( result.head() )

if __name__ == '__main__':
  if '--seal' in sys.argv:
    seal()

  if '--get_seal' in sys.argv:
    get_seal()

  if '--put_get' in sys.argv:
    put_get()

  if '--write_pandas_plasma' in sys.argv:
    write_pandas_plasma()

  if '--read_pandas_plasma' in sys.argv:
    read_pandas_plasma()
