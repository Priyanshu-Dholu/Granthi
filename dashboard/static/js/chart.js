function addCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const backgroundColor = ['rgba(255, 99, 132, 0.2)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 205, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(153, 102, 255, 0.2)'];

const borderColor = ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(153, 102, 255)'];

const type = 'doughnut';
const borderWidth = 1;
const hoverOffset = 2;

const options = {
    responsive: true,
    maintainAspectRatio: false,
    aspectRatio: 1,
    plugins: {
        legend: {
            position: 'right',
            display: true,
        },
    },
}

const datasets = [
    [{ backgroundColor: backgroundColor, borderColor: borderColor, borderWidth: borderWidth, hoverOffset: hoverOffset }],
    [{ backgroundColor: backgroundColor, borderColor: borderColor, borderWidth: borderWidth, hoverOffset: hoverOffset }],
    [{ backgroundColor: backgroundColor, borderColor: borderColor, borderWidth: borderWidth, hoverOffset: hoverOffset }],
    [{ backgroundColor: backgroundColor, borderColor: borderColor, borderWidth: borderWidth, hoverOffset: hoverOffset }],
]

const config_q1 = {
    type: 'doughnut',
    data: {
        datasets: datasets[0],
        labels: ['Through a person known to a police officer', 'With a neighbour/ local leader', 'On your own'],
    },
    options: options,
}

const config_q2 = {
    type: 'doughnut',
    data: {
        datasets: datasets[1],
        labels: ['More than 15 minutes', '15 minutes', '10 minutes', '5 minutes', 'Immediately'],
    },
    options: options,
}

const config_q3 = {
    type: 'doughnut',
    data: {
        datasets: datasets[2],
        labels: ['Worst', 'Bad', 'Good', 'V.Good', 'Excellent'],
    },
    options: options,
}

const q1 = new Chart('q1d', config_q1);
const q2 = new Chart('q2d', config_q2);
const q3 = new Chart('q3d', config_q3);

function chartUpdate() {
    q1.update();
    q2.update();
    q3.update();
}
