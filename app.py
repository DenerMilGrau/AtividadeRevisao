from flask import Flask, render_template, redirect, url_for, request, flash
from models import Tarefa, db_session
import sqlalchemy
from sqlalchemy import select

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/tarefas', methods=['GET', 'POST'])
def tarefas_func():
    lista_tarefas = select(Tarefa)
    lista_tarefas = db_session.execute(lista_tarefas).scalars()
    resultado = []
    for tarefa in lista_tarefas:
        resultado.append(tarefa.serialize_tarefa())
    return render_template('tarefas.html', tarefas=resultado)


@app.route('/tarefas/cadastro', methods=['GET', 'POST'])
def cadastro_func():
    print('')
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        if not nome:
            flash('O campo nome é obrigatorio', 'error')
        else:
            form_add_tarefa = Tarefa(nome=nome,
                                     descricao=descricao,
                                     status=0)
            form_add_tarefa.save()
            db_session.close()
            flash('Tarefa cadastrada com sucesso!', 'success')
            return redirect(url_for('tarefas_func'))
    return render_template('cadastro.html')

# rota inacabada
@app.route('/tarefas/editar-<id>', methods=['GET', 'POST'])
def editar_func(id):
    id=id
    lista_tarefas = select(Tarefa).where(Tarefa.id==id)
    resultado = db_session.execute(lista_tarefas).scalar()

    # resultado = []
    # for tarefa_ in lista_tarefas:
    #     resultado.append(tarefa_.serialize_tarefa())
    if request.method == 'POST':
        nome_var = request.form.get('nome')
        descricao_var = request.form['descricao']
        status = request.form['status_tarefa']
        if not nome_var:
            flash('Preencha o campo nome', 'error')
        else:
            try:
                status = int(status)
                print(type(status))

            except ValueError:
                flash('Houve um erro com os valores do status! Tente novamente', 'error')
            if status not in [0, 1, 2]:
                flash('Preencha o campo status da tarefa', 'error')
            else:
                resultado.nome = nome_var
                resultado.descricao = descricao_var
                resultado.status = status
                print(resultado)

                resultado.save()
                flash('Tarefa editada com sucesso!', 'success')
                return redirect(url_for('tarefas_func'))
    print(resultado)
    return render_template('editar.html', tarefa=resultado, id=id)



@app.route('/tarefas/deletar/<id>', methods=['GET', 'POST'])
def deletar_func(id):
    id=id
    print(id)
    lista_tarefas = select(Tarefa).where(Tarefa.id==id)
    resultado = db_session.execute(lista_tarefas).scalar()
    resultado.delete()
    flash('Tarefa deletada com sucesso!', 'success')
    return redirect(url_for('tarefas_func'))


@app.route('/tarefas/detalhes-<id>', methods=['GET', 'POST'])
def detalhes_func(id):
    id=id
    lista_tarefas = select(Tarefa).where(Tarefa.id==id)
    resultado = db_session.execute(lista_tarefas).scalar()

    return render_template('detalhes.html', tarefa=resultado, id=id)

if __name__ == '__main__':
    app.run(debug=True)
