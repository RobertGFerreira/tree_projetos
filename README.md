# 📁 Gerador de Árvore de Diretórios

> **Ferramenta gráfica para gerar representações visuais de estruturas de pastas** - Interface intuitiva em Tkinter para explorar diretórios e exportar árvores em formato texto ou Markdown com ícones.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-Included-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🏃‍♂️ Como Usar](#️-como-usar)
- [📋 Requisitos](#-requisitos)
- [🚀 Instalação](#-instalação)
- [🤝 Contribuindo](#-contribuindo)

---

## 🎯 Sobre o Projeto

O **Gerador de Árvore de Diretórios** é uma aplicação desktop desenvolvida em Python com Tkinter que permite explorar estruturas de pastas de forma interativa e gerar representações visuais em diferentes formatos.

### 🎯 Objetivos Principais

- **Exploração Visual**: Interface gráfica para navegar por diretórios
- **Filtragem Inteligente**: Seleção de extensões de arquivo específicas
- **Exportação Flexível**: Geração de árvores em texto puro ou Markdown com ícones
- **Prévia em Tempo Real**: Visualização imediata das mudanças

### 🏗️ Arquitetura

O projeto é organizado de forma simples e modular:

```
📁 Tree_estrutura/
├── 📄 diretorios.py    # Aplicação principal
└── 📄 README.md        # Esta documentação
```

---

## ✨ Funcionalidades

### 🗂️ Exploração de Diretórios

- ✅ **Seleção de Pasta**: Escolha qualquer diretório do sistema
- ✅ **Árvore Interativa**: Visualização hierárquica com checkboxes para seleção
- ✅ **Navegação**: Expansão/colapso de pastas

### 📄 Filtragem de Arquivos

- ✅ **Seleção de Extensões**: Checkboxes para escolher tipos de arquivo
- ✅ **Selecionar Todos**: Opção para marcar/desmarcar todas as extensões
- ✅ **Contagem**: Exibe quantidade de arquivos por extensão

### 📊 Geração de Árvores

- ✅ **Prévia em Tempo Real**: Atualização automática da visualização
- ✅ **Riscos Completos**: Estrutura com ├──, └──, │ para navegação clara
- ✅ **Numeração de Linhas**: Facilita referência em documentos

### 💾 Exportação

- ✅ **Formato TXT**: Árvore pura em texto com riscos
- ✅ **Formato Markdown**: Versão com ícones (📁 para pastas, 📄 para arquivos)
- ✅ **Abertura Automática**: Arquivo gerado abre automaticamente no sistema

---

## 🏃‍♂️ Como Usar

### 🚀 Execução Básica

1. **Execute o script**:
   ```bash
   python diretorios.py
   ```

2. **Selecione um diretório**:
   - Clique em "Procurar..." para escolher a pasta raiz
   - A árvore de diretórios será carregada automaticamente

3. **Configure filtros**:
   - Marque/desmarque pastas na árvore à esquerda
   - Selecione extensões de arquivo desejadas
   - Use "Selecionar Todas as Extensões" para alternar rapidamente

4. **Visualize a prévia**:
   - A prévia é atualizada automaticamente
   - Veja a estrutura com riscos e numeração

5. **Exporte o resultado**:
   - **"Gerar TXT"**: Salva em formato texto puro
   - **"Gerar Markdown"**: Salva com ícones e formatação Markdown

### 📋 Exemplo de Saída

**TXT:**

```text
   1 lib/features/
   2 ├── menu_configuracao/
   3 │   └── parametros_cultura/
   4 │       ├── controllers/
   5 │       ├── models/
   6 │       ├── presenter/
   7 │       └── bindings/
   8 ├── menu_gerenciamento/
   9 ├── menu_mapa/
  10 ├── menu_relatorios/
  11 └── menu_dashboard/
```

**Markdown:**

```text
# 📁 lib/features/
├── 📁 menu_configuracao/
│   └── 📁 parametros_cultura/
│       ├── 📁 controllers/
│       ├── 📁 models/
│       ├── 📁 presenter/
│       └── 📁 bindings/
├── 📁 menu_gerenciamento/
├── 📁 menu_mapa/
├── 📁 menu_relatorios/
└── 📁 menu_dashboard/
```

---

---

## 📋 Requisitos

- **Python 3.8+**: Linguagem principal
- **Tkinter**: Interface gráfica (incluído no Python padrão)
- **pathlib**: Manipulação de caminhos (incluído no Python 3.4+)

### 🔍 Verificação de Dependências

Execute este comando para verificar se tudo está instalado:

```bash
python -c "import tkinter; import pathlib; print('Todas as dependências estão OK!')"
```

---

---

## 🚀 Instalação

### 📥 Download

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/RobertGFerreira/tree_projetos.git
   cd tree_projetos
   ```

2. **Execute diretamente** (não há instalação necessária):

   ```bash
   python diretorios.py
   ```

### 🐧 Linux/Mac

Certifique-se de que o Tkinter está instalado:

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS (com Homebrew)
brew install python-tk

# Fedora/CentOS
sudo dnf install python3-tkinter
```

---

---

## 🤝 Contribuindo

### 📋 Processo de Contribuição

1. **Fork** o projeto
2. **Clone** seu fork: `git clone https://github.com/seu-usuario/tree_projetos.git`
3. **Crie uma branch**: `git checkout -b feature/sua-melhoria`
4. **Desenvolva** seguindo os padrões Python
5. **Teste** suas mudanças
6. **Commit**: `git commit -m "feat: descrição da melhoria"`
7. **Push**: `git push origin feature/sua-melhoria`
8. **Abra um PR** com descrição detalhada

### 💡 Sugestões de Melhorias

- **Interface**: Melhorar design e usabilidade
- **Formatos**: Adicionar exportação em HTML ou JSON
- **Funcionalidades**: Busca, filtros avançados, temas
- **Performance**: Otimização para diretórios muito grandes

### 🐛 Reportando Bugs

Para relatar problemas:

- Descreva o bug claramente
- Inclua passos para reproduzir
- Informe seu sistema operacional e versão Python
- Anexe screenshots se possível

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

*⭐ Se este projeto foi útil para você, considere dar uma estrela!* 🚀
