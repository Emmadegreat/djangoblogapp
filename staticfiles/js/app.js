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
        event.preventDefault(); // Prevent the default form submission behavior

            const formData = new FormData(form); // Collect form data
            const url = form.getAttribute('data-url'); // Get the URL from the form's data attribute
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

                // Display success or error messages dynamically
                if (response.ok) {
                    messageContainer.innerHTML = `<p style="color: green;">${data.message}</p>`;
                } else {
                    messageContainer.innerHTML = `<p style="color: red;">${data.error}</p>`;
                }

                // Clear form input on success
                if (data.success) {
                    form.reset();
                }
            } catch (error) {
                messageContainer.innerHTML = `<p style="color: red;">An error occurred. Please try again.</p>`;
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