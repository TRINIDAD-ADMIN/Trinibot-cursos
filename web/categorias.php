<?php
require_once 'conexion.php';

// Consulta
$sql = "SELECT c.nombre AS categoria, COUNT(r.id) AS total_cursos
        FROM categorias c
        LEFT JOIN recursos r ON c.id = r.categoria_id
        GROUP BY c.id, c.nombre
        ORDER BY c.nombre";

$stmt = $conexion->prepare($sql);
$stmt->execute();
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Categorías del Chatbot</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CDN para estilo responsivo -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
    <!-- Navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
        <a class="navbar-brand" href="index.php">← Volver a TriniBot</a>
    </nav>
    <div class="container mt-5">
        <h2 class="text-center mb-4">📚 Panel de Categorías del Chatbot</h2>
        <table class="table table-bordered table-hover table-striped">
            <thead class="table-dark">
                <tr>
                    <th>Categoría</th>
                    <th>Total de Cursos</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)): ?>
                <tr>
                    <td><?= htmlspecialchars($fila['categoria']) ?></td>
                    <td><?= $fila['total_cursos'] ?></td>
                </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    </div>
</body>

</html>