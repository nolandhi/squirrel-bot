<!doctype html>
<html lang="en" class="h-full bg-gray-100">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Squirrel Bot</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>

<style>
table, th, td {
  border:1px solid black;
}
</style>

<body class="h-full">
<div class="min-h-full">

    <header class="header">
        <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
            <h1 class="text-3xl font-bold tracking-tight text-gray-900"><?php echo e(request()->is('/') ? "User Nomination Table" : "Nominator Table"); ?></h1>
            <?php echo e($navbutton); ?>

        </div>
    </header>

    <main>
        <div class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">
            <table style="width:70%">
                <tr>
                    <th>name</th>
                    <th><?php echo e($tabletitle); ?></th>
                </tr>
                <?php echo e($phpcode); ?>

            </table>
        </div>
    </main>
</div>
</body>
</html>
<?php /**PATH /Users/nolan.galop/laravel/squirrelbot/resources/views/components/layout.blade.php ENDPATH**/ ?>