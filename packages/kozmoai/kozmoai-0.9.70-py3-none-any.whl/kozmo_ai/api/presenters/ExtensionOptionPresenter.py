from kozmo_ai.api.presenters.BasePresenter import BasePresenter


class ExtensionOptionPresenter(BasePresenter):
    default_attributes = [
        'description',
        'name',
        'templates',
        'uuid',
    ]
