<template>
    <div class="log-in-page p-5 rounded-3">
        <form @submit.prevent="submitForm">
            <p class="lead">Login</p>
            <div class="mb-3">
                <label for="Staff Number" class="col-form-label">Staff Number</label>
                <input type="text" class="form-control" v-model="username" />
            </div>
            <div class="mb-3">
                <label for="password" class="col-form-label">Password</label>
                <input type="password" class="form-control" v-model="password">
            </div>
            <button class="btn btn-success" type="submit"><BIconBoxArrowInRight />Log In</button>
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
            errors: []
        }
    },
    mounted() {
        document.title = this.$route.name + ' | TAMS'
    },
    methods: {
        async submitForm() {
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
                    console.log("This is where we are")
                    console.log(response.data)
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
                    if(error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                    } else {
                        this.errors.push('Something went wrong. Please try again')

                        console.log(JSON.stringify(error))
                    }
                })
        }
    }
}
</script>