<!doctype html>
<html lang="en" class="h-full bg-gray-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>My Website</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<style>
table, th, td {
  border:1px solid black;
}
</style>

<body class="h-full">
<div class="min-h-full">
    <nav class="bg-gray-800">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        </div>
        
    </nav>

    <header class="bg-white shadow">
        <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold tracking-tight text-gray-900">Data</h1>
        </div>
    </header>

    <main>
        <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
            <table style="width:100%">
                <tr>
                    <th>name</th>
                    <th>nominations</th>
                </tr>
                <?php
                    $users = DB::connection('mysql')->select("select * from users order by nominations desc");

                    foreach($users as $user)
                    {
                        echo "<tr>" . "<td>" . $user->name . "</td>" . "<td>" . $user->nominations . "</td>" ."</tr>";
                    }
                ?>
            </table>
        </div>
    </main>
</div>
</body>
</html>
<?php /**PATH /Users/nolan.galop/laravel/squirrelbot/resources/views/home.blade.php ENDPATH**/ ?>