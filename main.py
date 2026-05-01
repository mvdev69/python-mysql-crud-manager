import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

def conectar():
    return mysql.connector.connect (
        host = os.getenv("HOST"),
        user = os.getenv("USER"),
        password = os.getenv("PASSWORD"),
        database = os.getenv("DATABASE")
    )

def fazer_login():
    print("\n--- ACESSO AO SISTEMA ---")
    usuario_input = input("Usuário: ")
    senha_input = input("Senha: ")

    try:
        db = conectar()
        cursor = db.cursor()
        
        # Busca o usuário e traz todos os dados dele
        sql = "SELECT * FROM usuario WHERE usuario = %s AND senha = %s"
        cursor.execute(sql, (usuario_input, senha_input))
        resultado = cursor.fetchone()

        if resultado:
            # resultado[4] é onde está o 'nivel_acesso' (ajuste conforme a ordem das colunas)
            nivel = resultado[4] 
            return nivel  # Retorna 'admin' ou 'funcionario' em vez de True
        else:
            return None # Retorna nada se falhar

    except mysql.connector.Error as err:
        print(f"Erro ao conectar para login: {err}")
        return None
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

def criar_dado():
    try:
        db = conectar()
        cursor = db.cursor()

        nome = input("Digite o nome: ")
        try:
            preco = float(input("Digite o preço (ex: 10.99): "))
        except ValueError:
            print("ERRO. Digite um valor decimal.")
            return
        sql = "INSERT INTO produto (nome_produto, preco) VALUES (%s, %s)"
        cursor.execute(sql, (nome, preco))

        db.commit()
        print(f"{cursor.rowcount} registro inserido com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

def consultar_dados():
    try:
        db = conectar()
        cursor = db.cursor()

        try:
            opcao = int(input("1.Consultar por id | 2.Consultar por nome | 3.Consultar todos\nEscolha uma opção: "))
        except ValueError:
            print("Opção inválida.")
            return
        if opcao == 1:
            id = int(input("Digite o ID do produto: "))
            sql = "SELECT * FROM produto WHERE id_produto = %s"
            cursor.execute(sql, (id, )) 
            resultados = cursor.fetchall()
            
        elif opcao == 2:
            nome = input("Digite o nome do produto: ")
            sql = "SELECT * FROM produto WHERE nome_produto = %s"
            cursor.execute(sql, (nome, ))
            resultados = cursor.fetchall()

        elif opcao == 3:
            sql = "SELECT * FROM produto"
            cursor.execute(sql)
            resultados = cursor.fetchall()

        else:
            print("Opção inválida.")
            return
            
        if not resultados:
            print("Nenhum registro encontrado.")
        else:
            for (id_prod, nome_prod, preco) in resultados:
                print("-" * 80)
                print(f"ID: {id_prod}| NOME: {nome_prod}| PRECO {preco:.2f}")
        
    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

def atualizar_dado():
    try:
        db = conectar()
        cursor = db.cursor()

        id = input("Digite o id do produto a ser atualizado: ")
        nome = input("Digite o nome do novo produto: ")
        preco = input("Digite o novo valor: ")
        sql = ("UPDATE db_loj set nome_produto = %s, preco = %s WHERE id_produto = %s")
        cursor.execute(sql, (nome, preco, id))
        db.commit()
        print(f"Dado {nome} com o preço de R${preco} atualizados com sucesso!")

    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

def deletar_dado():
    try:
        db = conectar()
        cursor = db.cursor()
        try:
            opcao = int(input("1.Deletar por id | 2.Deletar por nome\nEscolha uma opção:"))
        except ValueError:
            print("Erro. Opção inválida.")
            return
        
        if opcao == 1:
            id = input("Digite o id do produto: ")
            sql = "DELETE FROM produto WHERE id_produto = %s"
            cursor.execute(sql, (id, ))
            db.commit()
            print("Registro deletado com sucesso!")
            return
            
        elif opcao == 2:
            nome = input("Digite o nome do produto: ")
            sql = "DELETE FROM produto WHERE nome_produto = %s"
            cursor.execute(sql, (nome, ))
            db.commit()
            print("Registro deletado com sucesso!")
            return
        
        else:
            print("Opção inválida. Escolha entre o id ou o nome do produto.")
            return

    except mysql.connector.Error as err:
        print(f"Erro no banco de dados: {err}")
    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()

# --- FLUXO DE EXECUÇÃO ---

# O sistema só inicia se o login for bem-sucedido
nivel_usuario = fazer_login() 

if nivel_usuario:
    if nivel_usuario == 'admin':
        print("Acesso de administrador concedido. Você tem permissão total.")
        while True:
            print("\n--- SISTEMA DE GESTÃO (ADMIN) ---")
            print("1. Criar | 2. Consultar | 3. Atualizar | 4. Deletar | 0. Sair")
            print("-" * 65)
            opcao = input("Escolha uma opção: ")

            if opcao == '1': criar_dado()
            elif opcao == '2': consultar_dados()
            elif opcao == '3': atualizar_dado()
            elif opcao == '4': deletar_dado()
            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!") 

    elif nivel_usuario == 'funcionario':
        print("Acesso de funcionário concedido. Você tem permissão limitada.")
        while True:
            print("\n--- SISTEMA DE GESTÃO (CONSULTA) ---")
            print("1. Consultar | 0. Sair")
            print("-" * 65)
            opcao = input("Escolha uma opção: ")

            if opcao == '1': consultar_dados()
            elif opcao == '0':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
else:
    print("\nFalha no login: Usuário ou senha incorretos.")