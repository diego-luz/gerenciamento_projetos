// Funções de prévia de imagem
function previewImage(url) {
    const preview = document.getElementById('imagePreview');
    preview.src = url;
    preview.style.display = url ? 'block' : 'none';
}

function previewEditImage(url) {
    const preview = document.getElementById('editImagePreview');
    preview.src = url;
    preview.style.display = url ? 'block' : 'none';
}

// Funções de seleção e exportação
function toggleSelectAll() {
    const checkboxes = document.querySelectorAll('.card-checkbox');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    checkboxes.forEach(cb => cb.checked = !allChecked);
}

function getSelectedIds() {
    const checkboxes = document.querySelectorAll('.card-checkbox:checked');
    return Array.from(checkboxes).map(cb => cb.value);
}

function exportSelected() {
    const selectedIds = getSelectedIds();
    if (selectedIds.length === 0) {
        alert('Por favor, selecione pelo menos um card para exportar.');
        return;
    }
    const queryString = selectedIds.map(id => `ids[]=${id}`).join('&');
    window.location.href = `/export?${queryString}`;
}

function exportAll() {
    window.location.href = '/export';
}

// Funções do modal de edição
function openEditModal(cardId) {
    fetch(`/edit_card/${cardId}`)
        .then(response => response.json())
        .then(card => {
            document.getElementById('editCardId').value = card.id;
            document.getElementById('editTitle').value = card.title;
            document.getElementById('editCategory').value = card.category;
            document.getElementById('editDescription').value = card.description;
            document.getElementById('editImageUrl').value = card.image_url;
            document.getElementById('editLink').value = card.link;
            previewEditImage(card.image_url);
            
            document.getElementById('editModal').style.display = 'block';
        });
}

function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

function submitEditForm(event) {
    event.preventDefault();
    const form = event.target;
    const cardId = document.getElementById('editCardId').value;
    
    fetch(`/edit_card/${cardId}`, {
        method: 'POST',
        body: new FormData(form)
    }).then(() => {
        window.location.reload();
    });
}

// Função para deletar card
function deleteCard(cardId) {
    if (confirm('Tem certeza que deseja excluir este card?')) {
        fetch(`/delete_card/${cardId}`, {
            method: 'POST'
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                window.location.reload();
            }
        });
    }
}

// Fechar modal quando clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeEditModal();
    }
}
// Função para submeter o formulário de edição
function submitEditForm() {
    const id = document.getElementById('editCardId').value;
    const form = document.getElementById('editForm');
    const formData = new FormData(form);

    fetch(`/edit_card/${id}`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            window.location.reload();
        } else {
            alert('Erro ao salvar as alterações');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar as alterações');
    });
}

// Função para deletar card
function deleteCard(cardId) {
    if (confirm('Tem certeza que deseja excluir este card?')) {
        fetch(`/delete_card/${cardId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const cardElement = document.querySelector(`.card[data-id="${cardId}"]`);
                if (cardElement) {
                    cardElement.remove();
                }
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao excluir o card');
        });
    }
}

// Função para fechar o modal
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Fechar modal quando clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeEditModal();
    }
}