<template>
    <div class="container mt-5">
        <h2 class="text-center mb-3">Student Attendance Report</h2>

        <div class="col-md-6 container bg-secondary bg-opacity-10 py-5 px-md-5 mt-3">
            <ErrorDisplay :errors="error" />
            <form @submit.prevent="submitForm">
                <div class="row mb-3">
                    <label for="studentRegNumber" class="lead form-label mb-3">Enter Student Registration Number</label>
                    <div class="col-lg">
                        <input type="text" class="form-control" id="studentRegNumber" :class="{'opacity-50': submitting}" v-model="studentRegNumber" required :disabled="submitting" />
                    </div>
                </div>
                <div class="col d-flex justify-content-end">
                    <button class="btn btn-success btn-lg mb-3" type="submit" :disabled="submitting">
                        <BIconSearch class="h3 pe-2" />Search
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { BIconSearch } from "bootstrap-icons-vue";
import ErrorDisplay from "../../components/ErrorDisplay.vue"
import router from "../../router";
export default {
    components: {
        BIconSearch,
        ErrorDisplay
    },
    data(){
        return {
            submitting: false,
            studentRegNumber: "",
            error: null
        }
    },
    methods: {
        submitForm() {
            this.submitting = true
                axios
                .get("/api/v1/students/"+ this.studentRegNumber)
                .then(response => {
                    if (response.status == 200){
                        router.push("/attendance/student-report/"+this.studentRegNumber)
                    }
                })
                .catch(error => {
                    if(error.response && error.response.status == 404){
                        this.error = "No student found with that registration number"
                    }
                })
            this.submitting = false
        }
    }
}
</script>