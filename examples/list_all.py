from mdd.modules import *

modules = get_modules()

module = modules["math"]()

print(module.to_dict())