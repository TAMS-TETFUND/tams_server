<template>
    <section class="container-fluid bg-secondary bg-opacity-10 py-5 px-md-5">
        <h3 class="mx-auto mb-5 mt-3 text-center">Attendance Records: <span>{{ course }}: {{ session }}</span></h3>
    </section>
</template>


<script>
import axios from 'axios'
export default {
    data() {
        return {
            dataReady: null,
            apiFetchFail: false,
            responseData: null
        }
    },
    async mounted(){
        this.processAttendanceDetails()
    },
    methods: {
        async processAttendanceDetails(){
            console.log("got here")
            this.dataReady = false
            await axios
            .get(`/api/v1/attendance/by-course/detail?course=${this.$route.params.course}&session=${this.$route.params.session}`, {
                headers: {Authorization: 'Token ' + this.$store.state.token}
            })
            .then(response => {
                console.log(response)
            })
            .catch(error => {
                console.log(error)
            })
        }
    }
}
</script>