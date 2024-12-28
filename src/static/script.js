// ===========================
// FUNCIONES PRINCIPALES
// ===========================

// Mostrar una sección principal y ocultar subsecciones
function showSection(sectionId) {
    const sections = document.querySelectorAll('.section-content');
    sections.forEach(section => section.classList.add('hidden'));

    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.remove('hidden');
    }

    updateMenuState(sectionId);
    hideSubsections(selectedSection);
}

// Mostrar una subsección específica dentro de una sección principal
function showSubsection(parentSectionId, subsectionId) {
    showSection(parentSectionId);

    const parentSection = document.getElementById(parentSectionId);
    const selectedSubsection = document.getElementById(subsectionId);

    if (selectedSubsection) {
        const subsections = parentSection.querySelectorAll('.subsection-content');
        subsections.forEach(subsection => subsection.classList.add('hidden'));

        selectedSubsection.classList.remove('hidden');
    }
}

// Manejar el envío de formularios genéricamente
function handleFormSubmit(formId, endpoint, successMessage, callback) {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', event => {
            event.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(() => {
                    alert(successMessage);
                    form.reset();
                    if (callback) callback();
                })
                .catch(error => console.error('Error al enviar el formulario:', error));
        });
    }
}

// ===========================
// FUNCIONES AUXILIARES
// ===========================

// Actualizar estado de los botones del menú
function updateMenuState(sectionId) {
    const buttons = document.querySelectorAll('.menu-btn');
    buttons.forEach(button => {
        if (button.getAttribute('data-section') === sectionId) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

// Ocultar todas las subsecciones de una sección principal
function hideSubsections(selectedSection) {
    if (selectedSection) {
        const subsections = selectedSection.querySelectorAll('.subsection-content');
        subsections.forEach(subsection => subsection.classList.add('hidden'));
    }
}

// ===========================
// FUNCIONES DE FETCH
// ===========================

// Cargar la lista de materiales
function fetchMaterials() {
    const materialList = document.getElementById('materialList');
    materialList.innerHTML = '<p>Cargando materiales...</p>';

    fetch('/api/materiales')
        .then(response => response.json())
        .then(materials => {
            materialList.innerHTML = materials.length ? '' : '<p>No hay materiales registrados.</p>';
            renderTable(materials, materialList, ['Nombre', 'Resistencia', 'Modula de Elasticidad','Densidad'], item => `
                <tr>
                    <td>${item.nombre}</td>
                    <td>${item.resistencia_traccion} MPa</td>
                    <td>${item.modulo_elasticidad} GPa</td>
                    <td>${item.densidad} kg/m³</td>
                </tr>
            `);
        })
        .catch(() => materialList.innerHTML = '<p>Error al cargar los materiales.</p>');
}

function fetchMaterialsList() {
    const materialSelect = document.getElementById('material_id');
    materialSelect.innerHTML = '<option value="">Cargando materiales...</option>';

    fetch('/api/materiales')  // Cambia esto con la URL real de tu API
        .then(response => response.json())
        .then(materials => {
            if (materials.length === 0) {
                materialSelect.innerHTML = '<option value="">No hay materiales registrados.</option>';
                return;
            }

            materialSelect.innerHTML = '<option value="">Seleccione un material</option>';
            materials.forEach(material => {
                const option = document.createElement('option');
                option.value = material.id_material;
                option.textContent = material.nombre;
                materialSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar los materiales:', error);
            materialSelect.innerHTML = '<option value="">Error al cargar materiales</option>';
        });
}

// Cargar la lista de puentes
function fetchBridges() {
    const puenteList = document.getElementById('puenteList');
    puenteList.innerHTML = '<p>Cargando puentes...</p>';

    fetch('/api/puentes')
        .then(response => response.json())
        .then(puentes => {
            puenteList.innerHTML = puentes.length ? '' : '<p>No hay puentes registrados.</p>';
            renderTable(puentes, puenteList, ['ID Puente', 'Nombre', 'Material', 'Longitud', 'Ancho', 'Altura', 'Carga Máxima'], item => `
                <tr>
                    <td>${item.id_puente}</td>
                    <td>${item.nombre}</td>
                    <td>${item.material}</td>
                    <td>${item.longitud}</td>
                    <td>${item.ancho}</td>
                    <td>${item.altura}</td>
                    <td>${item.carga_maxima}</td>
                </tr>
            `);
        })
        .catch(() => puenteList.innerHTML = '<p>Error al cargar los puentes.</p>');
}

function fetchBridgesList() {
    const puenteSelect = document.getElementById('puente_id');  // Coincide con el ID en el HTML
    
    // Verificar que el select esté presente
    if (!puenteSelect) {
        console.error('El select con id "puente_id" no se encuentra en el DOM');
        return;  // Salir de la función si no se encuentra el elemento
    }

    puenteSelect.innerHTML = '<option value="">Cargando puentes...</option>';

    fetch('/api/puentes')  // Cambia esto con la URL real de tu API
        .then(response => response.json())
        .then(bridges => {
            if (bridges.length === 0) {
                puenteSelect.innerHTML = '<option value="">Selecciona un puente</option>';
                return;
            }

            puenteSelect.innerHTML = '<option value="">Selecciona un puente</option>';
            bridges.forEach(puente => {
                const option = document.createElement('option');
                option.value = puente.id_puente;
                option.textContent = puente.nombre;
                puenteSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error al cargar los puentes:', error);
            puenteSelect.innerHTML = '<option value="">Error al cargar puentes</option>';
        });
}

// Cargar la lista de cálculos
function fetchCalculations() {
    const calculoResult = document.getElementById('calculoResult');
    calculoResult.innerHTML = '<p>Cargando cálculos...</p>';

    fetch('/api/calculos')
        .then(response => response.json())
        .then(calculos => {
            calculoResult.innerHTML = calculos.length ? '' : '<p>No hay cálculos registrados.</p>';
            renderTable(calculos, calculoResult, ['Puente','Factor de Seguridad','Resistencia Calculada','Resultado Final', 'Fecha de Cálculo'], item => `
                <tr>
                    <td>${item.nombre_puente}</td>
                    <td>${item.factor_seguridad}</td>
                    <td>${item.resistencia_calculada} MPa</td>
                    <td>${item.resultado_final} MPa</td>
                    <td>${item.fecha_calculo}</td>
                </tr>
            `);
        })
        .catch(() => calculoResult.innerHTML = '<p>Error al cargar los cálculos.</p>');
}

// ===========================
// GENERACIÓN DINÁMICA
// ===========================

// Crear una tabla dinámica
function renderTable(data, container, headers, rowTemplate) {
    const table = document.createElement('table');

    const thead = document.createElement('thead');
    thead.innerHTML = `<tr>${headers.map(header => `<th>${header}</th>`).join('')}</tr>`;
    table.appendChild(thead);

    const tbody = document.createElement('tbody');
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = rowTemplate(item);
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    container.appendChild(table);
}

// ===========================
// INICIALIZACIÓN
// ===========================
document.addEventListener('DOMContentLoaded', () => {
    showSection('welcome');

    document.querySelectorAll('.menu-btn').forEach(button => {
        button.addEventListener('click', () => {
            const sectionId = button.getAttribute('data-section');
            showSection(sectionId);
        });
    });

    document.querySelectorAll('.sub-menu-btn').forEach(button => {
        button.addEventListener('click', () => {
            const parentSectionId = button.closest('ul').previousElementSibling.getAttribute('data-section');
            const subsectionId = button.getAttribute('data-subsection');
            showSubsection(parentSectionId, subsectionId);
        });
    });
    fetchBridgesList(); // Llama a la función para cargar los puentes
    handleFormSubmit('materialForm', '/api/materiales', '¡Material agregado exitosamente!', fetchMaterials);
    handleFormSubmit('puenteForm', '/api/puentes', '¡Puente agregado exitosamente!', fetchBridges);
    handleFormSubmit('calculoForm', '/api/calcular_resistencia', '¡Cálculo realizado exitosamente!', fetchCalculations);

    // Verificar la existencia de los botones antes de asignar eventos
    const listarMaterialesBtn = document.querySelector('[data-subsection="listar-materiales"]');
    if (listarMaterialesBtn) {
        listarMaterialesBtn.addEventListener('click', fetchMaterials);
    } else {
        console.warn('El botón para listar materiales no se encontró en el DOM.');
    }

    const listarPuentesBtn = document.querySelector('[data-subsection="listar-puentes"]');
    if (listarPuentesBtn) {
        listarPuentesBtn.addEventListener('click', fetchBridges);
    } else {
        console.warn('El botón para listar puentes no se encontró en el DOM.');
    }

    const listarCalculosBtn = document.querySelector('[data-subsection="listar-calculos"]');
    if (listarCalculosBtn) {
        listarCalculosBtn.addEventListener('click', fetchCalculations);
    } else {
        console.warn('El botón para listar cálculos no se encontró en el DOM.');
    }

    // Función para cargar la lista de materiales
    if (typeof fetchMaterialsList === 'function') {
        fetchMaterialsList();  // Verifica que esta función esté definida
    } else {
        console.warn('La función fetchMaterialsList no está definida.');
    }

    // Verifica si la función fetchBridgesList está definida
    if (typeof fetchBridgesList === 'function') {
        fetchBridgesList();  // Llama a la función si está definida
    } else {
        console.warn('La función fetchBridgesList no está definida.');
    }
});
