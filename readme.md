# 🚀 Scripts Utilitários - Auto Update & Crypto Manager

Este repositório contém dois scripts Python úteis para uso no dia a dia: um atualizador automático de sistemas Linux e um gerenciador de criptografia seguro.

---

## 📦 Conteúdo

- **`auto.py`** - Atualizador automático de pacotes para sistemas Linux
- **`crypto.py`** - Gerenciador de criptografia usando Fernet (cryptography)

---

## 🔄 Auto.py - Atualizador Automático

### 📋 Funcionalidades

O `auto.py` é um script que automatiza a atualização de pacotes em diferentes distribuições Linux, detectando automaticamente o gerenciador de pacotes disponível.

#### **Gerenciadores Suportados:**

- 🔸 **APT** (Ubuntu, Debian, Mint) - `apt update && apt full-upgrade -y`
- 🔸 **DNF** (Fedora, RHEL 8+) - `dnf upgrade --refresh -y`
- 🔸 **Pacman** (Arch Linux, Manjaro) - `pacman -Syu --noconfirm`
- 🔸 **Zypper** (openSUSE) - `zypper refresh && zypper update -y`
- 🔸 **Flatpak** (Aplicações universais) - `flatpak update -y`
- 🔸 **Snap** (Pacotes snap) - `snap refresh`

### 🎯 Como Usar

#### **Execução Interativa:**

```bash
python3 auto.py
```

O script apresentará um menu:

```
Atualizador rápido — pressione uma letra e Enter:
 a=apt  d=dnf  p=pacman  z=zypper  f=flatpak  s=snap  x=auto-detect
>
```

#### **Opções Disponíveis:**

- **`a`** - Força uso do APT
- **`d`** - Força uso do DNF
- **`p`** - Força uso do Pacman
- **`z`** - Força uso do Zypper
- **`f`** - Atualiza apenas Flatpaks
- **`s`** - Atualiza apenas Snaps
- **`x`** - **Detecção automática** (recomendado)

### 💡 Casos de Uso Diário

1. **Manutenção Rápida:**

   ```bash
   python3 auto.py
   # Digite 'x' para detecção automática
   ```

2. **Atualização Específica:**

   ```bash
   python3 auto.py
   # Digite 'f' para atualizar só Flatpaks
   ```

3. **Automação em Scripts:**
   ```bash
   echo "x" | python3 auto.py  # Execução não-interativa
   ```

### 🔧 Recursos Técnicos

- **Detecção automática** do gerenciador de pacotes
- **Execução com sudo** quando necessário
- **Tratamento de erros** robusto
- **Suporte a múltiplos gerenciadores** no mesmo sistema

---

## 🔐 Crypto.py - Gerenciador de Criptografia

### 📋 Funcionalidades

O `crypto.py` oferece criptografia simétrica segura usando o algoritmo Fernet da biblioteca `cryptography`, com interface amigável para uso diário.

#### **Recursos Principais:**

- 🔸 **Geração de chaves** criptográficas seguras
- 🔸 **Criptografia/descriptografia** de mensagens
- 🔸 **Criptografia/descriptografia** de arquivos
- 🔸 **Salvamento/carregamento** de chaves
- 🔸 **Menu interativo** para facilitar o uso
- 🔸 **Tratamento de erros** completo

### 🎯 Como Usar

#### **Execução com Exemplo Automático:**

```bash
python crypto.py
```

Isso executará uma demonstração completa e perguntará se você quer usar o menu interativo.

#### **Menu Interativo:**

```
=== MENU DE CRIPTOGRAFIA ===
1. Gerar nova chave
2. Carregar chave de arquivo
3. Criptografar mensagem
4. Descriptografar mensagem
5. Criptografar arquivo
6. Descriptografar arquivo
7. Salvar chave atual
8. Mostrar chave atual
0. Sair
```

### 💡 Casos de Uso Diário

#### **1. Criptografar Mensagens Sensíveis:**

```python
from crypto import CryptoManager

crypto = CryptoManager()
crypto.gerar_chave()

# Criptografar
mensagem = "Informação confidencial"
cripto = crypto.criptografar_mensagem(mensagem)

# Descriptografar
original = crypto.descriptografar_mensagem(cripto)
```

#### **2. Proteger Arquivos Importantes:**

```python
# Criptografar arquivo
crypto.criptografar_arquivo("documento_importante.pdf")
# Gera: documento_importante.pdf.criptografado

# Descriptografar quando necessário
crypto.descriptografar_arquivo("documento_importante.pdf.criptografado")
# Gera: documento_importante.pdf.descriptografado
```

#### **3. Gerenciamento de Chaves:**

```python
# Salvar chave para uso futuro
crypto.salvar_chave("minha_chave_secreta.key")

# Carregar chave salva
novo_crypto = CryptoManager()
novo_crypto.carregar_chave("minha_chave_secreta.key")
```

### 🔧 Configuração Inicial

1. **Instalar dependências:**

   ```bash
   pip install cryptography
   ```

2. **Executar primeira vez:**
   ```bash
   python crypto.py
   ```

### 🛡️ Segurança

- **Algoritmo Fernet:** Criptografia simétrica segura (AES 128 em modo CBC)
- **Chaves únicas:** Cada chave é gerada com segurança criptográfica
- **Autenticação:** Verifica integridade dos dados criptografados
- **Tratamento seguro:** Sem exposição desnecessária de chaves

---

## 🚀 Instalação e Configuração

### **Pré-requisitos:**

- Python 3.7+
- pip (gerenciador de pacotes Python)

### **Instalação:**

```bash
# Clonar ou baixar os arquivos
git clone <repositório>
cd <diretório>

# Instalar dependências do crypto.py
pip install cryptography

# Tornar scripts executáveis (Linux)
chmod +x auto.py crypto.py
```

### **Execução:**

```bash
# Auto updater
python3 auto.py

# Crypto manager
python crypto.py
```

---

## 📁 Estrutura do Projeto

```
📦 Projeto/
├── 📄 auto.py              # Atualizador automático
├── 📄 crypto.py            # Gerenciador de criptografia
├── 📄 demo_crypto.py       # Script de demonstração
├── 📄 exemplo.txt          # Arquivo de teste
├── 📄 readme.md            # Este arquivo
└── 🔑 *.key               # Chaves criptográficas (geradas)
```

---

## 💼 Uso Empresarial/Pessoal

### **Auto.py:**

- 🔸 **Administradores de sistema:** Manutenção rápida de servidores
- 🔸 **Desenvolvedores:** Manter ambiente de desenvolvimento atualizado
- 🔸 **Usuários finais:** Atualização simples sem comandos complexos

### **Crypto.py:**

- 🔸 **Proteção de documentos:** Contratos, relatórios sensíveis
- 🔸 **Backup seguro:** Criptografar backups antes do armazenamento
- 🔸 **Comunicação:** Proteger mensagens sensíveis
- 🔸 **Desenvolvimento:** Proteger configurações e credenciais

---

## ⚠️ Notas Importantes

### **Auto.py:**

- Requer privilégios administrativos (sudo)
- Testado em Ubuntu, Fedora, Arch Linux
- Sempre faça backup antes de atualizações críticas

### **Crypto.py:**

- **NUNCA perca suas chaves** - sem elas os dados são irrecuperáveis
- Faça backup das chaves em local seguro
- Use chaves diferentes para dados diferentes
- **Não compartilhe chaves** por canais inseguros

---

## 🤝 Contribuição

Contribuições são bem-vindas! Algumas ideias:

- 🔸 Suporte a mais gerenciadores de pacotes
- 🔸 Interface gráfica para o crypto.py
- 🔸 Criptografia assimétrica (RSA/ECC)
- 🔸 Integração com gerenciadores de senhas

---

## 📄 Licença

Scripts desenvolvidos para uso educacional e produtivo. Use com responsabilidade!

---

## 📞 Suporte

Para dúvidas ou problemas:

1. Verifique se as dependências estão instaladas
2. Confirme as permissões de execução
3. Leia as mensagens de erro cuidadosamente
4. Consulte a documentação das bibliotecas utilizadas

**Lembre-se:** Sempre mantenha backups dos seus dados importantes! 🛡️
