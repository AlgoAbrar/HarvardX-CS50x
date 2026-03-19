document.addEventListener('DOMContentLoaded', function() {
    
    updateCurrentDate();
 
    initializeWelcomeButton();
    
    addScrollAnimations();
 
    initializeVisitorCounter();
   
    addInteractiveFeatures();

    adjustForMobile();
});

function updateCurrentDate() {
    const dateElements = document.querySelectorAll('[id$="Date"]');
    const now = new Date();
    const options = { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    };
    const formattedDate = now.toLocaleDateString('en-US', options);
    
    dateElements.forEach(element => {
        element.textContent = formattedDate;
    });
}

function initializeWelcomeButton() {
    const welcomeBtn = document.getElementById('welcomeBtn');
    if (welcomeBtn) {
        welcomeBtn.addEventListener('click', function() {
            Swal.fire({
                title: 'Welcome to Bangladesh!',
                html: `
                    <div class="text-start">
                        <p>Bangladesh offers:</p>
                        <ul>
                            <li>World's longest natural sea beach</li>
                            <li>Largest mangrove forest (Sundarbans)</li>
                            <li>Beautiful tea gardens</li>
                            <li>Picturesque hill tracts</li>
                            <li>Rich cultural heritage</li>
                        </ul>
                        <p>Start your journey by exploring our website!</p>
                    </div>
                `,
                icon: 'info',
                confirmButtonText: 'Start Exploring',
                background: '#f8f9fa',
                customClass: {
                    popup: 'animated fadeIn'
                }
            });
        });
    }
}

function initializeDivisionButtons() {
    const divisionBtn = document.getElementById('divisionBtn');
    if (divisionBtn) {
        divisionBtn.addEventListener('click', function() {
            const divisionsGrid = document.getElementById('divisionsGrid');
            if (divisionsGrid) {
                divisionsGrid.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
                
                divisionsGrid.classList.add('shadow-strong');
                setTimeout(() => {
                    divisionsGrid.classList.remove('shadow-strong');
                }, 2000);
            }
        });
    }
    
    const divisionCards = document.querySelectorAll('.division-card');
    divisionCards.forEach(card => {
        card.addEventListener('click', function() {
            divisionCards.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

function addScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.card, section').forEach(el => {
        observer.observe(el);
    });
}

function initializeVisitorCounter() {
    const counterElement = document.getElementById('visitorCount');
    if (counterElement) {
        let count = localStorage.getItem('bdTourismVisitors') || 1000;
        
        counterElement.textContent = parseInt(count).toLocaleString();
        
        setInterval(() => {
            count++;
            localStorage.setItem('bdTourismVisitors', count);
            counterElement.textContent = parseInt(count).toLocaleString();
            
            counterElement.classList.add('text-pulse');
            setTimeout(() => {
                counterElement.classList.remove('text-pulse');
            }, 500);
        }, 30000);
    }
}

function addInteractiveFeatures() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.classList.add('loaded');
        });

        img.addEventListener('click', function() {
            if (this.classList.contains('enlarged')) {
                this.classList.remove('enlarged');
                this.style.transform = 'scale(1)';
            } else {
                this.classList.add('enlarged');
                this.style.transform = 'scale(1.5)';
            }
        });
    });

    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
}

function adjustForMobile() {
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    
    if (isMobile) {
        document.documentElement.style.setProperty('--animation-speed', '0.5s');
        
        const cards = document.querySelectorAll('.card');
        cards.forEach(card => {
            card.style.transition = 'none';
        });
    }
    
    window.addEventListener('orientationchange', function() {
        setTimeout(() => {
            window.scrollTo(0, 0);
        }, 100);
    });
}

function showAlert(title, message, type = 'info') {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: title,
            text: message,
            icon: type,
            confirmButtonText: 'OK'
        });
    } else {
        alert(`${title}\n\n${message}`);
    }
}

const style = document.createElement('style');
style.textContent = `
    @keyframes textPulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .text-pulse {
        animation: textPulse 0.5s ease;
        color: #F42A41 !important;
    }
    
    img.loaded {
        opacity: 1;
        transition: opacity 0.3s ease;
    }
    
    img:not(.loaded) {
        opacity: 0;
    }
    
    img.enlarged {
        z-index: 1000;
        position: relative;
        cursor: zoom-out;
    }
    
    .is-invalid {
        border-color: #F42A41 !important;
    }
    
    .fade-in {
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .active {
        border: 3px solid #FFC107 !important;
        box-shadow: 0 0 20px rgba(255, 193, 7, 0.3) !important;
    }
`;
document.head.appendChild(style);

if (typeof Swal === 'undefined') {
    const swalScript = document.createElement('script');
    swalScript.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
    document.head.appendChild(swalScript);
}

if (window.location.pathname.includes('divisions.html')) {
    initializeDivisionButtons();
}

document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        window.location.href = 'index.html';
    }
    
    if (e.key === 'Escape') {
        const enlargedImages = document.querySelectorAll('img.enlarged');
        enlargedImages.forEach(img => {
            img.classList.remove('enlarged');
            img.style.transform = 'scale(1)';
        });
    }
});