from kozmo_ai.api.presenters.BasePresenter import BasePresenter
from kozmo_ai.api.presenters.mixins.users import AssociatedUserPresenter


class SessionPresenter(BasePresenter, AssociatedUserPresenter):
    default_attributes = [
        'expires',
        'token',
        'user',
    ]
