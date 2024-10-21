import typing as _typing

_Action = _typing.Union[_typing.Literal['cooperate'], _typing.Literal['nothing'], _typing.Literal['cheat']]

def act( action: _typing.Literal['cooperate'] | _typing.Literal['nothing'] | _typing.Literal['cheat'] ) -> None:
    """ Run an action for this round """

def cooperate() -> None:
    """ Choose to cooperate for this round """

def nothing() -> None:
    """ Choose not to cooperate for this round """

def cheat() -> None:
    """ Choose to cheat for this round """

def getTurn() -> int:
    """ Get the current turn number """
    
def getAction(n: int) -> _Action:
    """ Get the n-th action from opponent """
    
def getSelf(n: int) -> _Action:
    """ Get the n-th action from self """
