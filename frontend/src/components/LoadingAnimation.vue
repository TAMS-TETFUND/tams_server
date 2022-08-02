<template>
    <div class="spinner-grow text-success" role="status" v-if="visible">
        <span class="visually-hidden">Loading...</span>
    </div>
</template>

<script>
export default {
    props: ["visible"]
}
</script>