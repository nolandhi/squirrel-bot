<x-layout>
    <x-slot name="navbutton">
        <a href="/nominators" class="text-3xl font-bold tracking-tight text-blue-700 hover:text-blue-900 header-right">nominators</a>
    </x-slot>

    <x-slot name="phpcode">
        <?php
            $users = DB::connection('mysql')->select("select * from users order by nominations desc");

            foreach($users as $user)
            {
                echo "<tr>" . "<td>" . $user->name . "</td>" . "<td>" . $user->nominations . "</td>" ."</tr>";
            }
        ?>
    </x-slot>

    <x-slot name="tabletitle">
        Nominations
    </x-slot>
</x-layout>