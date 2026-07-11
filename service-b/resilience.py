import pybreaker
import logging

# Configuração do disjuntor
service_c_breaker = pybreaker.CircuitBreaker(fail_max=3, reset_timeout=30)
logger = logging.getLogger("uvicorn")

# Listener para monitorar mudanças de estado
class CircuitBreakerListener(pybreaker.CircuitBreakerListener):
    def state_change(self, cb, old_state, new_state):
        logger.info(f"Circuit Breaker mudou de {old_state.name} para {new_state.name}")
        if new_state.name == "open":
            logger.error("!!! CIRCUITO ABERTO: Serviço C indisponível. Entrando em modo de proteção.")

# Registra o ouvinte no disjuntor
service_c_breaker.add_listener(CircuitBreakerListener())
