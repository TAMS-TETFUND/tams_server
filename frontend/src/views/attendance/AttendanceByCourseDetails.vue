<template>
    <section class="container-fluid bg-secondary bg-opacity-10 py-5 px-md-5 col-md-10">
        <div v-if="responseData">
            <h3 class="mx-auto mb-5 mt-3 text-center">Attendance Records: <span>{{ course.title }} ({{course.code}}) {{ session.session }}</span></h3>
            <div class="row mb-5 d-flex justify-content-center">
                <div class="col-md-4 text-center">
                    <div class="card bg-dark">
                        <div class="card-title h3">Total number of events</div>
                        <div class="card-body h3">{{responseData.all_sessions.length}}</div>
                        <div class="card-footer"><span class="me-1">Lectures/Lab:{{numberOfLecturesAndLabs}}</span><span class="me-1">Quizzes:{{numberOfQuizes}}</span><span class="me-1">Exams:{{numberOfExams}}</span></div>
                    </div>
                </div>
                <div class="col-md-4 text-center">
                    <div class="card bg-dark">
                        <div class="card-title h3">Average Attendance Rate</div>
                        <div class="card-body h3" :class="attendanceRateColor(averageAttendanceRate()/100)">{{averageAttendanceRate()}}%</div>
                        <div class="card-footer"><span class="text-dark">/</span></div>
                    </div>
                </div>
            </div>
            <div class="row d-flex justify-content-center">
                <div class="col-md-8">
                    <div class="table-responsive" style="max-height:50vh;">
                        <table class="table table-sm table-dark text-light">
                            <thead>
                                <tr>
                                    <th scope="col">Name</th>
                                    <th scope="col">Reg. No</th>
                                    <th scope="col">Attendance rate (%)</th>
                                    <th scope="col">Last 5 Events</th>
                                    <!-- <th scope="col">Missed Quiz/Exam</th> -->
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="student in responseData.student_attendance" :key="student" :class="attendancePerformance(student.valid_check_ins.length, responseData.all_sessions.length)">
                                    <td>{{student.student.last_name}} {{student.student.first_name}}</td>
                                    <td>{{student.student.reg_number}}</td>
                                    <td>{{student.valid_check_ins.length/responseData.all_sessions.length * 100}}</td>
                                    <td>
                                        <div class="d-flex">
                                            <div class="me-1" v-for="item in getLastFiveAttendanceStats(student)" :key="item">
                                            <div v-if="item"><BIconCheckCircleFill class="text-success" /></div>
                                            <div v-else><BIconXCircleFill class="text-danger" /></div>
                                            </div>
                                        </div>
                                    </td>

                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="row mt-5 d-none d-md-flex justify-content-center">
                <div class="col-md-8" style="min-height:50vh;">
                    <AttendanceGraph :x_axis="getGraphData().x_axis" :y_axis="getGraphData().y_axis" />
                </div>

            </div>
        </div>
        <div v-else>
            Failed to load data
        </div>
    </section>
</template>


<script>
import axios from 'axios'
import AttendanceGraph from '../../components/attendance/AttendanceGraph.vue'
import { BIconCheckCircleFill, BIconXCircleFill } from 'bootstrap-icons-vue'
export default {
    components: { AttendanceGraph, BIconCheckCircleFill, BIconXCircleFill },
    data() {
        return {
            dataReady: null,
            apiFetchFail: false,
            responseData: null,
            course: '',
            session: '',
            numberOfExams: 0,
            numberOfQuizes: 0,
            numberOfLecturesAndLabs: 0
        }
    },
    async mounted(){
        this.processAttendanceDetails()
    },
    computed: {
        
    },
    methods: {
        async processAttendanceDetails(){
            console.log("got here course: " + this.$route.params.course + "session: " + this.$route.params.session)

            this.dataReady = false
            await axios
            .get(`http://localhost:8009/api/v1/attendance/by-course/detail/?course=${this.$route.params.course}&session=${this.$route.params.session}`, {
                headers: {Authorization: 'Token ' + this.$store.state.token}
            })
            .then(response => {
                // console.log(response)
                this.responseData = response.data
                this.course = response.data.course
                this.session = response.data.session

                this.countEvents()
            })
            .catch(error => {
                console.log(error)
            })
        },
        attendancePerformance(studentAttendance, totalAttendance){
            let attendanceRate = studentAttendance/totalAttendance
            return this.attendanceRateColor(attendanceRate)
        },
        attendanceRateColor(rate){
            if (rate >= 0.75){
                return "text-success"
            }else if(rate >=0.5) {
                return "text-warning"
            } else {
                return "text-danger"
            }
        },
        averageAttendanceRate(){
            let studentsNumber = this.responseData.student_attendance.length
            let eventsTotal = this.responseData.all_sessions.length
            let studentAttendance = this.responseData.student_attendance
            let studentAttendanceRates = 0.0
            for(let i in studentAttendance){
                studentAttendanceRates += (studentAttendance[i].valid_check_ins.length/eventsTotal * 100)
            }
            return (studentAttendanceRates/studentsNumber).toFixed(2)
        },
        countEvents(){
            let allEvents = this.responseData.all_sessions
            let examsCount = 0
            let quizCount = 0
            let lectureAndLabCount = 0
            
            for(let i in allEvents){
                if (allEvents[i].event_type_detail == "Lab" || allEvents[i].event_type_detail == "Lecture"){
                    lectureAndLabCount += 1
                } else if (allEvents[i].event_type_detail == "Exam"){
                    examsCount += 1
                } else if(allEvents[i].event_type_detail == "Quiz"){
                    quizCount += 1
                }
            }
            this.numberOfExams = examsCount
            this.numberOfLecturesAndLabs = lectureAndLabCount
            this.numberOfQuizes = quizCount
        },
        getGraphData(){
            let attendanceSessions = this.responseData.all_sessions
            let studentsPresent = []
            let eventDate = []
            for(let i in attendanceSessions) {
                studentsPresent.push(attendanceSessions[i].student_check_in_count)
                let start_datetime = new Date(attendanceSessions[i].start_time) 
                eventDate.push(''+start_datetime.getDay()+'-'+start_datetime.getMonth()+'-'+start_datetime.getFullYear())
            }
            return { x_axis: eventDate, y_axis: studentsPresent }
        },
        getLastFiveAttendanceStats(studentAttendance){
            let lastFiveSessions = this.responseData.all_sessions.slice(-5)
            let lastFiveStudentAttendance = []
            for (let i in lastFiveSessions){
                let currentSession = false
                for (let j in studentAttendance.valid_check_ins){
                    if(Object.values(studentAttendance.valid_check_ins[j]).includes(lastFiveSessions[i].id)){
                        currentSession = true
                        break
                    }
                }
                lastFiveStudentAttendance.push(currentSession)
            }
            return lastFiveStudentAttendance
        }
    }
}
</script>