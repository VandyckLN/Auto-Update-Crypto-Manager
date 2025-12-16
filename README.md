# Auto-Update-Crypto-Manager

Este repositório contém dois scripts Python úteis para uso no dia a dia: um atualizador automático de sistemas Linux e um gerenciador de criptografia seguro.

## 📋 Índice

- [Descrição](#descrição)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Auto Update](#auto-update)
  - [Crypto Manager](#crypto-manager)
- [Exemplos](#exemplos)
- [Segurança](#segurança)
- [Licença](#licença)

## 📖 Descrição

Este projeto fornece duas ferramentas essenciais:

1. **auto_update.py**: Automatiza o processo de atualização do sistema Linux, detectando automaticamente o gerenciador de pacotes (apt, dnf ou pacman) e realizando atualizações completas do sistema.

2. **crypto_manager.py**: Gerenciador de criptografia que permite criptografar e descriptografar arquivos de forma segura usando AES-256 com derivação de chave baseada em senha.

## ✨ Funcionalidades

### Auto Update
- ✅ Detecção automática do gerenciador de pacotes
- ✅ Suporte para apt (Debian/Ubuntu)
- ✅ Suporte para dnf (Fedora/RHEL)
- ✅ Suporte para pacman (Arch Linux)
- ✅ Registro detalhado de operações (logs)
- ✅ Limpeza automática de pacotes desnecessários
- ✅ Verificação de privilégios de root

### Crypto Manager
- ✅ Criptografia AES-256-CBC
- ✅ Derivação de chave PBKDF2 com SHA-256
- ✅ Interface de linha de comando intuitiva
- ✅ Prompt seguro de senha (sem exibição no terminal)
- ✅ Confirmação de senha ao criptografar
- ✅ Verificação de integridade
- ✅ Proteção contra sobrescrita acidental

## 🔧 Requisitos

- Python 3.6 ou superior
- Sistema operacional Linux (para auto_update.py)
- Privilégios de root/sudo (para auto_update.py)

## 📦 Instalação

1. Clone este repositório:
```bash
git clone https://github.com/VandyckLN/Auto-Update-Crypto-Manager.git
cd Auto-Update-Crypto-Manager
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Torne os scripts executáveis (opcional):
```bash
chmod +x auto_update.py crypto_manager.py
```

## 🚀 Uso

### Auto Update

O script de atualização automática requer privilégios de root:

```bash
sudo python3 auto_update.py
```

ou, se tornado executável:

```bash
sudo ./auto_update.py
```

O script irá:
1. Detectar automaticamente seu gerenciador de pacotes
2. Atualizar a lista de pacotes
3. Atualizar todos os pacotes instalados
4. Remover pacotes desnecessários
5. Limpar o cache de pacotes
6. Registrar todas as operações em `~/auto_update.log`

### Crypto Manager

#### Criptografar um arquivo:

```bash
python3 crypto_manager.py encrypt arquivo.txt arquivo.txt.enc
```

O script solicitará:
- Senha (mínimo 8 caracteres)
- Confirmação da senha

#### Descriptografar um arquivo:

```bash
python3 crypto_manager.py decrypt arquivo.txt.enc arquivo_descriptografado.txt
```

O script solicitará a senha usada na criptografia.

#### Ajuda:

```bash
python3 crypto_manager.py --help
```

## 📚 Exemplos

### Exemplo 1: Atualizar o sistema

```bash
$ sudo python3 auto_update.py

============================================================
Linux System Auto-Updater
Package Manager: apt
Started at: 2024-12-16 15:30:00
============================================================

[Log entries...]

============================================================
✓ System update completed successfully!
Finished at: 2024-12-16 15:35:00
============================================================
```

### Exemplo 2: Criptografar um documento

```bash
$ python3 crypto_manager.py encrypt documento.pdf documento.pdf.enc

============================================================
Crypto Manager - Encrypting File
============================================================
Input:  documento.pdf
Output: documento.pdf.enc
============================================================

Enter password: ********
Confirm password: ********
✓ File encrypted successfully: documento.pdf.enc
```

### Exemplo 3: Descriptografar um documento

```bash
$ python3 crypto_manager.py decrypt documento.pdf.enc documento_restaurado.pdf

============================================================
Crypto Manager - Decrypting File
============================================================
Input:  documento.pdf.enc
Output: documento_restaurado.pdf
============================================================

Enter password: ********
✓ File decrypted successfully: documento_restaurado.pdf
```

## 🔒 Segurança

### Crypto Manager

- **Algoritmo**: AES-256-CBC (Advanced Encryption Standard com chave de 256 bits)
- **Derivação de chave**: PBKDF2 com SHA-256 (100.000 iterações)
- **Salt**: Aleatório de 16 bytes (único para cada arquivo)
- **IV**: Aleatório de 16 bytes (único para cada arquivo)
- **Padding**: PKCS7

**Importante**: 
- Use senhas fortes e únicas
- Mantenha suas senhas em segurança
- Faça backup de arquivos importantes antes de criptografar
- Perder a senha significa perder o acesso aos dados criptografados

### Auto Update

- Requer privilégios de root/sudo
- Registra todas as operações
- Verifica a integridade dos pacotes através do gerenciador de pacotes

## 📝 Licença

Este projeto está disponível sob a licença MIT. Sinta-se livre para usar, modificar e distribuir conforme necessário.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 👨‍💻 Autor

VandyckLN

## ⚠️ Aviso Legal

Estes scripts são fornecidos "como estão", sem garantias de qualquer tipo. Use por sua conta e risco. Sempre faça backup de dados importantes antes de usar ferramentas de criptografia ou atualização de sistema.