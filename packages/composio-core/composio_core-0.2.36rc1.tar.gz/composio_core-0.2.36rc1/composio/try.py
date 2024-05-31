import os
from composio.sdk import format_schema, SchemaFormat
from composio import Action, App, ComposioCore, FrameworkEnum, Tag

client = ComposioCore(framework=FrameworkEnum.OPENAI, api_key=os.environ.get("COMPOSIO_API_KEY"))

from pprint import pprint

schemas = client.sdk.get_list_of_actions(
    apps = [App.MATHEMATICAL],
    actions=[Action.ASANA_ATTACHMENTS_GET_ATTACHMENT_RECORD, Action.ZOOM_CLOUD_RECORDING_UPDATE_SETTINGS],
)

entity = client.sdk.get_entity("default")

entity.execute_action(action = Action.MATHEMATICAL_CLACULATOR, params = {"operation": "200*7"})

print(len(schemas))
pprint(schemas)