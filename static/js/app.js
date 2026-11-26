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

// const confirmDelete = () => {
//     return confirm("Are you sure you want to delete this?");
// }


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



document.addEventListener('click', function (e) {
    var modal = document.getElementById('deleteModal');
    if (!modal) return;

    var delBtn = e.target.closest('.delete-comment-btn');
    if (delBtn) {
        document.getElementById('deleteForm').action = delBtn.dataset.deleteUrl;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.getElementById('deleteCancel').focus();
        return;
    }
    
    if (e.target.closest('#deleteCancel') || e.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('keydown', function (e) {
    var modal = document.getElementById('deleteModal');
    if (e.key === 'Escape' && modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});


const form = document.getElementById('commentForm');

if (form) {
    const box = document.getElementById('commentId');
    const err = document.getElementById('commentError');
    const count = document.getElementById('commentCount');
    const btn = document.getElementById('commentBtn');

    box.addEventListener('input', () => {
        count.textContent = box.value.length;
        if (box.value.trim()) err.classList.add('hidden');
    });

    form.addEventListener('submit', (e) => {
        if (!box.value.trim()) {
            e.preventDefault();
            err.classList.remove('hidden');
            box.focus();
            return;
        }
        btn.disabled = true;          
        btn.textContent = 'Posting...';
    });
}

document.addEventListener('click', function (e) {
    var editBtn = e.target.closest('.edit-comment-btn');
    var cancelBtn = e.target.closest('.cancel-edit-btn');

    if (editBtn) {
        var id = editBtn.dataset.id;
        document.getElementById('text-' + id).classList.add('hidden');
        document.getElementById('edit-' + id).classList.remove('hidden');
    }
    if (cancelBtn) {
        var cid = cancelBtn.dataset.id;
        document.getElementById('edit-' + cid).classList.add('hidden');
        document.getElementById('text-' + cid).classList.remove('hidden');
    }
});


document.addEventListener('click', function (e) {
    var replyBtn = e.target.closest('.reply-btn');
    var cancelReply = e.target.closest('.cancel-reply-btn');

    if (replyBtn) {
        var f = document.getElementById('reply-' + replyBtn.dataset.id);
        f.classList.toggle('hidden');

        if (!f.classList.contains('hidden')) {
            var ta = f.querySelector('textarea');
            ta.focus();
            ta.setSelectionRange(ta.value.length, ta.value.length);
        }
    }

    if (cancelReply) {
        document.getElementById('reply-' + cancelReply.dataset.id).classList.add('hidden');
    }
});




document.addEventListener('input', function (e) {
    if (e.target.id === 'commentId') {
        var counter = document.getElementById('commentCount');
        if (counter) counter.textContent = e.target.value.length;

        var err = document.getElementById('commentError');
        if (err && e.target.value.trim()) err.classList.add('hidden');
    }
});


document.addEventListener('submit', function (e) {
    if (e.target.id !== 'commentForm') return;

    var box = document.getElementById('commentId');
    var err = document.getElementById('commentError');

    if (!box.value.trim()) {
        e.preventDefault();
        if (err) err.classList.remove('hidden');
        box.focus();
        return;
    }

    var btn = document.getElementById('commentBtn');
    if (btn) {
        btn.disabled = true;
        btn.textContent = 'Posting...';
    }
});


document.addEventListener('click', function (e) {
    var modal = document.getElementById('deleteUserModal');
    if (!modal) return;

    var btn = e.target.closest('.delete-user-btn');
    if (btn) {
        document.getElementById('deleteUserForm').action = btn.dataset.deleteUrl;
        document.getElementById('deleteUserLabel').textContent = btn.dataset.deleteLabel;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.getElementById('deleteUserCancel').focus();
        return;
    }
    if (e.target.closest('#deleteUserCancel') || e.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('keydown', function (e) {
    var modal = document.getElementById('deleteUserModal');
    if (e.key === 'Escape' && modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});


document.addEventListener('submit', function (e) {
    if (e.target.id === 'deleteUserForm') {
        var b = document.getElementById('deleteUserSubmit');
        b.disabled = true;
        b.textContent = 'Deleting...';
    }
});




document.addEventListener('click', function (e) {
    var modal = document.getElementById('deleteCategoryModal');
    if (!modal) return;

    var btn = e.target.closest('.delete-category-btn');
    if (btn) {
        document.getElementById('deleteCategoryForm').action = btn.dataset.deleteUrl;
        document.getElementById('deleteCategoryLabel').textContent = btn.dataset.deleteLabel;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.getElementById('deleteCategoryCancel').focus();
        return;
    }
    if (e.target.closest('#deleteCategoryCancel') || e.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('keydown', function (e) {
    var modal = document.getElementById('deleteCategoryModal');
    if (e.key === 'Escape' && modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('submit', function (e) {
    if (e.target.id === 'deleteCategoryForm') {
        var b = document.getElementById('deleteCategorySubmit');
        b.disabled = true;
        b.textContent = 'Deleting...';
    }
});



document.addEventListener('click', function (e) {
    var modal = document.getElementById('deletePostModal');
    if (!modal) return;

    var btn = e.target.closest('.delete-post-btn');
    if (btn) {
        document.getElementById('deletePostForm').action = btn.dataset.deleteUrl;
        document.getElementById('deletePostLabel').textContent = btn.dataset.deleteLabel;
        modal.classList.remove('hidden');
        modal.classList.add('flex');
        document.getElementById('deletePostCancel').focus();
        return;
    }
    if (e.target.closest('#deletePostCancel') || e.target === modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('keydown', function (e) {
    var modal = document.getElementById('deletePostModal');
    if (e.key === 'Escape' && modal) {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
});

document.addEventListener('submit', function (e) {
    if (e.target.id === 'deletePostForm') {
        var b = document.getElementById('deletePostSubmit');
        b.disabled = true;
        b.textContent = 'Deleting...';
    }
});




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
});


if (document.getElementById('quill-editor')) {
    var quill = new Quill('#quill-editor', {
        theme: 'snow',
        modules: {
            toolbar: [
                [{ 'header': [1, 2, 3, false] }],
                ['bold', 'italic', 'underline', 'strike'],
                [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                ['link', 'image'],
                [{ 'align': [] }],
                ['blockquote', 'code-block'],
                ['clean']
            ]
        }
    });

    var existingContent = document.getElementById('blog_body').value;
    if (existingContent) {
        quill.root.innerHTML = existingContent;
    }

    document.querySelector('form').addEventListener('submit', function() {
        document.getElementById('blog_body').value = quill.root.innerHTML;
    });
}


const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTop.classList.remove('opacity-0', 'invisible');
        backToTop.classList.add('opacity-100', 'visible');
    } else {
        backToTop.classList.remove('opacity-100', 'visible');
        backToTop.classList.add('opacity-0', 'invisible');
    }
});

backToTop.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
