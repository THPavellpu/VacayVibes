 // Mobile Menu Toggle
        function toggleMenu() {
            const navLinks = document.getElementById('navLinks');
            navLinks.classList.toggle('active');
        }

        // Book Now Function - fallback: redirect to booking page
        function bookNow(packageName, packageId) {
            if (packageId) {
                window.location = `/book/?package_id=${packageId}`;
            } else {
                alert(`Thank you for your interest in "${packageName}"!\n\nOur team will contact you shortly.`);
            }
        }

        // Newsletter Subscribe (deprecated - form posts to server)
        function subscribeNewsletter(event) {
            event.preventDefault();
            const email = event.target.querySelector('input').value;
            alert(`Thank you for subscribing! 🎉\n\nWe'll send travel deals and updates to:\n${email}`);
            event.target.reset();
        }

        // Open WhatsApp to message admin with a prefilled booking message
        function openWhatsApp(el) {
            const number = el.getAttribute('data-number') || '';
            // Find the closest form (booking form) to read values
            const form = el.closest('form');
            let name = '';
            let email = '';
            let phone = '';
            let message = '';
            let packageTitle = '';
            if (form) {
                const nameEl = form.querySelector('#id_name');
                const emailEl = form.querySelector('#id_email');
                const phoneEl = form.querySelector('#id_phone');
                const messageEl = form.querySelector('#id_message');
                if (nameEl) name = nameEl.value || '';
                if (emailEl) email = emailEl.value || '';
                if (phoneEl) phone = phoneEl.value || '';
                if (messageEl) message = messageEl.value || '';
            }
            // Try to read package title from summary on the page
            const summaryTitle = document.querySelector('.summary-title');
            if (summaryTitle) packageTitle = summaryTitle.textContent.trim();

            let text = `Hello,%0AI'd like to inquire about a booking.`;
            if (packageTitle) text += `%0APackage: ${encodeURIComponent(packageTitle)}`;
            if (name) text += `%0AName: ${encodeURIComponent(name)}`;
            if (email) text += `%0AEmail: ${encodeURIComponent(email)}`;
            if (phone) text += `%0APhone: ${encodeURIComponent(phone)}`;
            if (message) text += `%0AMessage: ${encodeURIComponent(message)}`;

            // Normalize number: remove non-digits and leading +
            const normalized = (number || '').replace(/[^\d]/g, '');
            if (!normalized) {
                alert('WhatsApp number is not configured.');
                return;
            }

            const url = `https://wa.me/${normalized}?text=${text}`;
            window.open(url, '_blank', 'noopener');
        }

        // Smooth Scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                    // Close mobile menu if open
                    document.getElementById('navLinks').classList.remove('active');
                }
            });
        });

        // Lazy Loading Enhancement
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.src;
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[loading="lazy"]').forEach(img => {
                imageObserver.observe(img);
            });
        }

        // Hide header on scroll down, show on scroll up (performant)
        (function () {
            const header = document.querySelector('header');
            const mobileNav = document.getElementById('navLinks');
            if (!header) return;

            let lastScroll = window.pageYOffset || document.documentElement.scrollTop;
            let ticking = false;
            const delta = 5; // minimal scroll to trigger (reduced sensitivity)
            const hideAfter = 10; // don't hide when near the very top (lowered from 100)

            function onScroll() {
                const current = window.pageYOffset || document.documentElement.scrollTop;

                if (mobileNav && mobileNav.classList.contains('active')) {
                    // keep header visible while mobile menu is open
                    header.classList.remove('nav-hidden');
                    lastScroll = current;
                    return;
                }

                if (Math.abs(current - lastScroll) <= delta) return;

                if (current > lastScroll && current > hideAfter) {
                    // scrolling down
                    header.classList.add('nav-hidden');
                } else {
                    // scrolling up
                    header.classList.remove('nav-hidden');
                }

                lastScroll = current;
            }

            window.addEventListener('scroll', function () {
                if (!ticking) {
                    window.requestAnimationFrame(function () {
                        onScroll();
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        })();