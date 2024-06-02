<h1 align="center">pyconfig_util</h1>

- pyconfig_util.py

取出配置放进内存

规范：
配置文件路径：`root_dir + '/config/' + 'setting.yaml'` ，即项目运行目录下的`/config/setting.yaml`
默认配置文件路径： `root_dir + '/config/' + 'setting.default.yaml'`，即项目运行目录下的`/config/setting.default.yaml`

```python
from pyconfig_util.config_util import setting
DATABASE_HOST = setting.DATABASE_HOST
```