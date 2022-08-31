<template>
    <div class="page-content bg-secondary bg-opacity-10 p-5">
        <h1 class="bg-secondary bg-opacity-10 d-flex justify-content-center">
            <BIconExclamationTriangleFill class="text-danger display-1 h3" />
            <span class="ms-5 mt-2">Page Not Found</span></h1>
        <div class="d-flex justify-content-center">
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