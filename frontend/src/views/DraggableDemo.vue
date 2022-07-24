<template>
<div class="flex m-10">
    <p class="lead">Match the following protocols to the category they belong to</p>
    <div class="row">
        <div class="col">
            <div class="p-3 m-1 text-e">OSPF</div>
            <div class="p-3 m-1 text-e">EIGRP</div>
            <div class="p-3 m-1 text-e">BGP</div>
        </div>
        <div class="col">
            <draggable class="dragArea list-group w-full" v-model="myList" :list="list" @change="log">
            <div class="list-group-item bg-gray-300 m-1 p-3 rounded-md text-center"
                v-for="element in list"
                :key="element.name"
            >
                {{ element.name }}
            </div>
            </draggable>
        </div>
    </div>
</div>
</template>

<script>
import { defineComponent } from "vue"
import { VueDraggableNext } from "vue-draggable-next"
export default defineComponent({
    components: {
        draggable: VueDraggableNext
    },
    data() {
        return {
            enabled: true,
            list: [
                {name: "Link State", id: 1},
                {name: "Path Vector", id: 2},
                {name: "Distance Vector", id:3},
            ],
            list2: [
                {name: "OSPF", id: 1},
                {name: "EIGRP", id: 2},
                {name: "BGP", id:3},
            ],
            dragging: false,
        }
    },
    methods: {
        log(event) {
            console.log(event)
            console.log(this.list)
        }
    },
    computed: {
        myList: {
            get() {
                return this.$store.state.elements
            },
            set(value) {
                this.$store.dispatch('updateElements', value)
            }
        }
    }
})
</script>
<style scoped>
.draggable-list {
    background: #3f51b5;
    color: #fff;
    border: 1px solid;
    height: 50vh;
}
.list-item {
    margin: 10px;
    padding: 40px;
    cursor: pointer;
    font-size: 18px;
    border-radius: 5px;
    background: #f44336;
    display: inline-block;
}
</style>