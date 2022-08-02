<template>
    <div class="log-in-page p-3 rounded-3">
        <div class="row">
            <div class="col-2"></div>
            <div class="col-8 border border-success p-5">
                <h2 class="pb-4 text-center">Login</h2>
                <LoadingAnimation :visible="false" />
                <ErrorDisplay :errors="errorMessage" />
                <form @submit.prevent="submitForm">
                    <div class="row mb-3">
                        <label for="Staff Number" class="col-sm-3 col-form-label">Staff Number</label>
                        <div class="col-sm-9">
                            <input type="text" class="form-control" :class="{'opacity-50': submitting}" v-model="username" required="required" :disabled="submitting" />
                        </div>
                    </div>
                    <div class="row mb-3">
                        <label for="password" class="col-sm-3 col-form-label">Password</label>
                        <div class="col-sm-9">
                            <input type="password" class="form-control" :class="{'opacity-50': submitting}" v-model="password" required="required" :disabled="submitting" />
                        </div>
                        
                    </div>
                    <div class="col d-flex justify-content-end">
                        <button class="btn btn-success btn-lg mt-3" type="submit" :disabled="submitting"><BIconBoxArrowInRight class="mx-1" />Log In</button>
                    </div>
                    
                </form>
            </div>
            <div class="col-2"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import ErrorDisplay from '../components/ErrorDisplay.vue'
import LoadingAnimation from '../components/LoadingAnimation.vue'
import { BIconBoxArrowInRight } from 'bootstrap-icons-vue'
export default {
    name: 'LogIn',
    components: {
        BIconBoxArrowInRight,
        ErrorDisplay,
        LoadingAnimation
    },
    data() {
        return {
            username: '',
            password: '',
            message: '',
            errors: null,
            submitting: false
        }
    },
    mounted() {
        document.title = this.$route.name + ' | TAMS'
    },
    computed: {
        errorMessage() {
            if (this.errors){
                let message = ''
                for(let err in this.errors){
                    message += this.errors[err].includes(':') ? this.errors[err].split(':')[1] : this.errors[err]
                }
                return message
            }else{ return null}
        }
    },
    methods: {
        async submitForm() {
            this.submitting = true
            axios.defaults.headers.common["Authorization"] = ""

            localStorage.removeItem("token")

            const formData = {
                username: this.username,
                password: this.password
            }

            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)

                    localStorage.setItem("token", token)

                    axios.get("api/v1/users/me/", {
                        headers: {
                            Authorization: 'Token ' + token
                        }
                    }).then(response => {
                        console.log(response.data)
                        localStorage.setItem("username", response.data.username)
                        localStorage.setItem("userId", response.data.id)
                        localStorage.setItem("email", response.data.email)
                    })
                    const toPath = this.$route.query.to || '/'

                    this.$router.push(toPath)
                })
                .catch(error => {
                    this.errors = []

                    if(error.response) {
                        console.log(error.response.status)
                        if (error.response.status == 0){
                            this.errors.push('Failed to connect to server.')
                        }else{
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }}
                    } else {
                        this.errors.push('Something went wrong. Please try again')
                        console.log(JSON.stringify(error))
                    }
                })
                this.submitting = false
        }
    }
}
</script>