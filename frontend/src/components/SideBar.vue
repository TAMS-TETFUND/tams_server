<template>
    <div class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100">
        <ul class="nav nav-pill flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start" id="menu">
            <li class="nav-item">
                <router-link class="a nav-link align-middle px-0" to="/attendance">
                    <BIconFileEarmarkArrowDownFill class="text-success mx-1"/><span class="ms-1 d-none d-sm-inline text-white">Download Attendance</span>
                </router-link>
            </li>
            <li>
                <a href="#reports" data-bs-toggle="collapse" class="nav-link px-0 align-middle">
                    <BIconGraphUp class="text-success mx-1" /><span class="text-white d-none d-sm-inline">Reports</span>
                </a>
                <ul class="collapse nav flex-column ms-1" id="reports" data-bs-parent="#menu">
                    <li class="w-100">
                        <router-link class="a nav-link" to="/"><span class="d-none d-sm-inline text-white">> Student</span></router-link>
                    </li>
                    <li class="w-100">
                        <router-link class="a nav-link" to="/attendance/by-course"><span class="d-none d-sm-inline text-white">> Course</span></router-link>
                    </li>
                </ul>
            </li>
        </ul>

    </div>
    <!-- </div> -->
</template>

<script>
import { BIconFileEarmarkArrowDownFill, BIconGraphUp } from "bootstrap-icons-vue";
export default {
    components: {
        BIconFileEarmarkArrowDownFill,
        BIconGraphUp
    }
}
</script>