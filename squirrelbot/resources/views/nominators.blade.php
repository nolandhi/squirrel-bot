<x-layout>
    <x-slot name="navbutton">
        <a href="/" class="text-3xl font-bold tracking-tight text-blue-700 hover:text-blue-900 header-right">users</a>
    </x-slot>
    
    <x-slot name="phpcode">
        <?php   
            $users = DB::connection('mysql')->select("select * from nominators order by times_nominated desc");

            foreach($users as $user)
            {
                echo "<tr>" . "<td>" . $user->name . "</td>" . "<td>" . $user->times_nominated . "</td>" ."</tr>";
            }
        ?>
    </x-slot>

    <x-slot name="tabletitle">
        Nominations
    </x-slot>
</x-layout>