<template>
    <div class="container-fluid align-contents-center">
        <div class="my-3 text-center"><h2>Student Attendance Report</h2></div>
        <div class="card bg-secondary bg-opacity-25" v-if="student">
            <div class="card-title text-center">
                <h3>{{ full_name }}</h3>
            </div>
            <div class="card-body">
                <span>Department/Faculty: null/null</span><br>
                <span>Current Level of Study: {{ student.level_of_study * 100}}</span><br>
                <span>Possible Year of Graduation: {{student.possible_grad_yr}}</span><br>
                <span>Admission status: null</span>
            </div>
        </div>

        <div class="my-3" v-if="attendance_data">
            <table class="table table-dark table-hover bg-secondary">
                <thead>
                    <tr>
                        <th scope="col">Session</th>
                        <th scope="col">Course</th>
                        <th scope="col">Attendance Rate</th>
                        <th scope="col">Missed CA/Exam</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="record in attendance_data" :key="record">
                        <td>{{record.academic_session.session}}</td>
                        <td>{{record.course.code}}</td>
                        <td>{{ record.student_records.length / record.events.length * 100}}%</td>
                        <td>sd</td>
                    </tr>
                </tbody>

            </table>
            <!-- <span>{{attendance_data}}</span> -->
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: "StudentAttendanceReport",
    data() {
        return {
            full_name: "",
            student: null,
            attendance_data: null
        }
    },
    mounted(){
        this.set_student_details()
        this.get_attendance_data()
    },
    methods: {
        set_student_details(){
            axios
            .get("/api/v1/students/"+this.$route.params.id)
            .then(response => {
                this.student = response.data
                this.full_name = response.data.last_name .toUpperCase()+ ", " + response.data.first_name.toUpperCase()
            }
            )
            .catch(error => {
                console.log(error)
            })
        },
        get_attendance_data(){
            axios
            .get("/api/v1/attendance/student-report/"+this.$route.params.id)
            .then(response => {
                this.attendance_data = response.data
            })
            .catch(error => {
                console.log(error)
            })
        }
    },
    // computed: {
    //     missed_assessment(){
    //         if (this.attendance_data){
    //             for(let i in this.attendance_data){
    //                 for(let event in this.attendance_data[i].events){
    //                     if (this.attendance_data[i].events[event].event_type == 3)
    //                 }
    //             }
    //         }
    //     }
    // }
}
</script>