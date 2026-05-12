const FIELD_TYPES = ["FullName", "Number", "BirthDate", "Address", "Phone", "Email", "Job", "Company"];
let currentSchema = [];
let currentFileId = null;
let currentHeaders = null;

function loadSchema() {
    const saved = localStorage.getItem("dataSynth_schema");
    if (saved) {
        currentSchema = JSON.parse(saved);
    } else {
        currentSchema = [
            { name: "full_name", type: "FullName" },
            { name: "email", type: "Email" }
        ];
    }
    renderFields();
}

function saveSchema() {
    localStorage.setItem("dataSynth_schema", JSON.stringify(currentSchema));
}

function renderFields() {
    const container = document.getElementById("fieldsContainer");
    container.innerHTML = "";
    currentSchema.forEach((field, idx) => {
        const row = document.createElement("div");
        row.className = "field-row";
        row.innerHTML = `
            <input type="text" value="${escapeHtml(field.name)}" data-index="${idx}" data-field="name" placeholder="Имя поля">
            <select data-index="${idx}" data-field="type">
                ${FIELD_TYPES.map(t => `<option value="${t}" ${field.type === t ? 'selected' : ''}>${t}</option>`).join('')}
            </select>
            <button class="btn-remove" data-index="${idx}">✖</button>
        `;
        container.appendChild(row);
    });
    attachEvents();
}

function attachEvents() {
    document.querySelectorAll('.field-row input').forEach(inp => {
        inp.onchange = (e) => {
            const idx = e.target.dataset.index;
            currentSchema[idx].name = e.target.value;
            saveSchema();
        };
    });
    document.querySelectorAll('.field-row select').forEach(sel => {
        sel.onchange = (e) => {
            const idx = e.target.dataset.index;
            currentSchema[idx].type = e.target.value;
            saveSchema();
        };
    });
    document.querySelectorAll('.btn-remove').forEach(btn => {
        btn.onclick = (e) => {
            const idx = btn.dataset.index;
            currentSchema.splice(idx, 1);
            saveSchema();
            renderFields();
        };
    });
}

function addField() {
    currentSchema.push({ name: `field_${currentSchema.length + 1}`, type: "FullName" });
    saveSchema();
    renderFields();
}

async function generate() {
    const rows = parseInt(document.getElementById("rowsCount").value);
    const resultCard = document.getElementById("resultCard");
    const resultArea = document.getElementById("resultArea");
    const downloadCsvBtn = document.getElementById("downloadCsvBtn");
    const downloadJsonBtn = document.getElementById("downloadJsonBtn");

    resultCard.style.display = "block";
    resultArea.innerHTML = `<div class="status">⏳ Генерация...</div>`;
    downloadCsvBtn.style.display = "none";
    downloadJsonBtn.style.display = "none";
    currentFileId = null;

    try {
        const res = await fetch("/generate/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ rows: rows, fields: currentSchema })
        });
        if (!res.ok) throw new Error("Ошибка сервера");

        const data = await res.json();
        if (!data.file_id) throw new Error("Сервер не вернул file_id");

        currentFileId = data.file_id;
        currentHeaders = data.headers;

        let html = `<div style="overflow-x:auto;"><table><thead><tr>`;
        data.headers.forEach(h => html += `<th>${escapeHtml(h)}</th>`);
        html += `</thead><tbody>`;
        if (data.data && data.data.length) {
            data.data.forEach(row => {
                html += `<tr>`;
                row.forEach(cell => html += `<td>${escapeHtml(String(cell))}</td>`);
                html += `</tr>`;
            });
        } else {
            html += `<tr><td colspan="${data.headers.length}">Нет превью</td></tr>`;
        }
        html += `</tbody></table></div>`;
        resultArea.innerHTML = html;

        downloadCsvBtn.style.display = "inline-block";
        downloadJsonBtn.style.display = "inline-block";
    } catch (err) {
        resultArea.innerHTML = `<div class="status error">❌ ${err.message}</div>`;
        downloadCsvBtn.style.display = "none";
        downloadJsonBtn.style.display = "none";
    }
}

function escapeHtml(str) {
    return str.replace(/[&<>]/g, function(m) {
        if (m === '&') return '&amp;';
        if (m === '<') return '&lt;';
        if (m === '>') return '&gt;';
        return m;
    });
}

document.getElementById("addFieldBtn").onclick = addField;
document.getElementById("generateBtn").onclick = generate;

document.getElementById("downloadCsvBtn").onclick = () => {
    if (currentFileId) {
        window.location.href = `/generate/download/${currentFileId}?format=csv`;
    } else {
        alert("Нет сгенерированных данных");
    }
};

document.getElementById("downloadJsonBtn").onclick = () => {
    if (currentFileId) {
        window.location.href = `/generate/download/${currentFileId}?format=json`;
    } else {
        alert("Нет сгенерированных данных");
    }
};

loadSchema();
