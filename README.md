# Chainlit Train
Este repositório é uma prova de conceito (POC) do uso da ferramenta ChainLit com modelos de LLM.

Para esta abordagem, é utilizado modelos do Ollama rodando localmente.

## Rodando o projeto

### Ferramentas exigidas
```
docker --version
docker compose version
rocm-smi                    # só se for usar GPU AMD
```

### Primeira vez
Lembre-se de alteraar as variáveis de ambiente
```
cp .env.example .env
docker compose up --build
```

### Executando
```
docker compose up
```

## Variáveis de ambiente
- OLLAMA_MODEL: Nome do modelo desejado
- OLLAMA_HOST: Host e porta do Ollama (geralmente é fixo)
- GPU_TYPE & OLLAMA_IMAGE_TAG: Configurações para rodar o Ollama em GPUs, use as sugestões dos comentários