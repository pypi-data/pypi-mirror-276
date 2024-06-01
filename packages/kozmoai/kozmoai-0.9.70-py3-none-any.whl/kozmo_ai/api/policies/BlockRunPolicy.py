from kozmo_ai.api.oauth_scope import OauthScope
from kozmo_ai.api.operations import constants
from kozmo_ai.api.policies.BasePolicy import BasePolicy
from kozmo_ai.api.presenters.BlockRunPresenter import BlockRunPresenter
from kozmo_ai.orchestration.constants import Entity


class BlockRunPolicy(BasePolicy):
    @property
    def entity(self):
        query = self.options.get('query', {})
        pipeline_uuid = query.get('pipeline_uuid', [None])
        if pipeline_uuid:
            pipeline_uuid = pipeline_uuid[0]
        if pipeline_uuid:
            return Entity.PIPELINE, pipeline_uuid

        parent_model = self.options.get('parent_model')
        if parent_model:
            return Entity.PIPELINE, parent_model.pipeline_uuid

        return super().entity


BlockRunPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

BlockRunPolicy.allow_read(BlockRunPresenter.default_attributes + [], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())

BlockRunPolicy.allow_query([
    'order_by',
    'pipeline_run_id',
    'pipeline_uuid',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
