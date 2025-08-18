<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TriniBot - Cursos Gratis</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>

<?php
require_once 'conexion.php'; // ← Asegúrate de incluirlo al principio
?>

<body>
    <!-- Navbar mejorada -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
        <div class="container">
            <a class="navbar-brand fw-bold" href="#">TriniBot</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="index.html">Inicio</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Cursos</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="categorias.php">Categorías</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="acerca.php">Acerca de</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Contacto</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">FAQ</a>
                    </li>
                    <li class="nav-item">
                        <a class="btn btn-outline-light ms-2" href="https://t.me/TriniBot" target="_blank">
                            <i class="bi bi-telegram"></i> Ir al Bot
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>


    <div class="container py-4">
        <h2 class="text-center mb-4">Explora Cursos Gratis y con Descuento</h2>
        <!-- Filtros -->
        <form id="filtroForm" class="mb-4">
            <div class="row">
                <div class="col-md-5 mb-2">
                    <select class="form-select" name="categoria" id="categoria">
                        <option value="">Filtrar por categoría</option>
                        <?php
                        $catStmt = $conexion->query("SELECT id, nombre FROM categorias ORDER BY nombre ASC");
                        while ($row = $catStmt->fetch(PDO::FETCH_ASSOC)) {
                            echo "<option value='{$row['id']}'>{$row['nombre']}</option>";
                        }
                        ?>
                    </select>
                </div>
                <div class="col-md-5 mb-2">
                    <select class="form-select" name="tipo_curso" id="tipo_curso">
                        <option value="">Tipo de curso</option>
                        <option value="gratis">Gratis</option>
                        <option value="descuento">Con descuento</option>
                    </select>
                </div>
                <div class="col-md-2 mb-2">
                    <button type="submit" class="btn btn-primary w-100"><i class="bi bi-search"></i> Buscar</button>
                </div>
            </div>
        </form>

        <!-- Contenedor de resultados -->
        <div id="resultadoCursos" class="row"></div>

        <!-- Contenedor de paginación -->
        <nav id="paginacion" class="mt-4 text-center"></nav>







    </div>
</body>

</html>

<script>
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("filtroForm");
    const resultadoDiv = document.getElementById("resultadoCursos");
    const paginacionDiv = document.getElementById("paginacion");

    let paginaActual = 1;

    function cargarCursos(pagina = 1) {
        const categoria = document.getElementById("categoria").value;
        const tipo = document.getElementById("tipo_curso").value;

        const params = new URLSearchParams({
            categoria: categoria,
            tipo: tipo,
            pagina: pagina
        });

        fetch(`ajax_cursos.php?${params.toString()}`)
            .then(res => res.text())
            .then(data => {
                const [cursosHTML, paginacionHTML] = data.split("<!--PAGINACION-->");
                resultadoDiv.innerHTML = cursosHTML;
                paginacionDiv.innerHTML = paginacionHTML;

                // Delegar clics en paginación
                document.querySelectorAll(".page-link").forEach(btn => {
                    btn.addEventListener("click", e => {
                        e.preventDefault();
                        const nuevaPagina = parseInt(btn.dataset.pagina);
                        if (!isNaN(nuevaPagina)) {
                            paginaActual = nuevaPagina;
                            cargarCursos(paginaActual);
                        }
                    });
                });
            });
    }

    form.addEventListener("submit", e => {
        e.preventDefault();
        paginaActual = 1;
        cargarCursos(paginaActual);
    });

    // Cargar cursos al inicio
    cargarCursos(paginaActual);
});
</script>