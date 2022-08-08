<template>
    <!-- <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
        <ul class="nav nav-pill flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start" id="menu">
            <li class="nav-item">
                <router-link class="a nav-link align-middle px-0" to="/attendance">
                    <BIconFileEarmarkArrowDownFill class="text-success mx-1"/><span class="ms-1 d-none d-md-inline text-white">Download Attendance</span>
                </router-link>
            </li>
            <li>
                <a href="#reports" data-bs-toggle="collapse" class="nav-link px-0 align-middle">
                    <BIconGraphUp class="text-success mx-1" /><span class="text-white d-none d-md-inline">Reports</span>
                </a>
                <ul class="collapse nav flex-column ms-1" id="reports" data-bs-parent="#menu">
                    <li class="w-100">
                        <router-link class="a nav-link" to="/attendance/student-report/"><BIconFileEarmarkPerson class="text-success mx-1" /><span class="d-none d-md-inline text-white">Student</span></router-link>
                    </li>
                    <li class="w-100">
                        <router-link class="a nav-link" to="/attendance/by-course"><BIconCollectionFill class="text-success mx-1" /><span class="d-none d-md-inline text-white">Course</span></router-link>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
     -->
     <aside id="sidebar" class="sidebar">

         <ul class="sidebar-nav" id="sidebar-nav">
             <li class="nav-item">
                 <router-link to="/attendance" class="nav-link">
                     <BIconFileEarmarkArrowDownFill />Download Attendance
                 </router-link>
             </li>
             <li class="nav-item">
                 <a href="#" class="nav-link collapsed" data-bs-toggle="collapse" data-bs-target="#report-nav">
                    <BIconGraphUp />Reports
                </a>
                <ul class="nav-content collapse" id="report-nav" data-bs-parent="#sidebar-nav">
                    <li>
                        <router-link to="/attendance/student-report/">
                            <BIconFileEarmarkPerson />Student
                        </router-link>
                    </li>
                    <li>
                        <router-link to="/attendance/by-course">
                            <BIconCollectionFill />Course
                        </router-link>
                    </li>
                </ul>
             </li>
         </ul>
     </aside>
</template>

<script>
import { BIconCollectionFill, BIconFileEarmarkPerson, BIconFileEarmarkArrowDownFill, BIconGraphUp } from "bootstrap-icons-vue";
export default {
    components: {
        BIconCollectionFill,
        BIconFileEarmarkPerson,
        BIconFileEarmarkArrowDownFill,
        BIconGraphUp
    }
}
</script>

<style>
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
  background-color: #fff;
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
  color: #4154f1;
  transition: 0.3;
  background: #f6f9ff;
  padding: 10px 15px;
  border-radius: 4px;
}

.sidebar-nav .nav-link i {
  font-size: 16px;
  margin-right: 10px;
  color: #4154f1;
}

.sidebar-nav .nav-link.collapsed {
  color: #012970;
  background: #fff;
}

.sidebar-nav .nav-link.collapsed i {
  color: #899bbd;
}

.sidebar-nav .nav-link:hover {
  color: #4154f1;
  background: #f6f9ff;
}

.sidebar-nav .nav-link:hover i {
  color: #4154f1;
}

.sidebar-nav .nav-link .bi-chevron-down {
  margin-right: 0;
  transition: transform 0.2s ease-in-out;
}

.sidebar-nav .nav-link:not(.collapsed) .bi-chevron-down {
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
  color: #012970;
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
  color: #4154f1;
}

.sidebar-nav .nav-content .router-link-active i {
  background-color: #4154f1;
}
</style>