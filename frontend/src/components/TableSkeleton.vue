<template>
    <table class="table table-dark table-striped text-light">
        <thead>
            <tr class="placeholder-glow">
                <th scope="col" v-for="col in parseInt(cols)" :key="col"><span class="placeholder col-8"></span></th>
            </tr>
        </thead>
        <tbody>
            <tr class="placeholder-glow" v-for="row in parseInt(rows)" v-bind:key="row">
                <td v-for="col in parseInt(cols)" :key="col"><span class="placeholder col-8"></span></td>
            </tr>
        </tbody>
    </table>
</template>

<script>
    export default {
        props: ["cols", "rows"]
    }
</script>