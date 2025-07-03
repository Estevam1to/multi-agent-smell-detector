# Script Pylint para Comparação com Multi-Agent System

Este script executa o Pylint e gera um CSV com os mesmos code smells detectados pelo agente estático do sistema multi-agente.

## Code Smells Detectados

O script foca especificamente nos seguintes code smells:

- **R0902 - God Class** (too-many-instance-attributes): Classes com muitas responsabilidades
- **R0915 - Long Method** (too-many-statements): Métodos muito longos
- **R0912 - Too Many Branches** (too-many-branches): Muitas ramificações condicionais
- **R0913 - Too Many Arguments** (too-many-arguments): Muitos parâmetros em funções

## Uso

### Analisar um arquivo específico:
```bash
python src/scripts/run_pylint_script.py arquivo.py -o results/resultados.csv
```

### Analisar um diretório inteiro:
```bash
python src/scripts/run_pylint_script.py src/ -o results/resultados_src.csv
```

### Analisar arquivos de teste:
```bash
python src/scripts/run_pylint_script.py code-tests/ -o results/resultados_testes.csv
```

## Formato do CSV

O CSV gerado contém as seguintes colunas:

- **file**: Caminho do arquivo onde o code smell foi encontrado
- **type**: Tipo do code smell (God Class, Long Method, etc.)
- **message_id**: Código do Pylint (R0902, R0915, etc.)
- **description**: Descrição detalhada do problema
- **risk**: Explicação do risco associado ao code smell
- **line**: Número da linha onde o problema foi encontrado
- **column**: Número da coluna
- **symbol**: Símbolo/nome do elemento problemático
- **obj**: Objeto onde o problema foi encontrado

## Exemplo de Saída

```csv
file,type,message_id,description,risk,line,column,symbol,obj
code-tests/teste_1.py,God Class,R0902,Too many instance attributes (8/7),Classes with too many responsibilities violate Single Responsibility Principle and are hard to maintain,3,0,too-many-instance-attributes,UserManager
code-tests/teste_1.py,Too Many Arguments,R0913,Too many arguments (8/5),Too many parameters make functions difficult to invoke test and understand,4,4,too-many-arguments,UserManager.__init__
```

## Comparação com o Sistema Multi-Agente

Este script permite comparar os resultados do Pylint tradicional com o sistema multi-agente, mantendo consistência nos tipos de code smells detectados. O formato JSON retornado pelo agente é diferente, mas os code smells detectados são equivalentes.
