<template>
    <div class="page-content">
        <h1><BIconExclamationTriangleFill class=" text-danger display-1 pe-4 h3" /><span>Page Not Found</span></h1>
        <div class="col">
            <img src="../assets/404.svg" alt="" class="img-fluid">
        </div>
    </div>
</template>

<script>
import { BIconExclamationTriangleFill } from 'bootstrap-icons-vue'
export default {
    name: "PageNotFound",
    components: {
        BIconExclamationTriangleFill
    },
}
</script>