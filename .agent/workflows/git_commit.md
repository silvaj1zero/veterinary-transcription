---
description: Automatizar controle de versão e commit no GitHub
---

Este workflow automatiza o processo de commit, incluindo verificação de status, adição de arquivos, commit e atualização opcional de versão.

1.  **Verificar Status do Git**
    Execute o comando para ver o que mudou:
    ```bash
    git status
    ```

2.  **Adicionar Arquivos**
    Adicione todos os arquivos modificados (ou especifique se necessário):
    ```bash
    git add .
    ```

3.  **Realizar Commit**
    Solicite ao usuário uma mensagem de commit descritiva e execute:
    ```bash
    git commit -m "Sua mensagem aqui"
    ```

4.  **Verificar Necessidade de Atualização de Versão**
    Pergunte ao usuário se deseja atualizar a versão do projeto (Patch, Minor ou Major).
    Se SIM:
    a.  Leia a versão atual (pode estar em `README.md` ou `config.py`).
    b.  Calcule a nova versão.
    c.  Atualize `README.md` e outros arquivos onde a versão aparece.
    d.  Adicione uma entrada no `CHANGELOG.md` com a data e as mudanças do commit atual.
    e.  Faça um novo commit para a atualização de versão:
        ```bash
        git add .
        git commit -m "chore: bump version to X.Y.Z"
        ```

5.  **Push para o GitHub**
    Envie as alterações para o repositório remoto:
    ```bash
    git push
    ```

6.  **Confirmação**
    Confirme que tudo foi enviado com sucesso.
