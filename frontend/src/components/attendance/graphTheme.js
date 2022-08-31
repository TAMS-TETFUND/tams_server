var colorPalette = [
        "#ffc107",
        "#ff4249",
        "#38a6ff",
        "#3ab027",
        "#f49e89",
        "#72ccff",
        "#f7c5a0",
        "#d4a4eb",
        "#d2f5a6"
    ];

var customTheme = {
    color: colorPalette,

    backgroundColor: '#212529',
    title: {

        textStyle: {
            color: '#fff',
            fontWeight: 'normal'

        }
    },

    visualMap: {
        color: ['#1790cf', '#a2d4e6']
    },

    toolbox: {
        iconStyle: {
            normal: {
                borderColor: '#ffc107'
            }
        }
    },

    tooltip: {
        backgroundColor: 'rgba(0,0,0,1)'
    },

    dataZoom: {
        dataBackgroundColor: '#fff294',
        fillerColor: 'rgba(154,217,247,0.2)',
        handleColor: '#ddfd00'
    },

    timeline: {
        lineStyle: {
            color: '#005eaa'
        },
        controlStyle: {
            color: '#005eaa',
            borderColor: '#005eaa'
        }
    },

    candlestick: {
        itemStyle: {
            color: '#c12e34',
            color0: '#2b821d'
        },
        lineStyle: {
            width: 1,
            color: '#c12e34',
            color0: '#2b821d'
        },
        areaStyle: {
            color: '#e6b600',
            color0: '#005eaa'
        }
    },

    graph: {
        itemStyle: {
            color: '#e6b600'
        },
        linkStyle: {
            color: '#005eaa'
        }
    },

    map: {
        itemStyle: {
            color: '#f2385a',
            borderColor: '#eee',
            areaColor: '#ddd'
        },
        areaStyle: {
            color: '#ddd'
        },
        label: {
            color: '#c12e34'
        }
    },

    gauge: {
        axisLine: {
            show: true,
            lineStyle: {
                color: [
                    [0.2, '#ff4249'],
                    // [0.8, '#38a6ff'],
                    [1, '#3ab027']
                ],
                width: 5
            }
        },
        axisTick: {
            splitNumber: 10,
            length: 8,
            lineStyle: {
                color: 'auto'
            }
        },
        axisLabel: {
            color: 'auto'
        },
        splitLine: {
            length: 12,
            lineStyle: {
                color: 'auto'
            }
        },
        pointer: {
            length: '90%',
            width: 3,
            color: 'auto'
        },
        title: {
            color: '#fff'
        },
        detail: {
            color: 'auto'
        }
    }
};

export { customTheme };