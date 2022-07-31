<template>
    <div class="log-in-page p-3 rounded-3">
        <div v-if="submitting">
            <div class="spinner-grow text-success" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>            
        </div>
        <form @submit.prevent="submitForm">
            <h3 class="pb-4">Login</h3>
            <div class="card bg-secondary bg-opacity-25 text-danger lead" v-if="errors"><b>
                <div class="card-body">
                    <p v-for="error in errors" v-bind:key="error" class="">
                        {{error.includes(":") ? error.split(":")[1] : error}}
                    </p>    
                </div>
            </b>
            </div>
            <div class="mb-3">
                <label for="Staff Number" class="col-form-label">Staff Number</label>
                <input type="text" class="form-control" v-model="username" required="required" :disabled="submitting" />
            </div>
            <div class="mb-3">
                <label for="password" class="col-form-label">Password</label>
                <input type="password" class="form-control" v-model="password" required="required" :disabled="submitting">
            </div>
            <button class="btn btn-success" type="submit" :disabled="submitting"><BIconBoxArrowInRight />Log In</button>
        </form>

    </div>
</template>

<script>
import axios from 'axios'
import { BIconBoxArrowInRight } from 'bootstrap-icons-vue'
export default {
    name: 'LogIn',
    components: {
        BIconBoxArrowInRight
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