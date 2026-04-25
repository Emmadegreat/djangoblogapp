let hideLoader = false;

function mapPreloader() {
    if (hideLoader) return;

    const loader = document.getElementById("preloader");
    if (loader) {
        loader.style.opacity = '0';
        loader.style.pointerEvents = 'none';

        setTimeout(() => {
            loader.style.display = 'none';
        }, 500);

        hideLoader = true;
    }
}


document.getElementById("date").innerHTML = new Date().getFullYear();


function closeMessage(id) {
    const message = document.getElementById(id);
    if (message) {
        message.style.transition = "opacity 0.3s ease";
        message.style.opacity = "0";
        setTimeout(() => message.remove(), 300);
    }
}

const confirmDelete = () => {
    return confirm("Are you sure you want to delete this?");
}


document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('subscription-form');
    const messageContainer = document.getElementById('subscription-message');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

            const formData = new FormData(form);
            const url = form.getAttribute('data-url'); 
            const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    body: formData,
                });

                const data = await response.json();

                if (response.ok) {

                    messageContainer.innerHTML = `<p style="color: green;">${data.message}</p>`;
                } else {
                    
                    messageContainer.innerHTML = `<p style="color: red;">${data.error}</p>`;
                }

                setTimeout(() => {
                    messageContainer.innerHTML = '';
                    
                }, 3000);
        
                if (data.success) {
                    form.reset();
                }
            } catch (error) {
                messageContainer.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;

                setTimeout(() => {
                    messageContainer.innerHTML = '';
                    form.reset();
                }, 3000);
                
                console.error('Error:', error);
            }
        });
    });




function validateComment() {
    let comment = document.getElementById("commentId").value.trim();
    if (!comment) {
        alert("Please you must write a comment before submitting.");
        return false;
    }
    return true;
}

const hamburger = document.getElementById('hamburger');
    const mobileView = document.getElementById('mobile-view');
    const overlay = document.getElementById('overlay');

    hamburger.addEventListener('click', () => {
        
        mobileView.classList.toggle('-translate-x-full');
        mobileView.classList.toggle('translate-x-0');
        overlay.classList.toggle('hidden');
    });

    
    overlay.addEventListener('click', () => {
        mobileView.classList.add('-translate-x-full');
        mobileView.classList.remove('translate-x-0');
        overlay.classList.add('hidden');
    });

window.addEventListener('load', function(){
    setTimeout(mapPreloader, 1500);
})