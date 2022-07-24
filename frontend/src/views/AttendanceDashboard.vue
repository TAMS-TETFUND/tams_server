<template>
    <section>
        <h3 class="mx-auto">Attendance Records</h3>
            <div v-if="errors">
                <p v-for="error in errors" v-bind:key="error">{{error}}</p>
            </div>
            <template v-if="attendance_sessions">
                <table class="table text-light">
                    <thead>
                        <tr>
                            <th scope="col">Course</th>
                            <th scope="col">Event Type</th>
                            <th scope="col">Start Time</th>
                            <th scope="col">Duration (Hrs)</th>
                            <th scope="col">Event Status</th>
                        </tr>
                    </thead>
                        <tr v-for="session in attendance_sessions" v-bind:key="session.id">
                            <td><a v-bind:href="urlBase + session.id">{{ session.course.code }}: {{ session.course.title }}</a></td>
                            <td>{{ session.event_type_detail }}</td>
                            <td>{{ session.start_time }}</td>
                            <td>{{ session.duration }}</td>
                            <td>{{ session.status_detail }}</td>
                        </tr>
                </table>
            </template>
            <template v-else>
                <p><b>No attendance sessions available for user.</b></p>
            </template>
    </section>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return{
            attendance_sessions: null,
            urlBase: axios.defaults.baseURL + '/api/v1/attendance/session/',
            errors: []
        }
    },
    async mounted(){
        await axios
        .get(`/api/v1/attendance/`, {
            headers: {Authorization: 'Token ' + this.$store.state.token}
        })
        .then(response =>{
            this.attendance_sessions = response.data
        })
        
    },
}
</script>