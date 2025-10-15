# Estrutura de Agentes - Multi-Agent Code Smell Detector

## Organização

A estrutura de agentes foi organizada de forma modular e escalável:

```
src/agents/
│
├── __init__.py                              # Exports públicos
├── base/                                    # Classes base
│   ├── __init__.py
│   ├── agent_base.py                        # Classe abstrata base
│   └── agent_factory.py                     # Factory para criar agentes (TODO)
│
├── prompts/                                 # Prompts separados (manutenção)
│   ├── __init__.py
│   ├── long_method_prompt.py
│   └── long_parameter_list_prompt.py
│
├── specialized/                             # Agentes especializados
│   ├── __init__.py
│   ├── complexity/                          # Grupo: Complexidade
│   │   ├── __init__.py
│   │   └── long_method_agent.py
│   │
│   ├── structure/                           # Grupo: Estrutura
│   │   ├── __init__.py
│   │   └── long_parameter_list_agent.py
│   │
│   ├── naming/                              # Grupo: Nomenclatura (TODO)
│   │   └── __init__.py
│   │
│   └── statements/                          # Grupo: Statements (TODO)
│       └── __init__.py
│
├── supervisor/                              # Supervisor (TODO)
│   └── __init__.py
│
└── utils/                                   # Utilidades
    ├── __init__.py
    ├── agent_config.py                      # Configurações
    └── agent_registry.py                    # Registro de agentes
```

## Próximos Passos

- [ ] Implementar AgentFactory
- [ ] Implementar SupervisorAgent
- [ ] Adicionar agentes de naming
- [ ] Adicionar agentes de statements
- [ ] Implementar sistema de caching
- [ ] Adicionar métricas e monitoramento