# importar biblioteca.
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime

# importar session e sessionmaker.
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# configurar a conexão de banco.
engine = create_engine('sqlite:///base_tarefas.sqlite3')

# gerenciar sessao com banco de dados.
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Tarefa(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False, index=True)
    descricao = Column(String)
    status = Column(Integer, nullable=False, index=True)

    def __repr__(self):
        return '<tarefa: {} {}>'.format(self.id, self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_tarefa(self):
        dados_tarefa = {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'status': self.status
        }
        return dados_tarefa


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
