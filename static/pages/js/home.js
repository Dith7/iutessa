// JavaScript pour la page d'accueil
document.addEventListener('DOMContentLoaded', function() {
    
    // Animation d'apparition au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observer tous les blocs de page
    const pageBlocks = document.querySelectorAll('.page-block');
    pageBlocks.forEach(block => {
        observer.observe(block);
    });

    // Smooth scroll pour les liens internes
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Offset pour la nav fixe
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Parallax effect pour les images de fond (optionnel)
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.bg-hero-pattern');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            const yPos = -(scrolled * speed);
            element.style.transform = `translateY(${yPos}px)`;
        });
    });

    // Lazy loading pour les images
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('opacity-0');
                img.classList.add('opacity-100');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Animation des statistiques (si présentes)
    const statsElements = document.querySelectorAll('[data-stat]');
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const finalValue = parseInt(element.dataset.stat);
                animateCounter(element, 0, finalValue, 2000);
                statsObserver.unobserve(element);
            }
        });
    });

    statsElements.forEach(el => statsObserver.observe(el));

    // Fonction d'animation des compteurs
    function animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const current = Math.floor(start + (end - start) * progress);
            
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        requestAnimationFrame(animate);
    }

    // Gestion du formulaire de contact (si présent)
    const contactForms = document.querySelectorAll('.contact-form');
    contactForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validation basique
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('border-red-500');
                } else {
                    field.classList.remove('border-red-500');
                }
            });
            
            if (isValid) {
                // Simulation d'envoi
                showNotification('Message envoyé avec succès !', 'success');
                form.reset();
            } else {
                showNotification('Veuillez remplir tous les champs requis.', 'error');
            }
        });
    });

    // Fonction de notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `
            fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transition-all duration-300
            ${type === 'success' ? 'bg-green-500 text-white' : 
              type === 'error' ? 'bg-red-500 text-white' : 
              'bg-blue-500 text-white'}
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animation d'apparition
        setTimeout(() => {
            notification.classList.add('translate-x-0');
        }, 100);
        
        // Suppression automatique
        setTimeout(() => {
            notification.classList.add('translate-x-full', 'opacity-0');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }

    // Gestion des boutons "Lire la suite" avec expansion
    const expandButtons = document.querySelectorAll('[data-expand]');
    expandButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.dataset.expand;
            const target = document.getElementById(targetId);
            
            if (target) {
                target.classList.toggle('hidden');
                this.textContent = target.classList.contains('hidden') ? 
                    'Lire la suite' : 'Réduire';
            }
        });
    });

    console.log('🎓 Page d\'accueil universitaire chargée avec Tailwind CSS');
});