class AlunoCRUD:
    """Todas as operações do CRUD na tabela alunos.

    A conexão NÃO é criada aqui: ela vem do arquivo principal (main.py).
    """

    # Se os nomes no seu banco forem diferentes, mude só aqui
    TABELA = "alunos"
    COL_ID = "id"            # chave primária da tabela alunos (ex.: idaluno)
    COL_NOME = "nome"
    COL_CURSO = "curso_preferido"
    TABELA_CURSOS = "cursos"
    COL_ID_CURSO = "idcurso"

    def __init__(self, conexao):
        self.conexao = conexao

    # ---------- Preparação da tabela ----------
    def adicionar_coluna_curso_preferido(self):
        """Cria a coluna curso_preferido como chave estrangeira (só se ainda não existir)."""
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            SELECT COUNT(*) FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
              AND TABLE_NAME = %s AND COLUMN_NAME = %s
            """,
            (self.TABELA, self.COL_CURSO),
        )
        (existe,) = cursor.fetchone()

        if existe:
            print("A coluna curso_preferido já existe.")
        else:
            cursor.execute(
                f"""
                ALTER TABLE {self.TABELA}
                ADD COLUMN {self.COL_CURSO} INT NULL,
                ADD CONSTRAINT fk_aluno_curso_preferido
                    FOREIGN KEY ({self.COL_CURSO})
                    REFERENCES {self.TABELA_CURSOS}({self.COL_ID_CURSO})
                """
            )
            self.conexao.commit()
            print("Coluna curso_preferido criada com sucesso.")
        cursor.close()

    # ---------- CREATE ----------
    def criar(self, nome, curso_preferido=None):
        cursor = self.conexao.cursor()
        cursor.execute(
            f"INSERT INTO {self.TABELA} ({self.COL_NOME}, {self.COL_CURSO}) VALUES (%s, %s)",
            (nome, curso_preferido),
        )
        self.conexao.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        return novo_id

    # ---------- READ ----------
    def listar(self):
        cursor = self.conexao.cursor()
        cursor.execute(
            f"SELECT {self.COL_ID}, {self.COL_NOME}, {self.COL_CURSO} FROM {self.TABELA}"
        )
        linhas = cursor.fetchall()
        cursor.close()
        return linhas

    # ---------- UPDATE ----------
    def atualizar_curso_por_id(self, id_aluno, novo_curso):
        return self._atualizar_curso(self.COL_ID, id_aluno, novo_curso)

    def atualizar_curso_por_nome(self, nome, novo_curso):
        return self._atualizar_curso(self.COL_NOME, nome, novo_curso)

    def _atualizar_curso(self, coluna_criterio, valor, novo_curso):
        cursor = self.conexao.cursor()
        cursor.execute(
            f"UPDATE {self.TABELA} SET {self.COL_CURSO} = %s WHERE {coluna_criterio} = %s",
            (novo_curso, valor),
        )
        self.conexao.commit()
        afetados = cursor.rowcount
        cursor.close()
        return afetados

    # ---------- DELETE ----------
    def deletar_por_id(self, id_aluno):
        return self._deletar(self.COL_ID, id_aluno)

    def deletar_por_nome(self, nome):
        return self._deletar(self.COL_NOME, nome)

    def _deletar(self, coluna_criterio, valor):
        cursor = self.conexao.cursor()
        cursor.execute(
            f"DELETE FROM {self.TABELA} WHERE {coluna_criterio} = %s",
            (valor,),
        )
        self.conexao.commit()
        afetados = cursor.rowcount
        cursor.close()
        return afetados
