# Suporte Tecnico Hugo Miranda

Ferramenta de suporte e manutencao para Windows, feita em Python, com um menu interativo para tecnicos de TI executarem tarefas comuns de diagnostico, limpeza e reparacao.

![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Licenca](https://img.shields.io/badge/Licenca-MIT-green)

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

Clone o repositorio ou baixe o arquivo `suporte_tecnico.py`.

```powershell
python suporte_tecnico.py
```

Algumas funcoes precisam de permissao de Administrador. Execute o PowerShell ou Prompt de Comando como Administrador para obter o melhor resultado.

## Geracao de executavel

Opcionalmente, voce pode gerar um executavel com PyInstaller:

```powershell
pip install pyinstaller
pyinstaller --onefile --console suporte_tecnico.py
```

O executavel sera criado na pasta `dist/`, que fica fora do versionamento por padrao.

## Observacoes de seguranca

Use esta ferramenta apenas em computadores proprios ou em equipamentos onde voce tenha autorizacao para realizar manutencao. Algumas opcoes alteram configuracoes de rede, servicos do Windows ou executam reparos do sistema.

Arquivos gerados, executaveis, pacotes externos, logs e relatorios foram adicionados ao `.gitignore` para evitar publicacao acidental.

## Autor

Desenvolvido por Hugo Miranda - Suporte.

## Licenca

Este projeto esta licenciado sob os termos da licenca MIT. Consulte o arquivo [LICENSE](LICENSE).

