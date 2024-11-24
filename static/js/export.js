// Função para copiar o código para a área de transferência
function copyToClipboard() {
    const code = document.getElementById('htmlCode');
    const successMessage = document.getElementById('copySuccess');
    
    navigator.clipboard.writeText(code.textContent)
        .then(() => {
            successMessage.style.display = 'block';
            successMessage.style.opacity = '1';
            
            // Reset do elemento após a animação
            setTimeout(() => {
                successMessage.style.opacity = '0'; // Mudança para suavizar o desaparecimento
                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 500); // Espera o fade-out terminar
            }, 3000);
        })
        .catch(err => {
            alert('Erro ao copiar. Por favor, copie manualmente.');
            console.error('Erro:', err);
        });
}

// Função para highlight de sintaxe HTML
function highlightHTML() {
    const code = document.getElementById('htmlCode');
    let html = code.innerHTML;
    
    // Substituir tags e atributos por versões coloridas
    html = html.replace(/(<\/?[\w-]+)(\s*[^>]*)(\/?>)/gi, (match, tag, attrs, end) => {
        // Destaca a tag
        const highlightedTag = `<span class="html-tag">${tag}</span>`;
        
        // Destaca os atributos
        const highlightedAttrs = attrs.replace(/([\w-]+)=/gi, (match, p1) => {
            return `<span class="html-attr">${p1}</span>=`;
        }).replace(/"([^"]*)"/g, '<span class="html-string">"$1"</span>'); // Destaca o valor dos atributos
        
        return highlightedTag + highlightedAttrs + end;
    });
    
    // Destacar comentários
    html = html.replace(/<!--[^>]*-->/g, (comment) => {
        return `<span class="html-comment">${comment}</span>`;
    });
    
    // Atualizar o conteúdo do código
    code.innerHTML = html;
}

// Executar highlight quando a página carregar
document.addEventListener('DOMContentLoaded', highlightHTML);
