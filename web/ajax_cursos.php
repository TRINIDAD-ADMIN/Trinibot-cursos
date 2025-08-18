<?php
require_once 'conexion.php';

$categoria = $_GET['categoria'] ?? '';
$tipo = $_GET['tipo'] ?? '';
$pagina = max(1, (int)($_GET['pagina'] ?? 1));
$porPagina = 18;
$offset = ($pagina - 1) * $porPagina;

// Construir condiciones
$condiciones = [];
$parametros = [];

if ($categoria !== '') {
    $condiciones[] = 'categoria_id = ?';
    $parametros[] = $categoria;
}

if ($tipo !== '') {
    $condiciones[] = 'tipo = ?';
    $parametros[] = $tipo;
}

$where = $condiciones ? 'WHERE ' . implode(' AND ', $condiciones) : '';

// Total de resultados
$totalStmt = $conexion->prepare("SELECT COUNT(*) FROM recursos $where");
$totalStmt->execute($parametros);
$total = $totalStmt->fetchColumn();
$totalPaginas = ceil($total / $porPagina);

// Cursos
$query = "SELECT * FROM recursos $where ORDER BY id DESC LIMIT $porPagina OFFSET $offset";
$stmt = $conexion->prepare($query);
$stmt->execute($parametros);
$recursos = $stmt->fetchAll(PDO::FETCH_ASSOC);


 if (empty($recursos)): ?>
<div class="col-12 text-center">
    <div class="card p-5 border-0 shadow-sm bg-light">
        <div class="mb-3">
            <img src="https://cdn-icons-png.flaticon.com/512/4076/4076549.png" alt="Sin cursos" width="100">
        </div>
        <h4 class="text-muted">No hay cursos disponibles</h4>
        <p class="text-secondary">Vuelve más tarde o intenta con otro filtro.</p>
    </div>
</div>
<?php endif; 

// Generar HTML
 foreach ($recursos as $curso): ?>
<div class="col-md-4 mb-4">
    <div class="card h-100 shadow-sm">
        <div class="card-body">
            <h5 class="card-title"><?= htmlspecialchars($curso['titulo']) ?></h5>

            <p class="card-text" style="text-align: justify;">
                <?= htmlspecialchars(strlen($curso['descripcion']) > 200 ? substr($curso['descripcion'], 0, 200) . "..." : $curso['descripcion']) ?>
            </p>


            <span class="badge bg-<?= $curso['tipo'] == 'gratis' ? 'success' : 'warning' ?>">
                <?= ucfirst($curso['tipo']) ?>
            </span>
        </div>
        <div class="card-footer d-flex justify-content-between align-items-center">
            <?php if (!empty($curso['certificado']) && $curso['certificado'] == 1): ?>
            <div class="text-success d-flex align-items-center" title="Este curso ofrece certificación">
                <i class="bi bi-patch-check-fill me-1" style="font-size: 1.2rem;"></i>
                <small>Con Certificado</small>
            </div>
            <?php else: ?>
            <div></div> <!-- espacio para mantener el layout -->
            <?php endif; ?>

            <a href="<?= htmlspecialchars($curso['url']) ?>" target="_blank" class="btn btn-outline-primary btn-sm">
                Ver curso
            </a>
        </div>
    </div>
</div>
<?php endforeach; ?>


<!--PAGINACION-->
<?php if ($totalPaginas > 1): ?>
<ul class="pagination justify-content-center">
    <!-- Botón Anterior -->
    <li class="page-item <?= $pagina <= 1 ? 'disabled' : '' ?>">
        <a class="page-link" href="#" data-pagina="<?= $pagina - 1 ?>">Anterior</a>
    </li>

    <?php
    $rango = 2; // Número de páginas antes y después de la actual
    $mostrarPrimero = 1;
    $mostrarUltimo = $totalPaginas;

    for ($i = 1; $i <= $totalPaginas; $i++) {
        if (
            $i == 1 || $i == $totalPaginas || // Siempre mostrar primera y última
            ($i >= $pagina - $rango && $i <= $pagina + $rango) // Mostrar rango alrededor de actual
        ) {
            // Mostrar página
            echo '<li class="page-item ' . ($i == $pagina ? 'active' : '') . '">
                    <a class="page-link" href="#" data-pagina="' . $i . '">' . $i . '</a>
                  </li>';
        } elseif (
            $i == 2 && $pagina > $rango + 2 || // Puntos después de la primera
            $i == $totalPaginas - 1 && $pagina < $totalPaginas - $rango - 1 // Puntos antes de la última
        ) {
            echo '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }
    ?>

    <!-- Botón Siguiente -->
    <li class="page-item <?= $pagina >= $totalPaginas ? 'disabled' : '' ?>">
        <a class="page-link" href="#" data-pagina="<?= $pagina + 1 ?>">Siguiente</a>
    </li>
</ul>
<?php endif; ?>