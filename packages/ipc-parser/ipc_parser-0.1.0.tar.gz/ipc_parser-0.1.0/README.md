# IPC Parser

By using `ipc_parser` you will be able to get the data frame of International Patent Classifications (IPC) from IPC-Scheme xml file that you could download from wipo website. This dataframe includes ipc human readable code, description, parent list and materialized path.

## Use Case Example

```bash
pip install ipc_parser
```

```python
from ipc_parser.parser import IpcParser

ipc_obj = IpcParser(ipc_xml=path_to_ipc_xml)
df = ipc_obj.get_dataframe()


```
