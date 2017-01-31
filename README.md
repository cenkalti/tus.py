# tus.py
tus (resumable file upload protocol) client in python

# Install
```shell
pip install -U tus.py
```

# Usage (command line)
This command will upload a single file to the server:
```shell
tus-upload \
    example.bin \
    https://upload.example.com/files/ \
    --header authorization 'token foo' \
    --chunk-size 256000
```

After upload request is accepted on server, upload location is printed to
`stdout`.

If upload fails at any point, program will exit with a non-zero code.

You can continue uploading with following command:
```shell
tus-resume \
    example.bin \
    https://upload.example.com/files/393ebd3506d3a42994c1563c1f8c5684 \
    --header authorization 'token foo' \
    --chunk-size 256000
```

# Usage (Python)

The following example uploads a file in single call.

```python
import tus

FILE_PATH = 'example.bin'
TUS_ENDPOINT = 'https://upload.example.com/files/'
HEADERS = {'Authorization': 'token foo'}
CHUNK_SIZE = 256000

with open(FILE_PATH, 'rb') as f:
    tus.upload(
    	f,
        TUS_ENDPOINT,
        headers=headers,
        chunk_size=CHUNK_SIZE)
```

If you want resume feature use `tus.create()` and `tus.resume()` functions.
