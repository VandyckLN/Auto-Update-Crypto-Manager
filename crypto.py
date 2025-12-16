from cryptography.fernet import Fernet
import os


class CryptoManager:
    """Classe para gerenciar criptografia e descriptografia usando Fernet."""
    
    def __init__(self):
        self.key = None
        self.cipher_suite = None
    
    def gerar_chave(self):
        """Gera uma nova chave de criptografia."""
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        return self.key
    
    def salvar_chave(self, nome_arquivo="chave.key"):
        """Salva a chave em um arquivo."""
        if self.key is None:
            raise ValueError("Nenhuma chave foi gerada. "
                           "Use gerar_chave() primeiro.")
        
        with open(nome_arquivo, "wb") as arquivo_chave:
            arquivo_chave.write(self.key)
        print(f"Chave salva em '{nome_arquivo}'")
    
    def carregar_chave(self, nome_arquivo="chave.key"):
        """Carrega a chave de um arquivo."""
        if not os.path.exists(nome_arquivo):
            raise FileNotFoundError(f"Arquivo '{nome_arquivo}' "
                                  "não encontrado.")
        
        with open(nome_arquivo, "rb") as arquivo_chave:
            self.key = arquivo_chave.read()
            self.cipher_suite = Fernet(self.key)
        print(f"Chave carregada de '{nome_arquivo}'")
    
    def definir_chave(self, chave):
        """Define uma chave específica."""
        if isinstance(chave, str):
            chave = chave.encode()
        self.key = chave
        self.cipher_suite = Fernet(self.key)
    
    def criptografar_mensagem(self, mensagem):
        """Criptografa uma mensagem."""
        if self.cipher_suite is None:
            raise ValueError("Nenhuma chave definida. "
                           "Use gerar_chave() ou carregar_chave() primeiro.")
        
        if isinstance(mensagem, str):
            mensagem = mensagem.encode('utf-8')
        
        return self.cipher_suite.encrypt(mensagem)
    
    def descriptografar_mensagem(self, mensagem_criptografada):
        """Descriptografa uma mensagem."""
        if self.cipher_suite is None:
            raise ValueError("Nenhuma chave definida. "
                           "Use gerar_chave() ou carregar_chave() primeiro.")
        
        try:
            mensagem_descriptografada = self.cipher_suite.decrypt(
                mensagem_criptografada)
            return mensagem_descriptografada.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar: {str(e)}")
    
    def criptografar_arquivo(self, caminho_arquivo):
        """Criptografa o conteúdo de um arquivo."""
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' "
                                  "não encontrado.")
        
        with open(caminho_arquivo, "rb") as arquivo:
            conteudo = arquivo.read()
        
        conteudo_criptografado = self.criptografar_mensagem(conteudo)
        
        nome_arquivo_criptografado = f"{caminho_arquivo}.criptografado"
        with open(nome_arquivo_criptografado, "wb") as arquivo_criptografado:
            arquivo_criptografado.write(conteudo_criptografado)
        
        print(f"Arquivo criptografado salvo como "
              f"'{nome_arquivo_criptografado}'")
        return nome_arquivo_criptografado
    
    def descriptografar_arquivo(self, caminho_arquivo_criptografado):
        """Descriptografa o conteúdo de um arquivo criptografado."""
        if not os.path.exists(caminho_arquivo_criptografado):
            raise FileNotFoundError(
                f"Arquivo '{caminho_arquivo_criptografado}' "
                "não encontrado.")
        
        with open(caminho_arquivo_criptografado, "rb") as arquivo:
            conteudo_criptografado = arquivo.read()
        
        try:
            conteudo_descriptografado = self.cipher_suite.decrypt(
                conteudo_criptografado)
        except Exception as e:
            raise ValueError(f"Erro ao descriptografar arquivo: {str(e)}")
        
        nome_arquivo_descriptografado = caminho_arquivo_criptografado.replace(
            ".criptografado", ".descriptografado")
        with open(nome_arquivo_descriptografado, "wb") as arquivo_desc:
            arquivo_desc.write(conteudo_descriptografado)
        
        print(f"Arquivo descriptografado salvo como "
              f"'{nome_arquivo_descriptografado}'")
        return nome_arquivo_descriptografado


def exemplo_uso():
    """Exemplo de uso da classe CryptoManager."""
    print("=== EXEMPLO DE USO - CRIPTOGRAFIA COM FERNET ===\n")
    
    # Criar instância do gerenciador de criptografia
    crypto = CryptoManager()
    
    # Gerar nova chave
    print("1. Gerando nova chave...")
    chave = crypto.gerar_chave()
    print(f"Chave gerada: {chave.decode()}\n")
    
    # Mensagem para criptografar
    mensagem_original = "Esta é uma mensagem secreta que será criptografada!"
    print(f"Mensagem original: {mensagem_original}")
    
    # Criptografar mensagem
    print("\n2. Criptografando mensagem...")
    mensagem_criptografada = crypto.criptografar_mensagem(mensagem_original)
    print(f"Mensagem criptografada: {mensagem_criptografada}")
    
    # Descriptografar mensagem
    print("\n3. Descriptografando mensagem...")
    mensagem_descriptografada = crypto.descriptografar_mensagem(
        mensagem_criptografada)
    print(f"Mensagem descriptografada: {mensagem_descriptografada}")
    
    # Verificar se a descriptografia foi bem-sucedida
    verificacao = mensagem_original == mensagem_descriptografada
    print(f"\nVerificação: {verificacao}")
    
    # Salvar chave em arquivo
    print("\n4. Salvando chave em arquivo...")
    crypto.salvar_chave("minha_chave.key")
    
    # Demonstrar carregamento de chave
    print("\n5. Testando carregamento de chave...")
    novo_crypto = CryptoManager()
    novo_crypto.carregar_chave("minha_chave.key")
    
    # Testar com a chave carregada
    teste_mensagem = "Testando com chave carregada"
    teste_criptografado = novo_crypto.criptografar_mensagem(teste_mensagem)
    teste_descriptografado = novo_crypto.descriptografar_mensagem(
        teste_criptografado)
    print(f"Teste com chave carregada: {teste_descriptografado}")
    
    print("\n=== FIM DO EXEMPLO ===")


def menu_interativo():
    """Menu interativo para usar as funcionalidades de criptografia."""
    crypto = CryptoManager()
    
    while True:
        print("\n=== MENU DE CRIPTOGRAFIA ===")
        print("1. Gerar nova chave")
        print("2. Carregar chave de arquivo")
        print("3. Criptografar mensagem")
        print("4. Descriptografar mensagem")
        print("5. Criptografar arquivo")
        print("6. Descriptografar arquivo")
        print("7. Salvar chave atual")
        print("8. Mostrar chave atual")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        try:
            if opcao == "1":
                chave = crypto.gerar_chave()
                print(f"Nova chave gerada: {chave.decode()}")
                
            elif opcao == "2":
                nome_arquivo = input("Nome do arquivo da chave "
                                   "(padrão: chave.key): ").strip()
                if not nome_arquivo:
                    nome_arquivo = "chave.key"
                crypto.carregar_chave(nome_arquivo)
                
            elif opcao == "3":
                mensagem = input("Digite a mensagem para criptografar: ")
                resultado = crypto.criptografar_mensagem(mensagem)
                print(f"Mensagem criptografada: {resultado}")
                
            elif opcao == "4":
                entrada = input("Digite a mensagem criptografada: ")
                # Converter string para bytes se necessário
                if isinstance(entrada, str) and entrada.startswith("b'"):
                    entrada = eval(entrada)
                resultado = crypto.descriptografar_mensagem(entrada)
                print(f"Mensagem descriptografada: {resultado}")
                
            elif opcao == "5":
                arquivo = input("Caminho do arquivo para criptografar: ")
                crypto.criptografar_arquivo(arquivo)
                
            elif opcao == "6":
                arquivo = input("Caminho do arquivo criptografado: ")
                crypto.descriptografar_arquivo(arquivo)
                
            elif opcao == "7":
                nome_arquivo = input("Nome do arquivo para salvar a chave "
                                   "(padrão: chave.key): ").strip()
                if not nome_arquivo:
                    nome_arquivo = "chave.key"
                crypto.salvar_chave(nome_arquivo)
                
            elif opcao == "8":
                if crypto.key:
                    print(f"Chave atual: {crypto.key.decode()}")
                else:
                    print("Nenhuma chave definida.")
                    
            elif opcao == "0":
                print("Encerrando programa...")
                break
                
            else:
                print("Opção inválida!")
                
        except Exception as e:
            print(f"Erro: {str(e)}")


if __name__ == "__main__":
    # Executar exemplo de uso
    exemplo_uso()
    
    # Perguntar se o usuário quer usar o menu interativo
    resposta = input("\nDeseja usar o menu interativo? (s/n): ").lower()
    if resposta == 's' or resposta == 'sim':
        menu_interativo()