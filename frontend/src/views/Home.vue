<template>
    <div class="g-4" style="overflow-y:hidden">
        <div class="p-5 rounded-3 mb-5">
            <div class="row">
                <div class="col-xs-12 col-sm-6 d-sm-flex">
                    <img src="../assets/fingerprint.svg" alt="Fingerprint" class="img-fluid">
                </div>
                <div class="col-xs-12 col-sm-6 d-flex align-items-start">
                    <div class="row">
                        <h1>Welcome to TAMS</h1>
                        <p class="lead">
                            A multi-modal biometric attendance management solution crafted for African schools.
                        </p>
                        <router-link to="/" class="btn btn-success text-white col-md-4"><span class="me-1">Learn More</span><BIconArrowRightSquare /></router-link>
                    </div>                    
                </div>
            </div>
        </div>
        <div class="mt-5 border-top border-success p-5">
            <div class="text-center h3 text-capitalize my-4">
            <span>Features curently supported</span>
            </div>
            <div class="row d-flex justify-content-start mb-5">
                <div class="col-md-3 d-md-flex align-items-stretch py-3">
                    <div class="card bg-success bg-opacity-10 text-white border border-success">
                        <div class="card-body text-center">
                        <BIconUiChecks class="text-warning h1" />
                        <h3 class="card-title text-capitalize">Multi-modal Biometric Verification</h3>
                        <p class="card-text">
                            Supports fingerprint and face verification
                        </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 d-md-flex align-items-stretch py-3">
                    <div class="card bg-success bg-opacity-10 text-white border border-success">
                        <div class="card-body text-center">
                        <BIconFileEarmarkBarGraphFill class="text-warning h1" />
                        <h3 class="card-title text-capitalize">Auto-generated Attendance Breakdowns</h3>
                        <p class="card-text">
                            Generates student attendance reports. Makes it easy identify students with low attendance.
                        </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-3 d-md-flex align-items-stretch py-3">
                    <div class="card bg-success bg-opacity-10 text-white border border-success">
                        <div class="card-body text-center">
                        <BIconWifiOff class="text-warning h1" />
                        <h3 class="card-title text-capitalize">Works 100% Offline</h3>
                        <p class="card-text">
                            The attedance-logging devices do not rely on a network connection for attendance-taking.
                        </p>
                        </div>
                    </div>
                </div>    
                <div class="col-md-3 d-md-flex align-items-stretch py-3">
                    <div class="card bg-success bg-opacity-10 text-white border border-success">
                        <div class="card-body text-center">
                        <BIconBatteryFull class="text-warning h1" />
                        <h3 class="card-title text-capitalize">Excellent battery backup</h3>
                        <p class="card-text">
                            The attendance-logging devices have excellent battery backup. Battery life of up to 24 hours.
                        </p>
                        </div>
                    </div>
                </div>            
            </div>
        </div>
        <div class="row bg-white text-dark d-flex justify-content-center my-5">
            <div class="bg-success bg-opacity-10 p-3">
                <div class="text-center h4">Project Partners</div>
                <div class="row d-flex justify-content-start">
                    <div class="col-md-4 col-xs-12 d-flex justify-content-center align-items-stretch py-3">
                        <div class="card border-0" style="background-color:inherit;">
                            <div class="card-body text-center">
                                <img class="img-fluid" style="max-height: 100px;" src="../assets/tetfund-logo.png" alt="">
                                <p class="card-text fst-italic">The Tertiary Education Trust Fund</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md col-xs-12 d-flex align-items-stretch py-3 justify-content-center">
                        <div class="card border-0" style="background-color:inherit;">
                            <div class="card-body text-center">
                                <img class="img-fluid" style="max-height: 100px;" src="../assets/unn-logo.png" alt="">
                                <p class="card-text fst-italic">University of Nigeria</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 col-xs-12 d-flex align-items-stretch py-3 justify-content-center">
                        <div class="card border-0" style="background-color:inherit;">
                            <div class="card-body text-center">
                                <img class="img-fluid" style="max-height: 100px;" src="../assets/lgt-logo.png" alt="">
                                <p class="card-text fst-italic">Lion Gadgets and Technologies</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container footer-bottom clearfix p-5 mt-5">
            <div class="copyright text-center">
                &copy; Copyright <strong><span>TAMS</span></strong>. All Rights Reserved
            </div>
        </div>
    </div>
</template>

<script>
import {
    BIconArrowRightSquare, 
    BIconUiChecks,
    BIconFileEarmarkBarGraphFill,
    BIconWifiOff,
    BIconBatteryFull
    } from 'bootstrap-icons-vue'
export default {
    components: {
        BIconArrowRightSquare,
        BIconUiChecks,
        BIconFileEarmarkBarGraphFill,
        BIconWifiOff,
        BIconBatteryFull
    },
    mounted() {
        document.title = this.$route.name + ' | TAMS'
    }
}
</script>
