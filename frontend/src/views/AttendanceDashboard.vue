<template>
    <section>
        <h3 class="mx-auto mb-5 text-center">Attendance Records</h3>
        <div v-if="apiFetchFail"><ErrorDisplay errors="Something went wrong" /></div>
        <template v-if="attendance_sessions">
            <table class="table table-dark table-striped text-light">
                <thead>
                    <tr>
                        <th scope="col">Session</th>
                        <th scope="col">Course</th>
                        <th scope="col">Event Type</th>
                        <th scope="col">Start Time</th>
                        <th scope="col">Duration (Hrs)</th>
                        <th scope="col">Event Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="session in attendance_sessions" v-bind:key="session.id">
                        <td>{{ session.session.session }}</td>
                        <td><a v-bind:href="urlBase + session.id">{{ session.course.code }}: {{ session.course.title }}</a></td>
                        <td>{{ session.event_type_detail }}</td>
                        <td>{{ session.start_time }}</td>
                        <td>{{ session.duration }}</td>
                        <td>{{ session.status_detail }}</td>
                    </tr>
                </tbody>
            </table>
        </template>
        <template v-else>
            <TableSkeleton cols="6" rows="7" />
        </template>
    </section>
</template>

<script>
import axios from 'axios'
import ErrorDisplay from '../components/ErrorDisplay.vue'
import TableSkeleton from '../components/TableSkeleton.vue'
export default {
    components: {
        ErrorDisplay,
        TableSkeleton
    },
    data() {
        return{
            attendance_sessions: null,
            urlBase: axios.defaults.baseURL + '/api/v1/attendance/session/',
            errors: null,
            apiFetchFail: false,
            currentRoute: []
        }
    },
    created(){
        this.currentRoute = window.location.pathname.split("/")
    },
    async mounted(){
        await axios
        .get(`/api/v1/attendance/`, {
            headers: {Authorization: 'Token ' + this.$store.state.token}
        })
        .then(response =>{
            console.log(response.data)
            this.attendance_sessions = response.data
        })
        .catch(error => {
            this.apiFetchFail = true
            this.errors.push(error)
        }) 
    },
}
</script>