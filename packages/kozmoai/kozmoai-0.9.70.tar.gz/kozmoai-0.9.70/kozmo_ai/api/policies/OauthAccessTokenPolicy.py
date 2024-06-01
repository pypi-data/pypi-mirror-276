from kozmo_ai.api.oauth_scope import OauthScope
from kozmo_ai.api.operations import constants
from kozmo_ai.api.policies.BasePolicy import BasePolicy
from kozmo_ai.api.presenters.OauthAccessTokenPresenter import OauthAccessTokenPresenter


class OauthAccessTokenPolicy(BasePolicy):
    pass


OauthAccessTokenPolicy.allow_actions([
    constants.LIST,
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], condition=lambda policy: policy.has_at_least_viewer_role())


OauthAccessTokenPolicy.allow_read(OauthAccessTokenPresenter.default_attributes, scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())


OauthAccessTokenPolicy.allow_query([
    'show_all',
], scopes=[
    OauthScope.CLIENT_PRIVATE,
], on_action=[
    constants.LIST,
], condition=lambda policy: policy.has_at_least_viewer_role())
