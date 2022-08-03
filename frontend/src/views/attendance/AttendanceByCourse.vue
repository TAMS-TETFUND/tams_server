<template>
    <section>
        <h3 class="mx-auto mb-5 text-center">Attendance Records: By Courses</h3>

        <div v-if="apiFetchFail"><ErrorDisplay errors="Something went wrong" /></div>
        <template v-if="sessions_breakdown">
            <table class="table table-dark table-striped text-light">
                <thead>
                    <tr>
                        <th scope="col">Session</th>
                        <th scope="col">Course</th>
                        <th scope="col">Lectures/Labs</th>
                        <th scope="col">Exams</th>
                        <th scope="col">Continuous Assessments</th>
                        <th scope="col">Number of Staff</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="session in sessions_breakdown" v-bind:key="session.code">
                        <td>{{ session.session }}</td>
                        <td>
                            <a v-bind:href="'/session/'+ session.id">
                            {{ session.course }}</a>
                        </td>
                        <td>{{ session.lectures }}</td>
                        <td>{{ session.exams }}</td>
                        <td>{{ session.quiz }}</td>
                        <td>{{ session.initiators_count }}</td>
                    </tr>
                </tbody>
            </table>
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
            attendance_sessions: null,
            apiFetchFail: false,
            sessions_breakdown: []
        }
    },
    components: {
        ErrorDisplay,
        TableSkeleton
    },
    async mounted(){
        await axios
        .get(`/api/v1/attendance/by-course/`, {
            headers: {Authorization: 'Token ' + this.$store.state.token}
        })
        .then(response =>{
            let courseList = []
            let initiatorList = []
            for (let i in response.data){
                courseList.push([response.data[i].course.code, response.data[i].session.session])
                initiatorList.push(response.data[i].initiator)
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

            let lectureAndLabsCount, ExamCount, QuizCount
            for (let x in uniqueCourseList){
                lectureAndLabsCount = 0 
                ExamCount = 0
                QuizCount = 0
                for ( let y in response.data){
                    if (response.data[y].course.code == uniqueCourseList[x][0] && response.data[y].session.session == uniqueCourseList[x][1]){
                        if (response.data[y].event_type_detail == "Lecture" || response.data[y].event_type_detail == "Lab"){
                            lectureAndLabsCount = lectureAndLabsCount + 1
                        }
                        if (response.data[y].event_type_detail == "Examination"){
                            ExamCount = ExamCount + 1
                        }
                        if (response.data[y].event_type_detail == "Quiz"){
                            QuizCount = QuizCount + 1
                        }
                    }
                }
                this.sessions_breakdown.push({
                    "course":uniqueCourseList[x][0], 
                    "session": uniqueCourseList[x][1],
                    "lectures": lectureAndLabsCount, 
                    "exams": ExamCount, 
                    "quiz": QuizCount, 
                    "initiators_count": uniqueInitiatorsArray.length
                })

            }
        })
        
    },
}
</script>