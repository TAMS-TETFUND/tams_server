<template>
    <section class="container-fluid bg-secondary bg-opacity-10 py-5 px-md-5">
        <h3 class="mx-auto mb-5 mt-3 text-center">Attendance Records: By Courses</h3>

        <div v-if="apiFetchFail"><ErrorDisplay errors="Something went wrong" /></div>
        <template v-if="sessions_breakdown && dataReady">
            <div class="table-responsive">
                <table class="table table-sm table-dark table-striped text-light">
                    <thead>
                        <tr>
                            <th scope="col">Session</th>
                            <th scope="col">Course</th>
                            <th scope="col">Lectures/Labs</th>
                            <th scope="col">Continuous Assessments</th>
                            <th scope="col">Exams</th>
                            
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="session in sessions_breakdown" v-bind:key="session.code">
                            <td>{{ session.session }}</td>
                            <td>
                                <router-link v-bind:to="`/attendance/by-course/detail/${session.session_id}/${session.course_id}`">
                                {{ session.course }}</router-link>
                            </td>
                            <td>{{ session.lectures }}</td>
                            <td>{{ session.quiz }}</td>
                            <td>{{ session.exams }}</td>
                        </tr>
                    </tbody>
                </table>
                <div>{{sessions_breakdown}}</div>
            </div>
            <div>
                <Button type="button" class="btn btn-success btn-md mx-3" @click="loadPreviousPage()" v-if="hasPrev">Previous</Button>
                <Button type="button" class="btn btn-success btn-md" @click="loadNextPage()" v-if="hasNext">Next</Button>
            </div>
        </template >
        <TableSkeleton  rows="7" cols="6" v-else />
        <template>
            <p><b>No attendance sessions available for user.</b></p>
        </template>
    </section>
</template>

<script>
import axios from 'axios'
import ErrorDisplay from '../../components/ErrorDisplay.vue'
import TableSkeleton from '../../components/TableSkeleton.vue'
export default {
    data() {
        return{
            apiFetchFail: false,
            dataReady: null,
            sessions_breakdown: [],
            hasNext: null,
            hasPrev: null,
            currentPage: 1,
        }
    },
    components: {
        ErrorDisplay,
        TableSkeleton
    },
    async mounted(){
        this.processAttendanceSession()
    },
    methods: {
        async processAttendanceSession(){
            this.dataReady = false
        await axios
        .get(`/api/v1/attendance/by-course/`, {
            headers: {Authorization: 'Token ' + this.$store.state.token}
        })
        .then(response =>{
            this.sessions_breakdown = []
            this.hasNext = response.data.next
            this.hasPrev = response.data.previous
            let courseList = []
            let initiatorList = []
            let responseData = response.data
            for (let i in responseData){
                courseList.push([responseData[i].course.code, responseData[i].session.session, responseData[i].course.id, responseData[i].session.id])
                initiatorList.push(responseData[i].initiator)
            }
            const uniqueCourseList = courseList.filter((value, index) => {
                const _value = JSON.stringify(value);
                return index === courseList.findIndex(courseList => {
                    return JSON.stringify(courseList) === _value;
                });
            });

            const uniqueInitiatorsArray = initiatorList.filter((value, index) => {
                const _value = JSON.stringify(value)
                return index === initiatorList.findIndex(initiatorList => {
                    return JSON.stringify(initiatorList) === _value
                })
            })
            console.log(uniqueCourseList)
            let lectureAndLabsCount, ExamCount, QuizCount
            for (let x in uniqueCourseList){
                lectureAndLabsCount = 0 
                ExamCount = 0
                QuizCount = 0
                for ( let y in responseData){
                    console.log(responseData[y])
                    if (responseData[y].course.code == uniqueCourseList[x][0] && responseData[y].session.session == uniqueCourseList[x][1]){
                        if (responseData[y].event_type_detail == "Lecture" || responseData[y].event_type_detail == "Lab"){
                            lectureAndLabsCount = lectureAndLabsCount + 1
                        }
                        if (responseData[y].event_type_detail == "Examination"){
                            ExamCount = ExamCount + 1
                        }
                        if (responseData[y].event_type_detail == "Quiz"){
                            QuizCount = QuizCount + 1
                        }
                    }
                }
                this.sessions_breakdown.push({
                    "course":uniqueCourseList[x][0],
                    "session": uniqueCourseList[x][1],
                    "course_id": uniqueCourseList[x][2],
                    "session_id": uniqueCourseList[x][3],
                    "lectures": lectureAndLabsCount, 
                    "exams": ExamCount, 
                    "quiz": QuizCount, 
                    "initiators_count": uniqueInitiatorsArray.length
                })

            }
            this.dataReady = true
            console.log(uniqueCourseList)
        })
        
        },
        loadNextPage(){
            this.currentPage += 1
            this.processAttendanceSession()
        },
        loadPreviousPage(){
            this.currentPage -= 1
            this.processAttendanceSession()
        }
    }
}
</script>