from kozmo_ai.api.oauth_scope import OauthScope
from kozmo_ai.api.operations import constants
from kozmo_ai.api.policies.BasePolicy import BasePolicy
from kozmo_ai.api.presenters.IntegrationSourceStreamPresenter import IntegrationSourceStreamPresenter


class IntegrationSourceStreamPolicy(BasePolicy):
    pass


IntegrationSourceStreamPolicy.allow_actions([
    constants.UPDATE,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())

IntegrationSourceStreamPolicy.allow_read(IntegrationSourceStreamPresenter.default_attributes + [
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.UPDATE,
], condition=lambda policy: policy.has_at_least_viewer_role())
