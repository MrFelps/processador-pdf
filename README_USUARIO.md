# Guia de Uso Simplificado: Renomeador Automático de PDFs

Este guia explica como configurar e usar a ferramenta de renomeação de PDFs em um computador que já possui os programas necessários instalados.

## Pré-requisitos Essenciais

Para que o programa funcione, seu computador **obrigatoriamente** precisa ter os seguintes softwares já instalados e configurados:

* ✅ **Python** (versão 3.9 ou superior)
* ✅ **Tesseract OCR**
* ✅ **Poppler**

> **Atenção:** Este guia не cobre a instalação desses três programas. Se ocorrerem erros durante o uso, a causa mais provável é a ausência ou má configuração de um desses pré-requisitos.

---

## Parte 1: Configuração do Projeto (Feito Apenas Uma Vez)

Siga estes 3 passos para deixar o programa pronto para o uso.

### Passo 1: Baixar o Projeto
1.  Acesse a página do projeto no GitHub: `[COLOQUE O LINK DO SEU REPOSITÓRIO AQUI]`
2.  Clique no botão verde **"< > Code"** e depois em **"Download ZIP"**.
3.  Salve o arquivo e **descompacte a pasta** em um local de fácil acesso (ex: na sua Área de Trabalho).

### Passo 2: Instalar as Dependências do Projeto
Dentro da pasta que você descompactou, você encontrará um arquivo chamado `setup.bat`.
1.  Dê um **duplo-clique** no arquivo **`setup.bat`**.
2.  Uma tela preta aparecerá e instalará as bibliotecas específicas do projeto. Aguarde até que ela mostre a mensagem "Setup Concluído!" e se feche sozinha.

## Parte 2: Como Usar no Dia a Dia

Com o projeto configurado, o uso diário é muito simples.

### Passo 1: Adicionar os PDFs
* Abra a pasta do projeto e encontre a subpasta chamada **`meus_pdfs`**.
* Copie e cole todos os arquivos PDF que você deseja renomear para dentro desta pasta.

### Passo 2: Executar o Programa
* Na pasta principal do projeto, dê um **duplo-clique** no arquivo **`EXECUTAR.bat`**.
* Uma tela preta aparecerá, mostrando o progresso do trabalho em tempo real.

### Passo 3: Pegar os Arquivos Prontos
* Quando o processamento terminar, a tela preta mostrará o relatório final e a mensagem "Pressione qualquer tecla para continuar...".
* Você pode fechar a tela.
* Seus arquivos renomeados estarão na pasta **`pdfs_renomeados`**. Lá também estará um arquivo `.zip` com uma cópia de tudo.

Para processar novos arquivos, basta repetir os passos da **Parte 2**.
