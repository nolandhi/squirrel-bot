<?php if (isset($component)) { $__componentOriginal23a33f287873b564aaf305a1526eada4 = $component; } ?>
<?php if (isset($attributes)) { $__attributesOriginal23a33f287873b564aaf305a1526eada4 = $attributes; } ?>
<?php $component = Illuminate\View\AnonymousComponent::resolve(['view' => 'components.layout','data' => []] + (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag ? $attributes->all() : [])); ?>
<?php $component->withName('layout'); ?>
<?php if ($component->shouldRender()): ?>
<?php $__env->startComponent($component->resolveView(), $component->data()); ?>
<?php if (isset($attributes) && $attributes instanceof Illuminate\View\ComponentAttributeBag): ?>
<?php $attributes = $attributes->except(\Illuminate\View\AnonymousComponent::ignoredParameterNames()); ?>
<?php endif; ?>
<?php $component->withAttributes([]); ?>
     <?php $__env->slot('navbutton', null, []); ?> 
        <a href="/nominators" class="text-3xl font-bold tracking-tight text-blue-700 hover:text-blue-900 header-right">nominators</a>
     <?php $__env->endSlot(); ?>

     <?php $__env->slot('phpcode', null, []); ?> 
        <?php
            $users = DB::connection('mysql')->select("select * from users order by nominations desc");

            foreach($users as $user)
            {
                echo "<tr>" . "<td>" . $user->name . "</td>" . "<td>" . $user->nominations . "</td>" ."</tr>";
            }
        ?>
     <?php $__env->endSlot(); ?>

     <?php $__env->slot('tabletitle', null, []); ?> 
        Nominations
     <?php $__env->endSlot(); ?>
 <?php echo $__env->renderComponent(); ?>
<?php endif; ?>
<?php if (isset($__attributesOriginal23a33f287873b564aaf305a1526eada4)): ?>
<?php $attributes = $__attributesOriginal23a33f287873b564aaf305a1526eada4; ?>
<?php unset($__attributesOriginal23a33f287873b564aaf305a1526eada4); ?>
<?php endif; ?>
<?php if (isset($__componentOriginal23a33f287873b564aaf305a1526eada4)): ?>
<?php $component = $__componentOriginal23a33f287873b564aaf305a1526eada4; ?>
<?php unset($__componentOriginal23a33f287873b564aaf305a1526eada4); ?>
<?php endif; ?><?php /**PATH /Users/nolan.galop/laravel/squirrelbot/resources/views/users.blade.php ENDPATH**/ ?>