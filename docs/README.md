# Documentação - Multi-Agent Smell Detector

Esta pasta contém toda a documentação do projeto de detecção e revisão automatizada de code smells e security smells utilizando LLMs multiagentes.

## 📚 Documentos Disponíveis

### 🎓 Documentos Principais (TCC/Acadêmico)

| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[RESULTADOS_TCC.md](RESULTADOS_TCC.md)** | 📋 Documento principal sobre detecção automatizada com LLMs multiagentes | Orientadores, bancas, pesquisadores |
| **[ANALISE_ESTATISTICA.md](ANALISE_ESTATISTICA.md)** | 📊 Análise estatística rigorosa dos resultados da pesquisa | Pesquisadores, estatísticos, revisores |
| **[DETALHAMENTO_TECNICO.md](DETALHAMENTO_TECNICO.md)** | ⚙️ Implementação técnica dos agentes multiagentes | Desenvolvedores, implementadores |

### 📖 Guias Práticos

| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[EXEMPLO_COMPLETO.md](EXEMPLO_COMPLETO.md)** | 🚀 Tutorial completo passo a passo | Usuários finais, iniciantes |
| **[TESTING_AGENTS.md](TESTING_AGENTS.md)** | 🧪 Procedimentos de teste dos agentes | Desenvolvedores, testadores |

### 🔧 Documentação Técnica de Scripts

| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[README_BANDIT_SCRIPT.md](README_BANDIT_SCRIPT.md)** | 🛡️ Configuração e uso do script Bandit | Usuários do Bandit |
| **[README_PYLINT_SCRIPT.md](README_PYLINT_SCRIPT.md)** | 🔍 Configuração e uso do script Pylint | Usuários do Pylint |

## 📊 Dados e Resultados

### Resultados Principais
- **Pylint**: 22 code smells detectados
- **Bandit**: 61 vulnerabilidades detectadas  
- **Agente Estático**: 40 issues detectados (82% mais que Pylint)
- **Agente Segurança**: 56 vulnerabilidades detectadas

### Principais Descobertas
1. **Complementaridade**: Agentes de IA e ferramentas tradicionais são complementares
2. **Diversidade**: Agentes detectaram 3x mais tipos de problemas de segurança
3. **Explicabilidade**: Agentes forneceram contexto e sugestões superiores
4. **Performance**: Ferramentas tradicionais mantêm vantagem em velocidade
5. **Detecção Híbrida**: Agente estático também detectou vulnerabilidades

## 🔧 Estrutura do Projeto

```
multi-agent-smell-detector/
├── documentacao/               # 📁 Esta pasta
│   ├── README.md              # Este arquivo
│   ├── RESULTADOS_TCC.md      # Documento principal
│   ├── DETALHAMENTO_TECNICO.md # Implementação técnica
│   ├── ANALISE_ESTATISTICA.md # Análise estatística
│   └── EXEMPLO_COMPLETO.md    # Guia prático
├── src/                       # Código fonte
├── code-tests/               # Arquivos de teste
├── results/                  # Resultados gerados
└── scripts/                  # Scripts de automação
```

## 🎯 Como Usar Esta Documentação

### Para TCC/Dissertação
1. **Comece com**: `RESULTADOS_TCC.md`
2. **Aprofunde com**: `ANALISE_ESTATISTICA.md`
3. **Detalhes técnicos**: `DETALHAMENTO_TECNICO.md`

### Para Implementação
1. **Comece com**: `EXEMPLO_COMPLETO.md`
2. **Arquitetura**: `DETALHAMENTO_TECNICO.md`
3. **Validação**: `ANALISE_ESTATISTICA.md`

### Para Pesquisa Acadêmica
1. **Metodologia**: `RESULTADOS_TCC.md` (seção 2)
2. **Estatística**: `ANALISE_ESTATISTICA.md`
3. **Reprodutibilidade**: `DETALHAMENTO_TECNICO.md`

## 📈 Métricas de Qualidade

### Cobertura da Documentação
- ✅ **100%** dos resultados documentados
- ✅ **100%** dos scripts explicados
- ✅ **100%** da metodologia detalhada
- ✅ **100%** das análises estatísticas incluídas

### Rigor Científico
- ✅ Testes estatísticos adequados
- ✅ Limitações claramente expostas
- ✅ Metodologia reproduzível
- ✅ Dados abertos e transparentes

## 🤝 Contribuições

Este projeto contribui para:
1. **Framework de comparação** estruturado para análise de código
2. **Metodologia reproduzível** para avaliação de ferramentas
3. **Insights sobre complementaridade** de abordagens tradicionais e IA
4. **Base para desenvolvimento** de soluções híbridas

## 📞 Suporte

Para dúvidas sobre:
- **Uso prático**: Consulte `EXEMPLO_COMPLETO.md`
- **Implementação**: Consulte `DETALHAMENTO_TECNICO.md`
- **Metodologia**: Consulte `RESULTADOS_TCC.md` e `ANALISE_ESTATISTICA.md`

---

*Documentação gerada como parte da pesquisa de TCC sobre "Detecção e Revisão Automatizada de Code Smells e Security Smells Utilizando LLMs Multiagentes".*

**Última atualização**: 03 de Julho de 2025
**Versão**: 1.0
**Status**: Completo ✅
