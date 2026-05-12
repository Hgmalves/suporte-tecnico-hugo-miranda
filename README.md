# Suporte Tecnico Hugo Miranda

Ferramenta de suporte, diagnostico e manutencao para Windows, desenvolvida em Python para apoiar rotinas de atendimento tecnico, help desk e manutencao preventiva.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Licenca](https://img.shields.io/badge/Licenca-MIT-green)

## Visao geral

O projeto centraliza comandos comuns de suporte tecnico em um menu simples no terminal. A proposta e reduzir tempo em atendimentos repetitivos, padronizar verificacoes e facilitar a geracao de diagnosticos basicos em computadores Windows.

O script foi pensado para uso por tecnicos autorizados. Algumas acoes podem alterar configuracoes do sistema, reiniciar servicos, limpar caches ou executar ferramentas nativas de reparo do Windows.

## Funcionalidades

- Limpeza de arquivos temporarios.
- Limpeza de cache DNS.
- Reset completo de rede.
- Visualizacao da configuracao de IP.
- Acesso rapido a ferramentas do sistema Windows.
- Verificacao do sistema com `sfc /scannow`.
- Verificacao de disco com `chkdsk`.
- Reparo da imagem do Windows com `DISM`.
- Teste de conexao.
- Reset do Windows Update.
- Listagem de portas abertas, processos e usuarios logados.
- Diagnostico completo com geracao de relatorio.
- Pacotes de manutencao para executar varias tarefas em sequencia.

## Requisitos

| Requisito | Detalhe |
| --- | --- |
| Sistema operacional | Windows 10 ou Windows 11 |
| Python | 3.8 ou superior |
| Permissoes | Administrador recomendado |

## Como usar

Clone o repositorio:

```powershell
git clone https://github.com/Hgmalves/suporte-tecnico-hugo-miranda.git
cd suporte-tecnico-hugo-miranda
```

Execute o script:

```powershell
python suporte_tecnico.py
```

Para melhor resultado, abra o PowerShell ou Prompt de Comando como Administrador antes de executar.

## Geracao de executavel

Opcionalmente, voce pode gerar um executavel com PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --onefile --console suporte_tecnico.py
```

O executavel sera criado na pasta `dist/`, que fica fora do versionamento por padrao.

## Estrutura do projeto

```text
.
|-- suporte_tecnico.py   # Script principal
|-- README.md            # Documentacao do projeto
|-- LICENSE              # Licenca MIT
|-- CHANGELOG.md         # Historico de alteracoes
|-- SECURITY.md          # Orientacoes de seguranca
`-- .gitignore           # Arquivos ignorados pelo Git
```

## Observacoes de seguranca

- Use somente em computadores proprios ou em equipamentos onde voce tenha autorizacao.
- Revise as opcoes antes de executar acoes de reparo, reset ou limpeza.
- Mantenha backups quando estiver atuando em maquinas de producao.
- Nao publique logs ou relatorios que possam conter nomes de usuarios, configuracoes internas ou dados do ambiente.

Arquivos gerados, executaveis, pacotes externos, logs e relatorios foram adicionados ao `.gitignore` para reduzir risco de publicacao acidental.

## Roadmap

- Melhorar mensagens de erro e validacoes.
- Separar funcoes por modulos.
- Adicionar modo de diagnostico sem alteracoes no sistema.
- Criar testes para funcoes que nao dependem diretamente do Windows.

## Autor

Desenvolvido por Hugo Miranda - Suporte.

## Licenca

Este projeto esta licenciado sob os termos da licenca MIT. Consulte o arquivo [LICENSE](LICENSE).
