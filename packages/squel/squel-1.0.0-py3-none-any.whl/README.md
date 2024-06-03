# Squel 

SQL parsing, done right.

WIP, but you can you use it as base. Just add the missing definitions to
the grammar.

## Example

```python
from squel.app import Squel


tree = Squel.parse('hello.sql')
print(tree.pretty())
```

### CLI

```sh
squel parse hello.sql
```
