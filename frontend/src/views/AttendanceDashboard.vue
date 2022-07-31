<template>
    <section>
        <h3 class="mx-auto mb-3">Attendance Records</h3>
        <div class="wx-50" v-if="apiFetchFail">
            <div class="alert alert-danger d-flex align-items-center" role="alert">
                <p class="lead"><BIconExclamationTriangle class="h2 mx-2" />Something went wrong</p>
            </div>
        </div>
        <template v-if="attendance_sessions">
            <table class="table table-dark table-striped text-light">
                <thead>
                    <tr>
                        <th scope="col">Course</th>
                        <th scope="col">Event Type</th>
                        <th scope="col">Start Time</th>
                        <th scope="col">Duration (Hrs)</th>
                        <th scope="col">Event Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="session in attendance_sessions" v-bind:key="session.id">
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
            <table class="table table-dark table-striped text-light">
                <thead>
                    <tr class="placeholder-glow">
                        <th scope="col"><span class="placeholder col-8"></span></th>
                        <th scope="col"><span class="placeholder col-8"></span></th>
                        <th scope="col"><span class="placeholder col-8"></span></th>
                        <th scope="col"><span class="placeholder col-8"></span></th>
                        <th scope="col"><span class="placeholder col-8"></span></th>
                    </tr>
                </thead>
                <tbody>
                    <tr class="placeholder-glow" v-for="row in 5" v-bind:key="row">
                        <th scope="row"><span class="placeholder col-8"></span></th>
                        <td><span class="placeholder col-8"></span></td>
                        <td><span class="placeholder col-8"></span></td>
                        <td><span class="placeholder col-8"></span></td>
                        <td><span class="placeholder col-8"></span></td>
                    </tr>
                </tbody>
            </table>
        </template>
    </section>
</template>

<script>
import axios from 'axios'
import { BIconExclamationTriangle } from 'bootstrap-icons-vue'
export default {
    components: {
        BIconExclamationTriangle
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
            this.attendance_sessions = response.data
        })
        .catch(error => {
            this.apiFetchFail = true
            this.errors.push(error)
        }) 
    },
}
</script>