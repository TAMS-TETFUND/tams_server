<template>
    <v-chart class="chart" :option="option" />
</template>

<script>
import {use, registerTheme } from "echarts/core"
import { customTheme } from './graphTheme.js'
import {CanvasRenderer } from "echarts/renderers"
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, TitleComponent } from 'echarts/components'
import VChart, { THEME_KEY } from 'vue-echarts'
// import { provide } from "@vue/runtime-core"
import { ref, defineComponent, toRef } from "vue"

registerTheme('customGraphTheme', customTheme)

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, TitleComponent])

export default defineComponent({
    name: "AttendanceGraph",
    components: { VChart },
    provide: {[THEME_KEY]: "customGraphTheme"},
    props: { x_axis: Array, y_axis: Array},
    setup: (props) => {
        const option = ref({
            title: {
                text: "Attendance Logged",
                left: "center"
            },
            tooltip: {
                trigger: "item",
                formatter: "{b} : {c} students)"
            },
            xAxis: {
                type: 'category',
                data: toRef(props, 'x_axis')
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: toRef(props, 'y_axis'),
                    type: 'bar'
                }
            ]
        })
        return { option }
    }
})
</script>