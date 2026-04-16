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
        sql = "INSERT INTO db_loja (nome_produto, preco) VALUES (%s, %s)"
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
            sql = "SELECT * FROM db_loja WHERE id_produto = %s"
            cursor.execute(sql, (id, )) 
            resultados = cursor.fetchall()
            
        elif opcao == 2:
            nome = input("Digite o nome do produto: ")
            sql = "SELECT * FROM db_loja WHERE nome_produto = %s"
            cursor.execute(sql, (nome, ))
            resultados = cursor.fetchall()

        elif opcao == 3:
            sql = "SELECT * FROM db_loja"
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
        sql = ("UPDATE db_loja set nome_produto = %s, preco = %s WHERE id_produto = %s")
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
            sql = "DELETE FROM db_loja WHERE id_produto = %s"
            cursor.execute(sql, (id, ))
            db.commit()
            print("Registro deletado com sucesso!")
            return
            
        elif opcao == 2:
            nome = input("Digite o nome do produto: ")
            sql = "DELETE FROM db_loja WHERE nome_produto = %s"
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

while True:
    print("\n--- SISTEMA DE GESTÃO ---")
    print("1. Criar | 2. Consultar | 3. Atualizar | 4. Deletar | 0. Sair")
    print("-" * 65)
    opcao = input("Escolha uma opção: ")

    if opcao == '1': criar_dado()
    elif opcao == '2': consultar_dados()
    elif opcao == '3': atualizar_dado()
    elif opcao == '4': deletar_dado()
    elif opcao == '0': break
    else: print("Opção inválida!")