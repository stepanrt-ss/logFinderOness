<?php
    $_POST = json_decode(file_get_contents('php://input'), true);
    $login = $_POST['login'];
    $password = $_POST['password'];

    foreach ($_COOKIE as $key => $value) {
        if ($key == 'auth_token') {
            echo $login;
        }
    }


    function check_cookies() {

    }

    function add_cookies() {

    }