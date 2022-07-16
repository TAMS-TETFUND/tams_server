<template>
    <section>
        <h3 class="mx-auto">Attendance Records</h3>
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
                            <td>
                                <a href="/session/{{session.id}}">
                                {{ session.course.code }}: {{ session.course.title }}</a>
                            </td>
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
            attendance_sessions: null
        }
    },
    async mounted(){
        await axios
        .get(`/attendance/`, {params: {Token: this.$store.state.token}})
        .then(response =>{
            console.log(response.data)
            this.attendance_sessions = response.data
        })
        
    }
}
</script>