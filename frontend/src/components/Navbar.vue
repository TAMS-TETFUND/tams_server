<template>
    <nav class="navbar navbar-expand-lg bg-dark fixed-top border-bottom border-secondary">
        <div class="container-fluid mx-3">
            <router-link class="navbar-brand" to="/">
                <img src="../assets/logo.svg" class="img-fluid navbar-brand" alt="logo" style="max-height: 60px; max-width: 60px;">
                TAMS
            </router-link>    
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
                data-bs-target="#navmenu">
                <!-- <span class="navbar-toggler-icon bg-success"></span> -->
                <BIconList class="navbar-toggle-icon h1 text-white" />
            </button>
            <div class="collapse navbar-collapse justify-content-end" id="navmenu">
                <ul class="navbar-nav">
                    <li class="nav-item">
                    <router-link class="nav-link" to="/">Home</router-link>
                    </li>
                    <li class="nav-item dropdown" v-if="$store.state.isAuthenticated">
                      <a href="#" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">Attendance</a>
                      <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <li>
                          <router-link class="nav-link" to="/attendance/download"><span class="text-nowrap">Download Attendance</span></router-link>
                        </li>
                        <li>
                          <router-link class="nav-link" to="/attendance/by-course"><span class="text-nowrap">Attendance Analytics</span></router-link>
                        </li>
                        <li>
                          <router-link class="nav-link" to="/attendance/student-report"><span class="text-nowrap">Student Reports</span></router-link>
                        </li>    
                      </ul>
                    </li>
                    <!-- <li class="nav-item">
                    <router-link class="nav-link" to="/attendance/download">Attendance Records</router-link>
                    </li>
                    <li class="nav-item">
                    <router-link class="nav-link" to="/attendance/by-course">Attendance By Course</router-link>
                    </li> -->
                    <li class="nav-item">
                      <router-link class="nav-link" to="/draggable">Product Details</router-link>
                    </li>
                      <li class="nav-item">
                        <router-link class="nav-link" to="/draggable">Contact Us</router-link>
                    </li>
                    <template v-if="$store.state.isAuthenticated">
                    <li class="nav-item dropdown">
                    <a href="#" class="nav-link dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <b-icon-person-fill class="text-white h4"></b-icon-person-fill>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDopdown">
                        <li><router-link class="dropdown-item" to="/">Profile</router-link></li>
                        <li><button class=" btn btn-dark dropdown-item text-danger" @click="logout()">Log out</button></li>
                    </ul>
                    </li>
                    </template>
                    <li class="nav-item" v-else>
                    <router-link class="btn" to="/login">Log In</router-link>
                    </li>
                </ul>
            </div>
        </div> 
    </nav>
</template>

<script>
import axios from 'axios'
import { BIconPersonFill, BIconList } from 'bootstrap-icons-vue'
export default {
  name: 'NavBar',
  components: {
    BIconPersonFill,
    BIconList
  },
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


<style scoped>
.navbar {
  padding: 0;
}

.navbar a,
.navbar a:focus {
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 500;
  color: #69f0ae;
}

.navbar a i,
.navbar a:focus i {
  font-size: 12px;
  line-height: 0;
  margin-left: 5px;
}

.navbar a:hover,
.navbar .active,
.navbar .router-link-active,
.navbar .active:focus,
.navbar .router-link-active:focus,
.navbar li:hover>a {
  color: #198754;
  background: rgba(206, 212, 218,0.1);
}
.navbar .navbar-brand,
.navbar .navbar-brand:hover,
 .navbar .navbar-brand:focus,
 .navbar .navbar-brand:active{
    color: #fff;
    background:none;
}

.navbar .dropdown-menu {
    background: #343a40;
}
.navbar-toggle-icon {
    color:#69f0ae;
}
.navbar-toggle-icon:focus {
    border-color: #69f0ae;
}
</style>
