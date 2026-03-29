const form = document.getElementById("search-form");
const input = document.getElementById("search-input");
const resultsMessage = document.getElementById("results-message");
const bookGrid = document.getElementById("book-grid");
const template = document.getElementById("book-card-template");

const modal = document.getElementById("store-modal");
const modalBookTitle = document.getElementById("modal-book-title");
const modalBookMeta = document.getElementById("modal-book-meta");
const reservationPanel = document.getElementById("reservation-panel");
const successPanel = document.getElementById("success-panel");
const unitList = document.getElementById("unit-list");
const reservationUser = document.getElementById("reservation-user");
const reservationDate = document.getElementById("reservation-date");
const successSummary = document.getElementById("success-summary");
const successQr = document.getElementById("success-qr");
const newSearchButton = document.getElementById("new-search-button");
const closeModalElements = document.querySelectorAll("[data-close-modal]");

let selectedBook = null;
let selectedUnits = [];

function setMessage(text) {
    resultsMessage.textContent = text;
}

function openModal() {
    modal.classList.remove("is-hidden");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-open");
}

function closeModal() {
    modal.classList.add("is-hidden");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-open");
}

function formatStockLabel(quantity) {
    if (quantity === 1) {
        return "1 exemplar disponível";
    }

    return `${quantity} exemplares disponíveis`;
}

function renderBooks(books) {
    bookGrid.innerHTML = "";

    books.forEach((book) => {
        const card = template.content.cloneNode(true);

        card.querySelector(".book-card__title").textContent = book.titulo;
        card.querySelector(".book-card__author").textContent = `Autor: ${book.autor}`;
        card.querySelector(".book-card__publisher").textContent = `Editora: ${book.editora}`;
        card.querySelector(".book-card__stock").textContent = `${book.total_estoque} ${book.total_estoque === 1 ? "exemplar" : "exemplares"} em ${book.unidades_disponiveis.length} ${book.unidades_disponiveis.length === 1 ? "unidade" : "unidades"}`;
        card.querySelector(".book-card__badge").textContent = book.badge;

        const openUnitsButton = card.querySelector(".button--secondary");
        const reserveButton = card.querySelector(".button--primary");

        openUnitsButton.addEventListener("click", () => openUnitsModal(book));
        reserveButton.addEventListener("click", () => openUnitsModal(book));

        bookGrid.appendChild(card);
    });
}

async function searchBooks(query) {
    const response = await fetch(`/api/livros?termo=${encodeURIComponent(query)}`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Não foi possível realizar a busca.");
    }

    return data;
}

async function loadUnits(book) {
    const response = await fetch(`/api/livros/${book.id}/unidades`);
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Não foi possível carregar as unidades.");
    }

    return data.unidades;
}

function clearSuccessState() {
    reservationPanel.classList.remove("is-hidden");
    successPanel.classList.add("is-hidden");
}

function openUnitsModal(book) {
    selectedBook = book;
    selectedUnits = [];

    modalBookTitle.textContent = book.titulo;
    modalBookMeta.textContent = `${book.autor} • ${book.editora}`;

    reservationUser.value = "";
    reservationDate.value = "";
    clearSuccessState();
    unitList.innerHTML = `<div class="results-message">Carregando unidades disponíveis...</div>`;

    openModal();

    loadUnits(book)
        .then((units) => {
            selectedUnits = units;
            renderUnits(units);
        })
        .catch((error) => {
            unitList.innerHTML = `<div class="results-message">${error.message}</div>`;
        });
}

function renderUnits(units) {
    if (!units.length) {
        unitList.innerHTML = `
            <div class="results-message">
                Nenhuma unidade com estoque disponível para este livro.
            </div>
        `;
        return;
    }

    unitList.innerHTML = "";

    units.forEach((unit) => {
        const card = document.createElement("article");
        card.className = "unit-card";

        const info = document.createElement("div");

        const title = document.createElement("h3");
        title.className = "unit-card__title";
        title.textContent = unit.nome;

        const meta = document.createElement("p");
        meta.className = "unit-card__meta";
        meta.textContent = formatStockLabel(unit.quantidade);

        info.appendChild(title);
        info.appendChild(meta);

        const reserveButton = document.createElement("button");
        reserveButton.type = "button";
        reserveButton.className = "button button--primary";
        reserveButton.textContent = "Reservar nesta unidade";

        reserveButton.addEventListener("click", () => reserveBook(unit.nome, reserveButton));

        card.appendChild(info);
        card.appendChild(reserveButton);

        unitList.appendChild(card);
    });
}

async function reserveBook(unitName, buttonElement) {
    if (!selectedBook) {
        return;
    }

    const originalLabel = buttonElement.textContent;
    buttonElement.disabled = true;
    buttonElement.textContent = "Reservando...";

    try {
        const payload = {
            livro_id: selectedBook.id,
            unidade: unitName,
            usuario: reservationUser.value.trim() || null,
            data: reservationDate.value || null,
        };

        const response = await fetch("/api/reservas", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Não foi possível concluir a reserva.");
        }

        reservationPanel.classList.add("is-hidden");
        successPanel.classList.remove("is-hidden");

        successSummary.textContent = `${selectedBook.titulo} reservado em ${unitName}.`;
        successQr.textContent = data.reserva.qr_code;
    } catch (error) {
        alert(error.message);
    } finally {
        buttonElement.disabled = false;
        buttonElement.textContent = originalLabel;
    }
}

closeModalElements.forEach((element) => {
    element.addEventListener("click", closeModal);
});

newSearchButton.addEventListener("click", () => {
    closeModal();
    input.focus();
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !modal.classList.contains("is-hidden")) {
        closeModal();
    }
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = input.value.trim();

    if (!query) {
        setMessage("Digite um termo para buscar.");
        bookGrid.innerHTML = "";
        return;
    }

    setMessage("Buscando livros...");
    bookGrid.innerHTML = "";

    try {
        const data = await searchBooks(query);

        if (!data.livros.length) {
            setMessage(`Nenhum livro encontrado para "${query}".`);
            return;
        }

        setMessage(`Foram encontrados ${data.total} livro(s) para "${query}".`);
        renderBooks(data.livros);
    } catch (error) {
        setMessage(error.message);
    }
});

setMessage("Faça uma busca para começar.");
input.focus();