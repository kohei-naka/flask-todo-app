import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import TodoForm
from datetime import datetime
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

app = Flask(__name__)

# .env から読み込んだ値を設定
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# DBオブジェクト作成
db = SQLAlchemy(app)

# モデル定義（DBに対応するクラス）
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

# ルーティング
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TodoForm()
    
    # POST処理（タスク追加）
    if form.validate_on_submit():
        new_todo = Todo(
            title=form.title.data,
            due_date=form.due_date.data,
            priority=form.priority.data
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))

    # GET処理（表示＆ソート）
    sort = request.args.get('sort', 'default')
    if sort == 'due_date_asc':
        todos = Todo.query.order_by(Todo.due_date.asc()).all()
    elif sort == 'due_date_desc':
        todos = Todo.query.order_by(Todo.due_date.desc()).all()
    else:
        todos = Todo.query.all()

    return render_template('index.html', form=form, todos=todos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(
            title=form.title.data,
            due_date=form.due_date.data,
            priority=form.priority.data
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    form = TodoForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            todo.title = form.title.data
            todo.due_date = form.due_date.data
            todo.priority = int(form.priority.data)
            db.session.commit()
            return redirect('/')
    else:
        form.title.data = todo.title

        # ここで文字列を date に変換
        if isinstance(todo.due_date, str):
            todo.due_date = datetime.strptime(todo.due_date, "%Y-%m-%d").date()
        form.due_date.data = todo.due_date
        form.priority.data = str(todo.priority)  # HTML 側が文字列で扱うなら

    return render_template('edit.html', form=form, todo=todo)

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

# 初回のみ：DB作成コマンド（必要に応じて一時的に使う）
# with app.app_context():
    # db.create_all()
