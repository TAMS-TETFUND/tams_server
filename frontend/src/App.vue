<template>
<body class="bg-dark text-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark py-3 fixed-top border-bottom border-secondary">
        <div class="container">
            <router-link class="navbar-brand" to="/">TAMS</router-link>    
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navmenu">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navmenu">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                      <router-link class="nav-link a" to="/home">Dashboard</router-link>
                    </li>
                    <li class="nav-item">
                      <router-link class="nav-link a" to="/home">Attendance Records</router-link>
                    </li>

                    <template v-if="$store.state.isAuthenticated">
                    <li class="nav-item">
                      <router-link class="nav-link a" to="/profile">Profile</router-link>
                    </li>
                    <li class="nav-item">
                      <button class=" btn btn-dark nav-link a" @click="logout()">Log out</button>
                    </li>
                    </template>
                    <li class="nav-item" v-else>
                      <router-link class="nav-link a" to="/login">Log In</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <section class="p-lg-0 text-center text-white">
        <div class="container">
            <router-view />
        </div>
    </section>
</body>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  beforeCreate(){
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if(token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  },
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("email")
      localStorage.removeItem("userId")

      this.$store.commit('removeToken')

      this.$router.push('/')
    }
  }
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700&display=swap');
.wrapper {
  color: var(--body);
  font-family: Sora, "san-serif";
  line-height: 1.7;
  background-position: center;
  background-size: cover;
  background-image: url('~@/assets/background.png');
  z-index: 2;
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow-y: auto;
}

.wrapper:after {
  content: "";
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255 , 0.85);
  z-index: -1;
  overflow-y: auto;
}
body::before{
    display: block;
    content: '';
    height: 60px;
}
html {
  min-height: 100%;
}
body {
  min-height: 100vh;
}
</style>
