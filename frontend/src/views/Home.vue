<template>
    <div class="container text-center">
        <div class="h100 p-5 bg-secondary bg-opacity-10 rounded-3">
            <h1>Time and Attendance Management System</h1>
            <button class="btn btn-success">Get Started <BIconArrowRightSquare /></button>
        </div>
    </div>    
</template>

<script>
import {BIconArrowRightSquare} from 'bootstrap-icons-vue'
export default {
    components: {
        BIconArrowRightSquare
    },
    mounted() {
        document.title = this.$route.name + ' | TAMS'
    }
}
</script>
