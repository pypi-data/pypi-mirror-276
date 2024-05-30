from typing import Final, Literal

__ERR_MSGS: Final[dict] = {
    101: {
        "en": "Error accessing the DB {} in {}: {}",
        "pt": "Erro na interação com o BD {} em {}: {}",
    },
    102: {
        "en": "No record found on DB in {}, for {}",
        "pt": "Nenhum registro encontrado no BD, em {} para {}",
    },
    103: {
        "en": "Error accessing the object store: {}",
        "pt": "Erro na interação com o armazenador de objetos: {}",
    },
    104: {
        "en": "Unexpected error: {}",
        "pt": "Error não previsto: {}",
    },
    105: {
        "en": "Invalid operation {}",
        "pt": "Operação {} inválida",
    },
    106: {
        "en": "The operation {} returned the error {}",
        "pt": "A operação {} retornou o erro {}",
    },
    107: {
        "en": "Error invoking service {}: {}",
        "pt": "Erro na invocação do serviço {}: {}",
    },
    108: {
        "en": "Authentication token required",
        "pt": "Token de autenticação deve ser fornecido",
    },
    109: {
        "en": "Invalid authentication token",
        "pt": "Token de autenticação inválido",
    },
    110: {
        "en": "{}",
        "pt": "{}",
    },
    111: {
        "en": "Attribute is unknown or invalid in this context",
        "pt": "Atributo desconhecido ou inválido para o contexto",
    },
    112: {
        "en": "Required attribute",
        "pt": "Atributo obrigatório",
    },
    113: {
        "en": "Attribute not applicable for {}",
        "pt": "Atributo não se aplica a {}",
    },
    114: {
        "en": "Attribute applicable only for {}",
        "pt": "Atributo se aplica apenas a {}",
    },
    115: {
        "en": "A value has not yet been assigned",
        "pt": "Valor ainda não foi atribuído",
    },
    116: {
        "en": "Value {} cannot be assigned for attributes {} at the same time",
        "pt": "Valor {} não pode ser atribuído aos atributos {} ao mesmo tempo",
    },
    117: {
        "en": "Invalid value {}: must be less than {}",
        "pt": "Valor {} inválido: deve ser menor que {}",
    },
    118: {
        "en": "Invalid value {}: must be greater than {}",
        "pt": "Valor {} inválido: deve ser maior que {}",
    },
    119: {
        "en": "Invalid value {}: {}",
        "pt": "Valor {} inválido: {}",
    },
    120: {
        "en": "Invalid, inconsistent, or missing arguments",
        "pt": "Argumento(s) inválido(s), inconsistente(s) ou não fornecido(s)",
    },
    121: {
        "en": "Invalid value {}",
        "pt": "Valor {} inválido",
    },
    122: {
        "en": "Invalid value {}: length shorter than {}",
        "pt": "Valor {} inválido: comprimento menor que {}",
    },
    123: {
        "en": "Invalid value {}: length longer than {}",
        "pt": "Valor {} inválido: comprimento maior que {}",
    },
    124: {
        "en": "Invalid value {}: length must be {}",
        "pt": "Valor {} inválido: comprimento deve ser {}",
    },
    125: {
        "en": "Invalid value {}: must be {}",
        "pt": "Valor {} inválido: deve ser {}",
    },
    126: {
        "en": "Invalid value {}: must be one of {}",
        "pt": "Valor {} inválido: deve ser um de {}",
    },
    127: {
        "en": "Invalid value {}: must be in the range {}",
        "pt": "Valor {} inválido: deve estar no intervalo {}",
    },
    128: {
        "en": "Invalid value {}: must be type {}",
        "pt": "Valor {} inválido: deve ser do tipo {}",
    },
    129: {
        "en": "Invalid value {}: date is later than the current date",
        "pt": "Valor {} inválido: data posterior à data atual",
    },
    130: {
        "en": "No records matching the provided criteria found",
        "pt": "Não foram encontrados registros para os critérios fornecidos",
    },
}

_ERR_MSGS_EN: dict = {}
for key, value in __ERR_MSGS.items():
    _ERR_MSGS_EN[key] = value["en"]

_ERR_MSGS_PT: dict = {}
for key, value in __ERR_MSGS.items():
    _ERR_MSGS_PT[key] = value["pt"]


def validate_add_msgs(msgs: dict,
                      lang: Literal["en", "pt"] = "en") -> None:
    """
    Add the messages in *msgs* to the standard validation messages list for language *lang".

    If applicable, this operation should be performed at the start of the application importing this module,
    before any attempt to read from *_ERR_MSGS_EN* or *_ERR_MSGS_PT*.

    :param msgs: list of messages to be added
    :param lang: the reference language
    """
    match lang:
        case "en":
            _ERR_MSGS_EN.update(msgs)
        case "pt":
            _ERR_MSGS_PT.update(msgs)


def validate_set_msgs(msgs: dict,
                      lang: Literal["en", "pt"] = "en") -> None:
    """
    Set  the standard validation messages list for language *lang* to the messages in *msgs*.

    If applicable, this operation should be performed at the start of the application importing this module,
    before any attempt to read from *_ERR_MSGS_EN* or *_ERR_MSGS_PT*.

    :param msgs: list of messages to set the standard validation messages to
    :param lang: the reference language
    """
    global _ERR_MSGS_EN, _ERR_MSGS_PT

    match lang:
        case "en":
            _ERR_MSGS_EN = msgs
        case "pt":
            _ERR_MSGS_PT = msgs
