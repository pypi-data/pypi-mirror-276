from kozmo_ai.api.oauth_scope import OauthScope
from kozmo_ai.api.operations import constants
from kozmo_ai.api.policies.BasePolicy import BasePolicy
from kozmo_ai.api.presenters.FileVersionPresenter import FileVersionPresenter
from kozmo_ai.orchestration.constants import Entity


class FileVersionPolicy(BasePolicy):
    @property
    def entity(self):
        return Entity.ANY, None


FileVersionPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


FileVersionPolicy.allow_read(FileVersionPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())


FileVersionPolicy.allow_query([
  'block_uuid',
  'pipeline_uuid',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
