# IPC Parser

By using `ipc_parser` you will be able to get the data frame of International Patent Classifications (IPC) from IPC-Scheme xml file that you could download from wipo website. This dataframe includes ipc human readable code, description, parent list and materialized path.

## Use Case Example

```bash
pip install ipc_parser
```

Download IPC_scheme xml file from following link:
https://www.wipo.int/ipc/itos4ipc/ITSupport_and_download_area/20240101/MasterFiles/index.html

```python
from ipc_parser.parser import IpcParser

path_to_xml = "EN_ipc_scheme_20240101.xml"

ipc_obj = IpcParser(ipc_xml=path_to_xml)
df = ipc_obj.get_dataframe()


```
