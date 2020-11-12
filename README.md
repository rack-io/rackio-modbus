# rackio-modbus

A Rackio extension to enable Modbus TCP Server/Client integration

## Installation

```
pip install RackioModbus
```

## Usage

```python
from rackio import Rackio, TagEngine
from rackio_modbus import RackioModbus

app = Rackio()

driver = RackioSocket(app, mode="server")
```

## Defining Tags and Modbus bindings

```python
tag_egine = TagEngine()

# Tags definitions

tag_egine.set_tag("T1", "float")
tag_egine.set_tag("T2", "float")
tag_egine.set_tag("T3", "float")

# Modbus mapping

driver.define_mapping("T1", "write", 0, 60)
driver.define_mapping("T2", "write", 0, 50)
driver.define_mapping("T3", "read", 0, 110)
```

