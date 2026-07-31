/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    MAIN.JS — SCRIPT PRINCIPAL DO FRONTEND
 
    Por enquanto só tem duas coisas:

        1. Marca o link da navbar com uma classe "active" baseado
           na URL atual (pra mostrar onde o usuário está).

        2. Placeholder pra carregar dados dinâmicos depois.
 
    Se quiser testar, abra o console do navegador (F12) e digite:
    highlightCurrentPage()


    ─────────────────────────────────────────────────────────────────────────────────────────────────
    ◦ highlightCurrentPage
 
    Percorre todos os links da navbar. Se o href do link bater
    com a URL atual da página, adiciona a classe "active" nele.
 
    Exemplo: se a URL for /pacientes, o link de Pacientes fica
    destacado com a cor de destaque.
*/


function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.navbar__link');

    links.forEach(function (link) {
        // remove active de todos primeiro
        link.classList.remove('active');

        // compara o caminho do link com a URL atual
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}


/**
 * ────────────────────────────────────────────────────────────────
 * fetchStats
 *
 * PLACEHOLDER — FUTURO
 * Vai buscar os números reais de pacientes, profissionais e
 * atendimentos da API do backend e atualizar os cards.
 *
 * Exemplo de uso futuro:
 *   fetch('/api/stats')
 *     .then(res => res.json())
 *     .then(data => { ...atualiza os números... });
 * ────────────────────────────────────────────────────────────────
 */
function fetchStats() {
    // FUTURO: conectar com o backend
    // const cards = document.querySelectorAll('.stat-card__number');
    // fetch('/api/stats')
    //     .then(res => res.json())
    //     .then(data => {
    //         cards[0].textContent = data.pacientes;
    //         cards[1].textContent = data.profissionais;
    //         cards[2].textContent = data.atendimentos;
    //     });
}


/**
 * ────────────────────────────────────────────────────────────────
 * toggleDetail
 *
 * Expande ou colapsa a linha de detalhes (procedimentos)
 * abaixo de uma linha de atendimento.
 *
 * O botão + vira - quando expandido.
 */
function toggleDetail(btn) {
    var dataRow = btn.closest('.data-row');
    var detailRow = dataRow.nextElementSibling;

    if (detailRow && detailRow.classList.contains('detail-row')) {
        var isOpen = detailRow.classList.toggle('is-open');
        btn.textContent = isOpen ? '−' : '+';
    }
}


// ────────────────────────────────────────────────────────────────
// INIT: roda quando a página carrega


document.addEventListener('DOMContentLoaded', function () {
    highlightCurrentPage();
    // fetchStats();  // descomente quando tiver o backend pronto
});


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
