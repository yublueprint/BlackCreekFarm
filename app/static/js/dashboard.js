// Initialize chart when the DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('yieldChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Crop Yield (tons)',
                data: [12, 19, 15, 17, 21, 25],
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
            }, {
                label: 'Milk Production (gallons)',
                data: [18, 15, 20, 22, 24, 23],
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});