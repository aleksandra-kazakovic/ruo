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
               
                    
                    <li class="nav-item text-white">
                        <a class="nav-link nav-blue"href="index.php" }}>Početna </a>
                    </li>
                    
                
                    <u class="text-white">
                        <li class="nav-item">
                            <a class="nav-link" href="home.php" >Dodaj knjigu</a>
                        </li>
                </u>

            </ul>
        </div>
    </div>
</nav>
           <div class="content row mt-5">
        <div class="col-3">

        </div>
        <div class="col-6">
        <?php require_once './process.php'; 
        
        if (isset($_GET['edit']))
        {
            $mysqli = new mysqli("db", "root", "example");

            mysqli_select_db( $mysqli, "library");
           
            $id = $_GET['edit'];
            $result = $mysqli->query("SELECT * FROM `books` WHERE id=$id")or die($mysqli->error);

            if ($result)
            {
                $update = true;
                $row = $result->fetch_assoc();
                $name = $row['name'];
                $author = $row['author'];
                $id = $row['id'];
                $description = $row['description'];
                
            }
        }
        ?>
            <form action="process.php" name="addform" id="addform" method="POST">
                <input type="hidden" name="bookId" value="<?php echo $id; ?>"> 
                <div class="form-group">
                    <label for="exampleInputEmail1">Naziv knjige</label>
                    <input type="text" class="form-control" id="bookName" name="bookName" value="<?php echo $name; ?>" required>

                </div>
                <div class="form-group">
                    <label for="exampleInputEmail1">Ime autora</label>
                    <input type="text" class="form-control" id="authorName" name="authorName" value="<?php echo $author; ?>" required>

                </div>
                <div class="form-group">
                    <label for="exampleInputEmail1">Opis</label>

                    <textarea class="form-control" id="description" rows="8"  name="description" placeholder="Zašto pročitati ovu knjigu." required> <?php echo $description; ?></textarea>

                </div>
                 <?php if($update == true){ ?>
                <button type="submit" name="update" class="btn btn-primary">Izmeni</button>
                 <?php }
                 else 
                 {
                     ?>
                 <button type="submit" name="save" class="btn btn-primary">Dodaj</button>
                <?php 
                 }
                ?>
            </form>
                  </div>

    </div>
        <?php
        // put your code here
        ?>
    </body>
</html>
