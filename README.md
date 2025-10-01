# readables-py

Enhance code readability and self-documentation in our Python code

### Distributed Lock

> [!NOTE]
> Check out [the dedicated documentation](readables/dlock/README.md).

### Environment Variable Manager and Exporter

#### Declare and retrieve variables

Here is how you can declare and retrieve variables.

```python
from readables.env import required_env, optional_env, flag

ALPHA = required_env('ALPHA', help='Alpha variable')
BETA = optional_env('BETA', 'default_value', help='Beta variable')
CHARLIE = flag('CHARLIE', help='Charlie flag')
```

> [!TIP]
> When `required_env` is used, if the variable is not set, it will raise an exception.

#### Export variables

We have provided two exporters: the env file exporter and the MarkDown exporter. If you are working on the code that
the required environment variables are not set, you will need to set `READABLES_ENV_ALLOW_UNSET_REQUIRED` to `true`
before using an exporter to suppress the error.

In this example, we use the env file exporter to generate the content of the distributed env file using the content above.

```python
from os import environ

environ['READABLES_ENV_ALLOW_UNSET_REQUIRED'] = 'true' 

from readables.env import manager, EnvFileExporter

output = EnvFileExporter.export(manager.variables)
```

