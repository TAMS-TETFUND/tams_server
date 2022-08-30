<template>
    <ContentLayout>
        <div class="text-center">
            <h1 class="mb-5">Product Details</h1>
        </div>
        <div>
            <p>The Time and Attendance Management system (TAMS) is a
                multi-modal biometric attendance system designed primarily for use in
                tertiary institutions in Nigeria. The project is backed by the Tertiary
                Education Fund (TETFUND) of Nigeia.</p>
            <h3 class="text-warning">Attendance Logging</h3>
            The system supports two modes of biometric verification: 
            <div class="row">
                <div class="d-md-flex justify-content-center">
                    <div class="col-md-3 card bg-success bg-opacity-10 text-center m-2">
                        <div class="card-title h4">Face Verification</div>
                        <div class="card-body card-image">
                            <BIconPersonBoundingBox />
                        </div>
                    </div>
                    <div class="col-md-3 card bg-success bg-opacity-10 text-center m-2">
                        <div class="card-title h4">Fingerprint Verification</div>
                        <div class="card-body card-image">
                            <BIconFingerprint />
                        </div>
                    </div>
                </div>
            </div>
            <h3 class="text-warning">System Design</h3>
            <div>TAMS is an end-to-end solution to the problem of attedance management, especially 
                for events with high number of students. The system comprises of two major modules:
                <div class="row">
                    <div class="d-md-flex justify-content-center bg-success bg-opacity-10">
                        <div class="m-2 border-end text-center">
                            <div class="h2"><BIconServer /><span class="ms-2">TAMS Server</span></div>
                        </div>
                        <div class="m-2">
                            <div class="h2 "><BIconMotherboard /><span class="ms-2">TAMS Node Device</span></div>
                        </div>
                    </div>
                </div>
                the server module and the node device (the devices that are used for the actual attedance-logging).
                Communication between the server and the node device can be via a Wireless Local Area Network (WLAN/WiFi)
                or via a low-power wireless LoRa mesh network (for our Raspberry PI-based node devices only).
                
                The system can be adopted in numerous ways:
                <ul>
                    <li>Deploying our Raspberry PI-based node devices equipped with the TAMS software and biometric capture devices (fingerprint scanner and camera) for attendance-logging</li>
                    <li>Deploying the TAMS software on a regular PC and procuring our biometric capture device (Fingerprint scanner)</li>
                </ul>
            </div>
        </div>
    </ContentLayout>
</template>

<script>
import ContentLayout from '../components/ContentLayout.vue'
import { 
    BIconPersonBoundingBox, 
    BIconFingerprint,
    BIconMotherboard,
    BIconServer 
    } from 'bootstrap-icons-vue';
export default{
    name: "ProductDetail",
    components: { 
        ContentLayout, 
        BIconPersonBoundingBox, 
        BIconFingerprint,
        BIconServer,
        BIconMotherboard 
    }
}
</script>

<style scoped>
.card-image {
    font-size: 120px;
    color: #eeeeee;
}
</style>