from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from database import (
    init_db, get_cards, get_categories, add_card, update_card, 
    delete_card, get_card_by_id, generate_cards_html,
    User, get_user_by_username
)
import os

# Criar pastas necessárias
if not os.path.exists('static/css'):
    os.makedirs('static/css', exist_ok=True)
if not os.path.exists('static/js'):
    os.makedirs('static/js', exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.get(int(user_id))

# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se já estiver logado, redireciona para a página principal
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user = get_user_by_username(username)
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            # Redireciona para a página que o usuário tentava acessar
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        
        flash('Usuário ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('login'))

# Rotas principais
@app.route('/')
@login_required
def index():
    categories = get_categories()
    return render_template(
        'admin.html',
        cards=get_cards(),
        categories=categories,
        user=current_user
    )

# Rotas de gerenciamento de cards
@app.route('/add_card', methods=['POST'])
@login_required
def create_card():
    try:
        add_card(
            request.form['title'],
            request.form['category'],
            request.form['description'],
            request.form['image_url'],
            request.form['link']
        )
        flash('Card adicionado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar projeto: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit_card/<int:card_id>', methods=['GET', 'POST'])
@login_required
def edit_card(card_id):
    if request.method == 'POST':
        try:
            update_card(
                card_id,
                request.form['title'],
                request.form['category'],
                request.form['description'],
                request.form['image_url'],
                request.form['link']
            )
            flash('Projeto atualizado com sucesso!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Erro ao atualizar projeto: {str(e)}', 'error')
            return redirect(url_for('index'))
    
    card = get_card_by_id(card_id)
    if card:
        return jsonify({
            'id': card[0],
            'title': card[1],
            'category': card[2],
            'description': card[3],
            'image_url': card[4],
            'link': card[5]
        })
    
    flash('Projeto não encontrado.', 'error')
    return redirect(url_for('index'))

@app.route('/delete_card/<int:card_id>', methods=['POST'])
@login_required
def remove_card(card_id):
    try:
        delete_card(card_id)
        return jsonify({'success': True, 'message': 'Projeto removido com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro ao remover Projeto: {str(e)}'})

@app.route('/export')
@login_required
def export():
    try:
        selected_ids = request.args.getlist('ids[]')
        if selected_ids:
            selected_ids = [int(id) for id in selected_ids]
            cards_html = generate_cards_html(selected_ids)
        else:
            cards_html = generate_cards_html()
        return render_template('export.html', cards_html=cards_html)
    except Exception as e:
        flash(f'Erro ao exportar cards: {str(e)}', 'error')
        return redirect(url_for('index'))

# Rota para API de categorias (usado no autocomplete)
@app.route('/api/categories')
@login_required
def api_categories():
    try:
        return jsonify(get_categories())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tratamento de erros
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Inicializar o banco de dados
    init_db()
    
    # Configurações do servidor
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # Iniciar o servidor
    app.run(host=host, port=port, debug=debug)