# Guia rapido para publicar no GitHub

## 1. Instalar Git

O Git nao foi encontrado neste computador. Instale pelo site oficial:

https://git-scm.com/download/win

Depois de instalar, feche e abra novamente o PowerShell.

## 2. Criar o repositorio no GitHub

1. Acesse https://github.com/new
2. Nome sugerido: `suporte-tecnico-hugo-miranda`
3. Descricao sugerida: `Ferramenta Python para diagnostico e manutencao de computadores Windows`
4. Escolha `Public`
5. Nao marque para criar README, .gitignore ou LICENSE, pois estes arquivos ja existem aqui.

## 3. Enviar os arquivos

No PowerShell, dentro desta pasta, rode:

```powershell
git init
git add README.md LICENSE .gitignore PUBLICAR_NO_GITHUB.md suporte_tecnico.py
git commit -m "Publica versao inicial do suporte tecnico"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/suporte-tecnico-hugo-miranda.git
git push -u origin main
```

Troque `SEU-USUARIO` pelo seu usuario do GitHub.

## 4. Antes de publicar

Confira se apenas os arquivos desejados serao enviados:

```powershell
git status
```

Evite publicar executaveis, arquivos `.zip`, pastas `build/`, `dist/`, logs, relatorios e ferramentas de terceiros.

