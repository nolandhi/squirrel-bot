<?php

use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('users');
});

Route::get('/nominators', function () {
    return view('nominators');
});
