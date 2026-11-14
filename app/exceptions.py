"""Exceções de domínio. A camada de rotas/handlers as converte em status HTTP."""


class NaoEncontradoError(Exception):
    """Recurso inexistente -> HTTP 404."""


class RegraNegocioError(Exception):
    """Violação de regra de negócio ou dado inválido -> HTTP 400."""
