<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Acerca de - TriniBot</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" />
    <!-- Bootstrap Icons -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css" rel="stylesheet">

    <style>
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }

    .hero {
        background-color: #ffffff;
        padding: 60px 20px;
        border-bottom: 2px solid #e3e3e3;
    }

    .hero h1 {
        font-size: 2.5rem;
        font-weight: 700;
    }

    .section {
        padding: 40px 20px;
    }

    .section h3 {
        font-weight: 600;
        margin-bottom: 20px;
    }

    .icon-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }

    .icon-title i {
        font-size: 1.2rem;
        color: #0d6efd;
    }

    footer {
        background-color: #212529;
        color: #ffffff;
        text-align: center;
        padding: 20px 10px;
        margin-top: 40px;
    }

    a {
        color: #0d6efd;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }

    @media (max-width: 576px) {
        .hero h1 {
            font-size: 2rem;
        }
    }
    </style>
</head>

<body>

    <!-- Navegación -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-3">
        <a class="navbar-brand" href="index.php">← Volver a TriniBot</a>
    </nav>

    <!-- Hero principal -->
    <div class="hero text-center">
        <h1>Acerca de TriniBot</h1>
        <p class="lead">Tu asistente inteligente para encontrar cursos gratuitos y con descuento en línea.</p>
    </div>

    <!-- Sección: Descripción -->
    <section class="section container my-5">
        <h3 class="icon-title text-primary"><i class="bi bi-info-circle-fill"></i> ¿Qué es TriniBot?</h3>
        <p>
            <strong>TriniBot</strong> es un chatbot profesional que detecta y publica cursos <strong>gratuitos</strong>
            o con <strong>descuentos especiales</strong> de plataformas educativas como <em>Udemy, Coursera,
                FutureLearn, edX</em> y otras más.
        </p>
        <p>
            Este asistente está diseñado para <strong>todo tipo de usuarios</strong>: estudiantes, técnicos,
            profesionales, emprendedores y personas autodidactas que desean capacitarse en diferentes disciplinas, sin
            complicaciones y sin gastar de más.
        </p>
        <p>
            Con TriniBot puedes acceder a formación de calidad en áreas como tecnología, salud, ingeniería, idiomas,
            recursos humanos, entre muchas otras.
        </p>
    </section>
    <!-- Sección: Categorías por áreas -->
    <section class="section bg-light py-5">
        <div class="container">
            <h3 class="text-center mb-4 text-dark"><i class="bi bi-grid-fill"></i> Áreas de Conocimiento</h3>
            <div class="row row-cols-2 row-cols-md-4 g-4 text-center">

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-laptop fs-2 text-primary"></i>
                        <h6 class="mt-2">Tecnología</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-cpu-fill fs-2 text-success"></i>
                        <h6 class="mt-2">Programación</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-buildings fs-2 text-danger"></i>
                        <h6 class="mt-2">Construcción</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-heart-pulse-fill fs-2 text-danger"></i>
                        <h6 class="mt-2">Medicina</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-translate fs-2 text-info"></i>
                        <h6 class="mt-2">Idiomas</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-bar-chart-fill fs-2 text-warning"></i>
                        <h6 class="mt-2">Negocios</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-calculator-fill fs-2 text-secondary"></i>
                        <h6 class="mt-2">Matemáticas</h6>
                    </div>
                </div>

                <div class="col">
                    <div class="p-3 border rounded bg-white shadow-sm">
                        <i class="bi bi-people-fill fs-2 text-dark"></i>
                        <h6 class="mt-2">Recursos Humanos</h6>
                    </div>
                </div>

            </div>
        </div>
    </section>



    <!-- Sección: Objetivos -->
    <!-- Sección: Objetivos del Proyecto -->
    <section class="section container bg-light p-4 rounded shadow-sm my-5">
        <h3 class="icon-title text-primary"><i class="bi bi-bullseye me-2"></i> Objetivos del Proyecto</h3>
        <ul class="mt-3">
            <li>💡 <strong>Democratizar el acceso</strong> a la educación en línea de calidad.</li>
            <li>⏰ <strong>Ahorrar tiempo</strong> al usuario automatizando la búsqueda de cursos.</li>
            <li>🔔 <strong>Notificar de forma automática</strong> oportunidades educativas relevantes.</li>
            <li>📈 <strong>Impulsar el desarrollo personal y profesional</strong> continuo y accesible.</li>
        </ul>
    </section>


    <!-- Sección: Tecnologías -->
    <section class="section container">
        <h3 class="icon-title"><i class="bi bi-cpu"></i> Tecnologías Utilizadas</h3>
        <div class="row">
            <div class="col-md-6">
                <ul>
                    <li>Python (scrapers, lógica del bot)</li>
                    <li>Telegram Bot API</li>
                    <li>MySQL (gestión de base de datos)</li>
                </ul>
            </div>
            <div class="col-md-6">
                <ul>
                    <li>PHP (API y backend web)</li>
                    <li>HTML5, CSS3, Bootstrap</li>
                    <li>JavaScript (interacción frontend)</li>
                </ul>
            </div>
        </div>
    </section>

    <!-- Sección: Creador -->
    <!-- Sección: Sobre el Creador -->
    <section class="section container bg-light p-4 rounded shadow-sm my-5">
        <h3 class="icon-title text-primary"><i class="bi bi-person-circle me-2"></i> Sobre el Creador</h3>
        <p class="mt-3">
            <strong>Trinidad Pérez</strong> es un desarrollador con enfoque social, apasionado por la automatización,
            la educación digital y el desarrollo de herramientas que generen impacto real.
        </p>
        <p>
            <strong>TriniBot</strong> forma parte de su iniciativa <strong>Trinova DevPS</strong>, centrada en la
            creación
            de soluciones tecnológicas accesibles, prácticas y orientadas al aprendizaje global.
        </p>
    </section>

    <!-- Sección: Contacto y Redes -->
    <section class="section container text-center">
        <h3 class="icon-title justify-content-center">
            <i class="bi bi-people-fill"></i> Contáctame / Redes Sociales
        </h3>
        <p>Si tienes preguntas, sugerencias o quieres colaborar, ¡no dudes en escribirme!</p>
        <div class="d-flex flex-wrap justify-content-center gap-3 mt-4">
            <a href="https://wa.me/5211234567890" target="_blank" class="btn btn-outline-success">
                <i class="bi bi-whatsapp"></i> WhatsApp
            </a>
            <a href="https://www.linkedin.com/in/tu-perfil" target="_blank" class="btn btn-outline-primary">
                <i class="bi bi-linkedin"></i> LinkedIn
            </a>
            <a href="https://github.com/tu-usuario" target="_blank" class="btn btn-outline-dark">
                <i class="bi bi-github"></i> GitHub
            </a>
            <a href="https://facebook.com/tu.perfil" target="_blank" class="btn btn-outline-primary">
                <i class="bi bi-facebook"></i> Facebook
            </a>
        </div>
    </section>


    <!-- Pie de página -->
    <footer>
        <p>&copy; 2025 TriniBot | Desarrollado por Trinidad Pérez Santis</p>
    </footer>

</body>

</html>