from typing import Dict

from kozmo_ai.api.constants import AuthorizeStatusType
from kozmo_ai.api.oauth_scope import OauthScopeType
from kozmo_ai.api.operations.constants import OperationType
from kozmo_ai.api.parsers.BaseParser import BaseParser
from kozmo_ai.shared.hash import extract


class ProjectParser(BaseParser):
    pass


async def parse_read(parser, value: Dict, **kwargs) -> Dict:
    return extract(value, ['features'])


ProjectParser.parse_read(
    parser=parse_read,
    on_action=[
        OperationType.LIST,
    ],
    on_authorize_status=[
        AuthorizeStatusType.FAILED,
    ],
    scopes=[
        OauthScopeType.CLIENT_PUBLIC,
    ],
)
