import mysql.connector
from mysql.connector import Error

from aluno import AlunoCRUD


def ler_curso(mensagem):
    """Lê o id do curso (inteiro). Enter em branco = None (sem curso)."""
    texto = input(mensagem).strip()
    if texto == "":
        return None
    return int(texto)


def escolher_criterio():
    print("Buscar por: 1 - ID | 2 - Nome")
    opcao = input("Escolha: ").strip()
    if opcao == "1":
        return "id", int(input("Digite o ID: "))
    if opcao == "2":
        return "nome", input("Digite o nome: ").strip()
    return None, None


def mostrar_menu():
    print("\n===== CRUD ALUNOS =====")
    print("1 - Cadastrar aluno (Create)")
    print("2 - Listar alunos (Read)")
    print("3 - Atualizar curso preferido (Update)")
    print("4 - Excluir aluno (Delete)")
    print("0 - Sair")


def main():
    # A conexão é feita aqui, no arquivo principal
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            database="banco_109",
        )
    except Error as e:
        print(f"Erro ao conectar: {e}")
        return

    crud = AlunoCRUD(conexao)

    try:
        crud.adicionar_coluna_curso_preferido()
    except Error as e:
        print(f"Erro ao preparar a tabela alunos: {e}")
        conexao.close()
        return

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                nome = input("Nome do aluno: ").strip()
                curso = ler_curso("ID do curso preferido (Enter para nenhum): ")
                novo_id = crud.criar(nome, curso)
                print(f"Aluno cadastrado com ID {novo_id}.")

            elif opcao == "2":
                alunos = crud.listar()
                if not alunos:
                    print("Nenhum aluno cadastrado.")
                for id_, nome, curso in alunos:
                    print(f"ID: {id_} | Nome: {nome} | Curso preferido: {curso}")

            elif opcao == "3":
                tipo, valor = escolher_criterio()
                if tipo is None:
                    print("Opção inválida.")
                    continue
                novo_curso = ler_curso("Novo ID do curso preferido: ")
                if tipo == "id":
                    afetados = crud.atualizar_curso_por_id(valor, novo_curso)
                else:
                    afetados = crud.atualizar_curso_por_nome(valor, novo_curso)
                print(f"{afetados} registro(s) atualizado(s).")

            elif opcao == "4":
                tipo, valor = escolher_criterio()
                if tipo is None:
                    print("Opção inválida.")
                    continue
                if tipo == "id":
                    afetados = crud.deletar_por_id(valor)
                else:
                    afetados = crud.deletar_por_nome(valor)
                print(f"{afetados} registro(s) excluído(s).")

            elif opcao == "0":
                print("Encerrando...")
                break

            else:
                print("Opção inválida.")

        except ValueError:
            print("Valor inválido: digite um número onde for pedido um ID.")
        except Error as e:
            # Ex.: tentar usar um curso que não existe (viola a chave estrangeira)
            print(f"Erro no banco de dados: {e}")

    conexao.close()


if __name__ == "__main__":
    main()
