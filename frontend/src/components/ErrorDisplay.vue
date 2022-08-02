<template>
    <div class="container bg-secondary bg-opacity-25 lead border border-danger my-4" v-if="errors">
            <div class="row justify-content-start align-items-center">
                <div class="col-1 mx-3"><BIconExclamationTriangle class="h2 text-danger" /></div>
                <div class="col-8 justify-content-start p-1">
                    <b class="text-danger">Error</b>
                    <br>
                    {{ errors }}
                </div>
            </div>
    </div>
</template>

<script>
import { BIconExclamationTriangle } from "bootstrap-icons-vue";
export default {
    components: {
        BIconExclamationTriangle
    },
    props: ['errors']
}
</script>