<template>
    <!-- <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
        <ul class="nav nav-pill flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start" id="menu">
            <li class="nav-item">
                <router-link class="a nav-link align-middle px-0" to="/attendance">
                    <BIconFileEarmarkArrowDownFill class="text-success me-1"/><span class="ms-1 d-none d-md-inline text-white">Download Attendance</span>
                </router-link>
            </li>
            <li>
                <a href="#reports" data-bs-toggle="collapse" class="nav-link px-0 align-middle">
                    <BIconGraphUp class="text-success me-1" /><span class="text-white d-none d-md-inline">Reports</span>
                </a>
                <ul class="collapse nav flex-column ms-1" id="reports" data-bs-parent="#menu">
                    <li class="w-100">
                        <router-link class="a nav-link" to="/attendance/student-report/"><BIconFileEarmarkPerson class="text-success me-1" /><span class="d-none d-md-inline text-white">Student</span></router-link>
                    </li>
                    <li class="w-100">
                        <router-link class="a nav-link" to="/attendance/by-course"><BIconCollectionFill class="text-success me-1" /><span class="d-none d-md-inline text-white">Course</span></router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
     -->
     <aside id="sidebar" class="sidebar bg-secondary bg-opacity-10">

         <ul class="sidebar-nav" id="sidebar-nav">
             <li class="nav-item">
                 <a href="#" class="nav-link collapsed" data-bs-toggle="collapse" data-bs-target="#report-nav">
                    <BIconGraphUp class="me-1" /><span>Reports</span><BIconChevronDown class="collapse-icon ms-auto" />
                </a>
                <ul class="nav-content collapse" id="report-nav" data-bs-parent="#sidebar-nav">
                    <li>
                        <router-link to="/attendance/student-report/">
                            <BIconFileEarmarkPerson class="me-1" />Student
                        </router-link>
                    </li>
                    <li>
                        <router-link to="/attendance/by-course">
                            <BIconCollectionFill class="me-1" />Course
                        </router-link>
                    </li>
                </ul>
             </li>
             <li class="nav-item">
                 <a href="#" class="nav-link collapsed" data-bs-toggle="collapse" data-bs-target="#download-nav">
                     <BIconDownload class="me-1" /><span>Downloads</span><BIconChevronDown class="collapse-icon ms-auto" />
                 </a>
                 <ul class="nav-content collapse" id="download-nav" data-bs-parent="#sidebar-nav">
                     <li>
                        <router-link to="/attendance/download" class="nav-link">
                            <BIconFileEarmarkArrowDownFill class="me-1" />Attendance
                        </router-link>
                     </li>
                 </ul>
             </li>
         </ul>
     </aside>
</template>

<script>
import { 
    BIconCollectionFill, 
    BIconFileEarmarkPerson, 
    BIconFileEarmarkArrowDownFill, 
    BIconGraphUp,
    BIconDownload,
    BIconChevronDown
    } from "bootstrap-icons-vue";
export default {
    components: {
        BIconCollectionFill,
        BIconFileEarmarkPerson,
        BIconFileEarmarkArrowDownFill,
        BIconGraphUp,
        BIconDownload,
        BIconChevronDown
    }
}
</script>

<style scoped>
.sidebar {
  position: fixed;
  top: 60px;
  left: 0;
  bottom: 0;
  width: 300px;
  z-index: 996;
  transition: all 0.3s;
  padding: 20px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: #aab7cf transparent;
  box-shadow: 0px 0px 20px rgba(1, 41, 112, 0.1);
  /* background-color: #fff; */
}

@media (max-width: 1199px) {
  .sidebar {
    left: -300px;
  }
}

.sidebar::-webkit-scrollbar {
  width: 5px;
  height: 8px;
  background-color: #fff;
}

.sidebar::-webkit-scrollbar-thumb {
  background-color: #aab7cf;
}

@media (min-width: 1200px) {

  #main,
  #footer {
    margin-left: 300px;
  }
}

@media (max-width: 1199px) {
  .toggle-sidebar .sidebar {
    left: 0;
  }
}

@media (min-width: 1200px) {

  .toggle-sidebar #main,
  .toggle-sidebar #footer {
    margin-left: 0;
  }

  .toggle-sidebar .sidebar {
    left: -300px;
  }
}

.sidebar-nav {
  padding: 0;
  margin: 0;
  list-style: none;
}

.sidebar-nav li {
  padding: 0;
  margin: 0;
  list-style: none;
}

.sidebar-nav .nav-item {
  margin-bottom: 5px;
}

.sidebar-nav .nav-heading {
  font-size: 11px;
  text-transform: uppercase;
  color: #899bbd;
  font-weight: 600;
  margin: 10px 0 5px 15px;
}

.sidebar-nav .nav-link {
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 600;
  color: #92f7bc;
  transition: 0.3;
  /* background: #f6f9ff; */
  background: rgba(206, 212, 218,0.1);
  padding: 10px 15px;
  border-radius: 4px;
}

.sidebar-nav .nav-link i {
  font-size: 16px;
  margin-right: 10px;
  color: #92f7bc;
}

.sidebar-nav .nav-link.collapsed {
  color: #198754;
  background: rgba(206, 212, 218,0.01);
}

.sidebar-nav .nav-link.collapsed i {
  color: #899bbd;
}

.sidebar-nav .nav-link:hover {
  color: #92f7bc;
  background: rgba(206, 212, 218,0.1);
}

.sidebar-nav .nav-link:hover i {
  color: #92f7bc;
}

.sidebar-nav .nav-link .collapse-icon {
  margin-right: 0;
  transition: transform 0.2s ease-in-out;
}

.sidebar-nav .nav-link:not(.collapsed) .collapse-icon {
  transform: rotate(180deg);
}

.sidebar-nav .nav-content {
  padding: 5px 0 0 0;
  margin: 0;
  list-style: none;
}

.sidebar-nav .nav-content a {
  display: flex;
  align-items: center;
  font-size: 14px;
  font-weight: 600;
  color: #198754;
  transition: 0.3;
  padding: 10px 0 10px 40px;
  transition: 0.3s;
}

.sidebar-nav .nav-content a i {
  font-size: 6px;
  margin-right: 8px;
  line-height: 0;
  border-radius: 50%;
}

.sidebar-nav .nav-content a:hover,
.sidebar-nav .nav-content .router-link-active {
  color: #92f7bc;
  background: rgba(206, 212, 218,0.1);

}

.sidebar-nav .nav-content .router-link-active i {
  background-color: #92f7bc;
}
</style>