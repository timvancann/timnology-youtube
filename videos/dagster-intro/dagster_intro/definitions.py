import importlib

module = importlib.import_module("dagster_intro.06_partitions")
definitions = getattr(module, "definitions")


defs = definitions()
