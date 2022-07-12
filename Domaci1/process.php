<?php

$mysqli = new mysqli("db", "root", "example");

mysqli_select_db( $mysqli, "library");

$name = '';
$author = '';
$description='';
$id='';

$update = false;
if (isset($_POST['save']))
{
    $name = $_POST['bookName'];
    $author = $_POST['authorName'];
    $description = $_POST['description'];
    
    $mysqli->query("INSERT INTO `books`(`name`, `author`, `description`) VALUES ('$name','$author','$description')")or die($mysqli->error);
    header("location: index.php");
    
}
if (isset($_GET['delete']))
{
    $id = $_GET['delete'];
    $mysqli->query("DELETE FROM `books` WHERE id=$id")or die($mysqli->error);
    header("location: index.php");
    
}



if (isset($_POST['update']))
{
    $id = $_POST['bookId'];
    $name = $_POST['bookName'];
    $author = $_POST['authorName'];
    $description = $_POST['description'];
    $update = false;
  
    $mysqli->query("UPDATE books SET name='$name', author='$author', description='$description' WHERE id=$id")or die($mysqli->error);
    header("location: index.php");
    
}