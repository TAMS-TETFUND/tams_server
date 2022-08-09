<template>
<body class="bg-dark text-light">
    <div>
      <Navbar />
    </div>
    <div class="row flex-nowrap">
      <div class="col-xl-3 d-none d-xl-flex">
        <SideBar />
      </div>
      <div class="col-sm-12 col-xl-9 py-5 ">    
        <section class="text-white">

            <div class="container-fluid component-mount">
                <router-view v-slot="{ Component }">
                  <transition name="fade" mode="out-in">
                    <component :is="Component" />
                  </transition>
                </router-view>
            </div>
        </section>
      </div>
    </div>
</body>
</template>

<script>
import axios from 'axios'
import SideBar from './components/SideBar.vue'
import Navbar from './components/Navbar.vue'
export default {
  name: 'App',
  components: {
    SideBar,
    Navbar
  },
  beforeCreate(){
    this.$store.commit('initializeStore')

    const token = this.$store.state.token

    if(token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
  }
}
</script>


<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;700&display=swap');
body::before{
    display: block;
    content: '';
    height: 35px;
}
body{
    overflow-x: hidden;
}
html {
  min-height: 100%;
}
body {
  min-height: 100vh;
}
.face-enter-from, .fade-leave-to {
  opacity: 0;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.25s ease-out;
}
.component-mount a {
  color:#69f0ae;
}
.component-mount a:hover{
  color: #198754;
  text-decoration: none;
}
</style>
