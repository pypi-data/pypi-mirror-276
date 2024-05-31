from piny import MarshmallowValidator, StrictMatcher, YamlLoader
from .models import NotaConfigSchema

def load_config(path) -> NotaConfigSchema:
  return YamlLoader(
    path=path,
    matcher=StrictMatcher,
    validator=MarshmallowValidator,
    schema=NotaConfigSchema,
  ).load(many=False)
