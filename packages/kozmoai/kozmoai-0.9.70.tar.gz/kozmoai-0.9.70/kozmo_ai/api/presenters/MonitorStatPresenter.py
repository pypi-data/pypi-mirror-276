from kozmo_ai.api.presenters.BasePresenter import BasePresenter


class MonitorStatPresenter(BasePresenter):
    default_attributes = [
        'stats_type',
        'stats',
    ]
