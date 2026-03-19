// Toggle habit completion
document.addEventListener('DOMContentLoaded', function() {
    // Handle habit toggles
    document.querySelectorAll('.habit-toggle input').forEach(toggle => {
        toggle.addEventListener('change', function() {
            const habitId = this.dataset.habitId;
            const completed = this.checked;

            fetch('/toggle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `habit_id=${habitId}&completed=${completed}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update streak display
                    const streakElement = document.querySelector(`.habit-streak[data-habit-id="${habitId}"]`);
                    if (streakElement) {
                        streakElement.textContent = `${data.streak} day${data.streak !== 1 ? 's' : ''}`;
                    }

                    // Visual feedback
                    const habitItem = this.closest('.habit-item');
                    habitItem.classList.add('fade-in');
                    setTimeout(() => {
                        habitItem.classList.remove('fade-in');
                    }, 300);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert toggle on error
                this.checked = !completed;
            });
        });
    });

    // Color picker for new habits
    const colorInput = document.getElementById('color');
    if (colorInput) {
        const colorPreview = document.createElement('div');
        colorPreview.style.cssText = `
            width: 30px;
            height: 30px;
            border-radius: 4px;
            margin-left: 10px;
            border: 2px solid #ddd;
        `;
        colorInput.parentNode.insertBefore(colorPreview, colorInput.nextSibling);

        colorInput.addEventListener('input', function() {
            colorPreview.style.backgroundColor = this.value;
        });

        // Set initial color
        colorPreview.style.backgroundColor = colorInput.value;
    }

    // Chart for dashboard
    const completionChart = document.getElementById('completionChart');
    if (completionChart) {
        const ctx = completionChart.getContext('2d');
        const data = JSON.parse(completionChart.dataset.values);
        const dates = Object.keys(data);
        const values = Object.values(data);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates.map(date => new Date(date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                })),
                datasets: [{
                    label: 'Completion Rate (%)',
                    data: values,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + '% completed';
                            }
                        }
                    }
                }
            }
        });
    }

    // Delete habit confirmation
    document.querySelectorAll('.delete-habit').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this habit? All completion data will be lost.')) {
                e.preventDefault();
            }
        });
    });

    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 0.875rem;
                z-index: 1000;
                white-space: nowrap;
            `;

            const rect = this.getBoundingClientRect();
            tooltip.style.top = (rect.top - 40) + 'px';
            tooltip.style.left = (rect.left + rect.width / 2 - tooltip.offsetWidth / 2) + 'px';

            document.body.appendChild(tooltip);
            this.tooltipElement = tooltip;
        });

        element.addEventListener('mouseleave', function() {
            if (this.tooltipElement) {
                this.tooltipElement.remove();
            }
        });
    });
});
