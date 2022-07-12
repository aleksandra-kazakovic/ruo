<?php 


$mysqli = new mysqli("db", "root", "example");

$sql = "CREATE DATABASE IF NOT EXISTS library";
if ($mysqli->query($sql) === TRUE) {

  //echo "Database created successfully";

} else {
  echo "Error creating database: " . $conn->error;
}

mysqli_select_db( $mysqli, "library");

$sql = "CREATE TABLE books (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    description VARCHAR(255)
    )";
    $mysqli->query($sql);

?>
<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <meta charset="UTF-8">
        <title>Knjige</title>
          <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <!--     Fonts and icons     -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700,200" rel="stylesheet"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/latest/css/font-awesome.min.css"/>

    <!-- Styles -->

    <link href="paper/css/paper-kit.css" rel="stylesheet">
    <link href="paper/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg bg-primary">
    <div class="container">
        <h5 class="navbar-brand">Knjige koje vredi pročitati</h5>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
               
                    <u class="text-white">
                    <li class="nav-item text-white">
                        <a class="nav-link nav-blue"href="index.php" }}>Početna </a>
                    </li>
                    </u>
                
                    
                        <li class="nav-item">
                            <a class="nav-link" href="home.php" >Dodaj knjigu</a>
                        </li>
                

            </ul>
        </div>
    </div>
</nav>

<?php 
$results = $mysqli->query("SELECT * FROM books")or die($mysqli->error);
?>        
    <div class="content row">
        <div class="col-3 ">
        </div>
        <div class="col-6">
            <div
                class="relative flex items-top justify-center min-h-screen bg-gray-100  sm:items-center py-4 sm:pt-0">

                <div class="">
                    <div class="">
                        <table class="table table-striped">
                            <thead>
                            <tr>
                                <th scope="col"></th>
                                <th scope="col">Naziv</th>
                                <th scope="col">Autor</th>
                                <th scope="col">Opis</th>
                                <th scope="col"></th>
                                <th scope="col"></th>
                            </tr>
                            </thead>
                            <tbody>
                            <?php 
                            if(is_null($results) != true){
                            while( $res = $results->fetch_assoc()){ ?>
                                <tr>
                                    <th scope="row"></th>
                                    <td class="align-middle"><?php echo $res['name']; ?> </td>
                                    <td class="align-middle"><?php echo $res['author']; ?></td>
                                    <td class="text-justify"><?php echo $res['description']; ?></td>
                                    <td class="align-middle">
                                        <a class="btn btn-warning" href="home.php?edit=<?php echo $res['id']; ?>" ><i class="nc-icon nc-ruler-pencil"></i></a>

                                    </td>
                                    <td class="align-middle">
                                        <a class="btn btn-danger" href="process.php?delete=<?php echo $res['id']; ?>" ><i class="nc-icon nc-simple-remove"></i></a>

                                    </td>

                                </tr>
                            <?php }
                            } ?>


                            </tbody>
                        </table>

                    </div>


                </div>

            </div>
        </div>

    </div>
        <?php
        // put your code here
        ?>
    </body>
</html>

