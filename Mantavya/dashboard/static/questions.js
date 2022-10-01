// Chart - 1
const ctx = document.getElementById('myChart').getContext('2d');
// Chart - 2
const ctx1 = document.getElementById('myChart1').getContext('2d');


const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Excellent', 'Good', 'Ok'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3],
            backgroundColor: [
                'rgb(22, 191, 214)',
                'rgb(247, 101, 163)',
                'rgb(161, 85, 185)'
            ],
            borderWidth: 1,
            borderColor: 'rgb(40, 44, 52)',
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        aspectRatio: 1,
        layout: {
            padding: 5
        },
    },
    plugins:{
        legend: {
            align: 'starts',
            position: 'right',  
        },
    },
});
myChart.options.plugins.legend.position = 'right';
myChart.update();

const myChart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: ['Excellent', 'Good', 'Ok'],
        datasets: [{
            label: '# of Votes',
            data: [12, 19, 3],
            backgroundColor: [
                'rgb(22, 191, 214)',
                'rgb(247, 101, 163)',
                'rgb(161, 85, 185)'
            ],
            borderWidth: 1,
            borderColor: 'rgb(40, 44, 52)',
        }]
    },
    options: {
        responsive: false,
        maintainAspectRatio: false,
        aspectRatio: 1,
        layout: {
            padding: 5
        }
    },
});