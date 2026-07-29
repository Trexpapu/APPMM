"""
Script para inyectar estilos modernos individuales en cada HTML de la app veterinaria.
Agrega un bloque {% block extra_head %} con CSS premium en cada archivo seleccionado.
"""
import os
import re

# Estilos modernos a inyectar en FORMULARIOS (crear/editar)
FORM_STYLES = """{% block extra_head %}
<style>
  /* ====== FORMULARIO MODERNO PREMIUM ====== */
  .container { padding: 2rem 2.5rem; max-width: 1100px; margin: 0 auto; }

  /* Header de página */
  .header-actions {
    background: linear-gradient(135deg, #0d47a1 0%, #00838f 100%);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    box-shadow: 0 8px 24px rgba(13, 71, 161, 0.25);
  }
  .header-actions h2 {
    color: #fff;
    margin: 0;
    font-size: 1.7rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }
  .header-actions h2 i { opacity: 0.9; }

  /* Secciones de formulario */
  .form-section {
    background: #ffffff;
    border-radius: 18px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e8edf5;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.25s ease;
  }
  .form-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, #1e88e5, #00acc1);
  }
  .form-section:hover { box-shadow: 0 8px 30px rgba(0,0,0,0.1); }

  .form-section h3 {
    color: #0d47a1;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 1.5rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #eef1f7;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* Grid de campos */
  .form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
  }
  .form-group { margin-bottom: 0; }
  .form-group.full-width { grid-column: 1 / -1; }

  /* Labels */
  .form-group label, form label {
    display: block;
    font-size: 0.78rem;
    font-weight: 700;
    color: #546e7a;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 0.45rem;
  }

  /* Inputs, selects, textareas */
  .form-control, .search-input, .searchable-dropdown, .filtro-input,
  input[type="text"], input[type="number"], input[type="date"],
  input[type="datetime-local"], input[type="email"], input[type="tel"],
  select, textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1.5px solid #dde3ef;
    border-radius: 10px;
    font-size: 0.95rem;
    font-family: 'Inter', sans-serif;
    color: #263238;
    background: #f8fafd;
    box-sizing: border-box;
    transition: border-color 0.2s, box-shadow 0.2s, background 0.2s, transform 0.15s;
    outline: none;
    -webkit-appearance: none;
    appearance: none;
  }
  .form-control:focus, .search-input:focus, .searchable-dropdown:focus,
  input[type="text"]:focus, input[type="number"]:focus, input[type="date"]:focus,
  input[type="datetime-local"]:focus, input[type="email"]:focus, input[type="tel"]:focus,
  select:focus, textarea:focus {
    border-color: #1e88e5;
    background: #fff;
    box-shadow: 0 0 0 3px rgba(30,136,229,0.12);
    transform: translateY(-1px);
  }
  textarea { min-height: 110px; resize: vertical; line-height: 1.6; }
  select {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='%23546e7a' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    padding-right: 2.5rem;
    cursor: pointer;
  }

  /* Errores */
  .alert.alert-error {
    background: #fff5f5;
    border-left: 4px solid #e53935;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    color: #c62828;
    margin-bottom: 1.25rem;
    font-size: 0.9rem;
  }
  .field-errors {
    color: #e53935;
    font-size: 0.82rem;
    margin-top: 0.35rem;
    padding: 0.4rem 0.7rem;
    background: rgba(229,57,53,0.07);
    border-radius: 6px;
    border-left: 3px solid #e53935;
  }
  .help-text {
    color: #78909c;
    font-size: 0.8rem;
    margin-top: 0.35rem;
    display: block;
  }

  /* Botones de acción */
  .action-buttons {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin-top: 1.5rem;
    align-items: center;
  }
  .btn-home, .btn-agregar, .btn-regresar,
  button[type="submit"] {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.6rem;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    border: none;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s, filter 0.2s;
  }
  button[type="submit"] {
    background: linear-gradient(135deg, #43a047, #66bb6a);
    color: #fff;
    box-shadow: 0 4px 14px rgba(67,160,71,0.35);
  }
  button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(67,160,71,0.45);
    filter: brightness(1.05);
  }

  /* Info-grid para paneles de datos de mascota */
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 0.5rem;
  }
  .info-item {
    background: #f4f7fb;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border: 1px solid #e4eaf5;
    border-left: 3px solid #1e88e5;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .info-item:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.07); }
  .info-item.full-width { grid-column: 1 / -1; }
  .info-item strong {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    color: #546e7a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.4rem;
  }
  .info-item span, .info-item p { color: #263238; font-size: 0.95rem; margin: 0; }
  .info-content, .content-box {
    background: #f8fafd;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    border: 1px solid #e4eaf5;
    color: #37474f;
    line-height: 1.6;
    margin-top: 0.3rem;
  }

  .info-section { margin-bottom: 1.5rem; }
  .info-section h4 {
    color: #0d47a1;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.75rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #eef1f7;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* Alerts de información */
  .alert-info {
    background: linear-gradient(135deg, #e0f7fa, #b2ebf2);
    border-left: 4px solid #00acc1;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
  }
  .btn-group { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.75rem; }

  /* Grupo de documentos */
  .documento-group {
    background: #f4f7fb;
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    border: 1px dashed #b0bec5;
  }

  /* Responsivo */
  @media (max-width: 768px) {
    .container { padding: 1rem; }
    .form-grid { grid-template-columns: 1fr; }
    .header-actions { border-radius: 12px; padding: 1rem; }
    .header-actions h2 { font-size: 1.3rem; }
    .form-section { padding: 1.25rem; border-radius: 12px; }
    .action-buttons { flex-direction: column; }
    .btn-home, .btn-agregar, .btn-regresar, button[type="submit"] { width: 100%; justify-content: center; }
  }
</style>
{% endblock %}"""


# Estilos para páginas de DETALLE (ver información)
DETAIL_STYLES = """{% block extra_head %}
<style>
  /* ====== DETALLE / VER - DISEÑO PREMIUM ====== */
  .container { padding: 2rem 2.5rem; max-width: 1100px; margin: 0 auto; }

  /* Header */
  .header-actions {
    background: linear-gradient(135deg, #0d47a1 0%, #00838f 100%);
    border-radius: 18px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    box-shadow: 0 8px 24px rgba(13, 71, 161, 0.25);
  }
  .header-actions h2 {
    color: #fff;
    margin: 0;
    font-size: 1.7rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }
  .header-actions .action-buttons { margin: 0; }

  /* Tarjetas de sección */
  .form-section {
    background: #ffffff;
    border-radius: 18px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    border: 1px solid #e8edf5;
    position: relative;
    overflow: hidden;
  }
  .form-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, #1e88e5, #00acc1);
  }
  .form-section h3 {
    color: #0d47a1;
    font-size: 1.15rem;
    font-weight: 700;
    margin: 0 0 1.25rem 0;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #eef1f7;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .form-section h3 i { color: #1e88e5; }

  /* Grid de info */
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1rem;
  }
  .info-grid.compact { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); }
  .info-item {
    background: #f4f7fb;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    border: 1px solid #e4eaf5;
    border-left: 3px solid #1e88e5;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  .info-item:hover { transform: translateY(-2px); box-shadow: 0 4px 14px rgba(30,136,229,0.1); }
  .info-item.full-width { grid-column: 1 / -1; }
  .info-item strong {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #546e7a;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
  }
  .info-item p, .info-item span { color: #263238; font-size: 0.97rem; margin: 0; line-height: 1.5; }

  /* Contenido de texto largo */
  .content-box, .info-content, .description-content,
  .health-content, .complications-content {
    background: #f4f7fb;
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    border: 1px solid #dde3ef;
    color: #37474f;
    line-height: 1.7;
    min-height: 40px;
    margin-top: 0.3rem;
  }

  /* Información de sección con sub-títulos */
  .info-section { margin-bottom: 1.75rem; }
  .info-section:last-child { margin-bottom: 0; }
  .info-section h4 {
    color: #0d47a1;
    font-size: 1rem;
    font-weight: 700;
    margin: 0 0 0.85rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #e8edf5;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  /* Badges */
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.8rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }
  .badge-success { background: #e8f5e9; color: #2e7d32; border: 1px solid #a5d6a7; }
  .badge-danger  { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; }
  .badge-info    { background: #e0f7fa; color: #00838f; border: 1px solid #80deea; }
  .badge-warning { background: #fff8e1; color: #f57f17; border: 1px solid #ffe082; }

  /* Botones de acción */
  .action-buttons {
    display: flex;
    gap: 0.75rem;
    flex-wrap: wrap;
    align-items: center;
    margin-top: 1.5rem;
  }
  .action-buttons.compact { margin-top: 0; justify-content: center; }
  .btn-home, .btn-agregar, .btn-regresar {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.65rem 1.4rem;
    border-radius: 10px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s, filter 0.2s;
    color: #fff;
  }
  .btn-home:hover, .btn-agregar:hover, .btn-regresar:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.18);
    filter: brightness(1.07);
  }

  /* Tabla */
  .custom-table-container {
    border-radius: 14px;
    overflow-x: auto;
    overflow-y: visible;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #e8edf5;
    margin-top: 1rem;
    -webkit-overflow-scrolling: touch;
  }
  .custom-table { width: 100%; border-collapse: collapse; }
  .custom-table thead th {
    background: linear-gradient(135deg, #1e88e5, #00acc1);
    color: #fff;
    padding: 1rem 1.25rem;
    font-size: 0.82rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: left;
    white-space: nowrap;
  }
  .custom-table tbody td {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid #f0f4fa;
    color: #37474f;
    font-size: 0.93rem;
    vertical-align: middle;
  }
  .custom-table tbody tr:last-child td { border-bottom: none; }
  .custom-table tbody tr:hover { background: #f4f8ff; }
  .custom-table tbody tr:nth-child(even) { background: #f9fbff; }
  .custom-table tbody tr:nth-child(even):hover { background: #f0f5ff; }

  /* No-data */
  .no-data {
    text-align: center;
    color: #90a4ae;
    padding: 2.5rem;
    font-style: italic;
    background: #f4f7fb;
    border-radius: 12px;
    border: 2px dashed #dde3ef;
    margin: 1rem 0;
  }

  /* Documentos */
  .documentos-list { display: flex; flex-direction: column; gap: 0.75rem; }
  .documento-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 1.25rem;
    background: #f4f7fb;
    border-radius: 12px;
    border: 1px solid #dde3ef;
    border-left: 4px solid #1e88e5;
    gap: 1rem;
    flex-wrap: wrap;
  }
  .documento-info strong { display: block; color: #263238; font-size: 0.95rem; }
  .documento-info small { color: #78909c; font-size: 0.8rem; }

  /* Fotos */
  .photos-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 0.5rem;
  }
  .photo-container {
    background: #f4f7fb;
    border-radius: 14px;
    padding: 1.25rem;
    text-align: center;
    border: 1px solid #e4eaf5;
  }
  .photo-container h4 { color: #0d47a1; margin: 0 0 1rem 0; font-size: 1rem; }
  .operation-photo {
    max-width: 100%;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    border: 2px solid #fff;
  }
  .no-photo {
    padding: 2rem;
    color: #90a4ae;
    background: #eceff1;
    border-radius: 10px;
    border: 2px dashed #b0bec5;
  }

  /* Responsivo */
  @media (max-width: 768px) {
    .container { padding: 1rem; }
    .header-actions { border-radius: 12px; padding: 1rem; flex-direction: column; }
    .header-actions h2 { font-size: 1.3rem; }
    .form-section { padding: 1.25rem; border-radius: 12px; }
    .info-grid, .form-grid { grid-template-columns: 1fr; }
    .action-buttons { flex-direction: column; }
    .btn-home, .btn-agregar, .btn-regresar { width: 100%; justify-content: center; }
    .custom-table-container { overflow-x: auto; }
    .documento-item { flex-direction: column; align-items: flex-start; }
  }
</style>
{% endblock %}"""


# Archivos de formularios (crear/editar)
FORM_FILES = [
    "templates/agenda/proximasCitas/agendarCita.html",
    "templates/agenda/proximasCitas/editarProximaCita.html",
    "templates/clientesMascotas/Clientes/agregarCliente.html",
    "templates/clientesMascotas/Clientes/editarCliente.html",
    "templates/clientesMascotas/Mascotas/agregarMascota.html",
    "templates/clientesMascotas/Mascotas/editarMascota.html",
    "templates/consultasMedicas/consultasMedicasBase/nuevaConsulta.html",
    "templates/consultasMedicas/consultasMedicasBase/editarConsulta.html",
    "templates/estetica/nuevoServicio.html",
    "templates/estetica/editarServicio.html",
    "templates/guarderiaHospitalizacion/guarderia/nuevoServicio.html",
    "templates/guarderiaHospitalizacion/guarderia/editarServicio.html",
    "templates/guarderiaHospitalizacion/hospitalizacion/nuevoServicio.html",
    "templates/guarderiaHospitalizacion/hospitalizacion/editarServicio.html",
    "templates/procedimientos/operaciones/nuevaOperacion.html",
    "templates/procedimientos/operaciones/editarOperacion.html",
    "templates/procedimientos/vacunaciones/nuevaVacunacion.html",
    "templates/procedimientos/vacunaciones/editarVacunacion.html",
    "templates/procedimientos/desparasitaciones/nuevaDesparasitacion.html",
    "templates/procedimientos/desparasitantes/agregarDesparasitante.html",
    "templates/procedimientos/desparasitantes/editarDesparasitante.html",
    "templates/procedimientos/vacunas/agregarVacuna.html",
    "templates/procedimientos/vacunas/editarVacuna.html",
]

# Archivos de detalle/ver
DETAIL_FILES = [
    "templates/clientesMascotas/Clientes/detalleCliente.html",
    "templates/clientesMascotas/Clientes/VerClientes.html",
    "templates/clientesMascotas/Mascotas/DetalleMascota.html",
    "templates/clientesMascotas/Mascotas/verMascotas.html",
    "templates/consultasMedicas/consultasMedicasBase/verConsultas.html",
    "templates/consultasMedicas/consultasMedicasBase/verDetalleConsulta.html",
    "templates/consultasMedicas/consultasMedicasBase/recetaMedica.html",
    "templates/estetica/detalleServicio.html",
    "templates/estetica/historialServicios.html",
    "templates/guarderiaHospitalizacion/guarderia/detalleServicio.html",
    "templates/guarderiaHospitalizacion/guarderia/historialGuarderia.html",
    "templates/guarderiaHospitalizacion/hospitalizacion/detalleServicio.html",
    "templates/guarderiaHospitalizacion/hospitalizacion/historialHospitalizacion.html",
    "templates/procedimientos/operaciones/detalleOperacion.html",
    "templates/procedimientos/operaciones/verOperaciones.html",
    "templates/procedimientos/vacunaciones/verVacunaciones.html",
    "templates/procedimientos/desparasitaciones/verDesparasitaciones.html",
    "templates/procedimientos/desparasitantes/verDesparasitantes.html",
    "templates/procedimientos/vacunas/verVacunas.html",
    "templates/agenda/proximasCitas/verProximasCitas.html",
]


def inject_styles(filepath, styles_block, base_dir):
    full_path = os.path.join(base_dir, filepath)
    if not os.path.exists(full_path):
        print(f"  [SKIP] No encontrado: {filepath}")
        return

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya tiene el bloque extra_head con estilos nuestros, lo reemplazamos
    # Buscar patrón de bloque extra_head existente
    pattern = r'\{%\s*block extra_head\s*%\}.*?\{%\s*endblock\s*%\}'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, styles_block, content, flags=re.DOTALL)
        print(f"  [UPDATE] {filepath}")
    else:
        # Insertar justo después de la primera línea ({% extends ... %})
        lines = content.split('\n')
        insert_after = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('{%') and 'extends' in line:
                insert_after = i
                break
        lines.insert(insert_after + 1, '\n' + styles_block + '\n')
        new_content = '\n'.join(lines)
        print(f"  [INJECT] {filepath}")

    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    base_dir = r"c:\Users\emman\Desktop\Mascotas Morelia\APPSMascotasMorelia"
    
    print("=== Inyectando estilos modernos en formularios ===")
    for f in FORM_FILES:
        inject_styles(f, FORM_STYLES, base_dir)

    print("\n=== Inyectando estilos modernos en páginas de detalle/ver ===")
    for f in DETAIL_FILES:
        inject_styles(f, DETAIL_STYLES, base_dir)

    print("\n✅ ¡Listo! Todos los archivos HTML han sido actualizados.")


if __name__ == "__main__":
    main()
