# Suporte Tecnico Hugo Miranda

Ferramenta de suporte, diagnostico e manutencao para Windows, desenvolvida em Python para apoiar rotinas de atendimento tecnico, help desk e manutencao preventiva.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Versao](https://img.shields.io/badge/Versao-2.3-green)
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
- Verificacao de compatibilidade do ambiente.
- Registro de logs de execucao.
- Modo teste para reduzir risco em acoes destrutivas.
- Ajuda de recuperacao de acesso usando caminhos oficiais.
- Consulta de licenciamento do Windows com ferramentas oficiais.

## Atualizacao 2.3

Esta versao substitui a versao inicial publicada no GitHub e traz uma base mais completa para uso tecnico.

| Area | Versao anterior | Versao 2.3 |
| --- | --- | --- |
| Administrador | Reiniciava como administrador de forma direta | Pergunta antes de reiniciar como administrador |
| Seguranca operacional | Executava algumas rotinas diretamente | Usa `MODO_TESTE` para simular acoes destrutivas por padrao |
| Logs | Sem log centralizado | Cria logs em `logs/` com historico da execucao |
| Relatorios | Relatorio mais simples | Relatorios salvos em `relatorios/` com resumo e detalhes |
| Compatibilidade | Nao havia tela dedicada | Nova opcao `C` para verificar ambiente, internet, PowerShell e permissoes |
| Recuperacao de acesso | Nao havia modulo dedicado | Nova opcao com links e passos oficiais, sem bypass de senha |
| Licenciamento | Nao havia orientacao separada | Consulta status com `slmgr` e abre configuracoes oficiais do Windows |
| Publicacao no GitHub | Base inicial | Versao preparada para repositorio publico, sem scripts externos de ativacao |

Por seguranca e profissionalismo, a atualizacao publica nao executa ativadores, bypass, instalacao de chaves ou scripts externos. A opcao 18 foi mantida como orientacao oficial de ativacao/licenciamento.

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

Por padrao, a constante `MODO_TESTE` fica ativada no arquivo `suporte_tecnico.py`. Nesse modo, algumas rotinas de maior impacto simulam a operacao em vez de alterar o sistema.

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
