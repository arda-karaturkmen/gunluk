// Main JavaScript for Social Diary

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('div');
        counter.className = 'text-muted small text-end mt-1';
        counter.innerHTML = `<span class="current">0</span>/${maxLength}`;
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            const current = this.value.length;
            const currentSpan = counter.querySelector('.current');
            currentSpan.textContent = current;
            
            if (current > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
            
            if (current >= maxLength) {
                counter.classList.add('text-danger');
                counter.classList.remove('text-warning');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    });
});

// Photo preview functionality
function previewImages(input) {
    const preview = document.getElementById('photoPreview');
    if (!preview) return;
    
    preview.innerHTML = '';
    
    if (input.files.length > 3) {
        showAlert('En fazla 3 fotoğraf seçebilirsiniz.', 'warning');
        input.value = '';
        return;
    }
    
    Array.from(input.files).forEach((file, index) => {
        if (!file.type.startsWith('image/')) {
            showAlert('Sadece resim dosyaları yükleyebilirsiniz.', 'warning');
            return;
        }
        
        const reader = new FileReader();
        reader.onload = function(e) {
            const div = document.createElement('div');
            div.className = 'position-relative d-inline-block me-2 mb-2';
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview" 
                     class="img-thumbnail" style="width: 120px; height: 120px; object-fit: cover;">
                <button type="button" class="btn btn-sm btn-danger position-absolute top-0 end-0" 
                        onclick="removePreview(this, ${index})" style="transform: translate(50%, -50%);">
                    <i class="fas fa-times"></i>
                </button>
            `;
            preview.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}

function removePreview(button, index) {
    const input = document.getElementById('photos');
    if (!input) return;
    
    const dt = new DataTransfer();
    
    Array.from(input.files).forEach((file, i) => {
        if (i !== index) {
            dt.items.add(file);
        }
    });
    
    input.files = dt.files;
    button.parentElement.remove();
}

// Follow/Unfollow functionality
function toggleFollow(username) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfToken) {
        showAlert('CSRF token bulunamadı.', 'danger');
        return;
    }

    fetch(`/follow/${username}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken.value,
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const btn = document.getElementById('followBtn');
        if (!btn) return;
        
        const icon = btn.querySelector('i');
        const span = btn.querySelector('span');
        
        if (data.is_following) {
            icon.className = 'fas fa-user-minus me-2';
            span.textContent = 'Takibi Bırak';
            btn.setAttribute('data-following', 'true');
            btn.classList.remove('btn-primary');
            btn.classList.add('btn-outline-danger');
        } else {
            icon.className = 'fas fa-user-plus me-2';
            span.textContent = 'Takip Et';
            btn.setAttribute('data-following', 'false');
            btn.classList.remove('btn-outline-danger');
            btn.classList.add('btn-primary');
        }
        
        // Update follower count if element exists
        const followerCount = document.querySelector('.follower-count');
        if (followerCount) {
            const current = parseInt(followerCount.textContent);
            followerCount.textContent = data.is_following ? current + 1 : current - 1;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Bir hata oluştu. Lütfen tekrar deneyin.', 'danger');
    });
}

// Show alert function
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertContainer, container.firstChild);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertContainer);
            bsAlert.close();
        }, 5000);
    }
}

// Infinite scroll for feed
let loading = false;
let currentPage = 1;

function loadMoreEntries() {
    if (loading) return;
    
    loading = true;
    const loadingIndicator = document.getElementById('loadingIndicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'block';
    }
    
    fetch(`?page=${currentPage + 1}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newEntries = doc.querySelectorAll('.diary-card');
        
        if (newEntries.length > 0) {
            const entriesContainer = document.querySelector('.entries-container');
            if (entriesContainer) {
                newEntries.forEach(entry => {
                    entriesContainer.appendChild(entry);
                });
                currentPage++;
            }
        }
        
        loading = false;
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error loading more entries:', error);
        loading = false;
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    });
}

// Check if user is near bottom of page for infinite scroll
window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 1000) {
        loadMoreEntries();
    }
});

// Form validation
function validateDiaryForm() {
    const content = document.querySelector('textarea[name="content"]');
    const photos = document.querySelector('input[name="photos"]');
    
    if (!content || content.value.trim().length === 0) {
        showAlert('Günlük içeriği boş olamaz.', 'warning');
        return false;
    }
    
    if (photos && photos.files.length > 3) {
        showAlert('En fazla 3 fotoğraf yükleyebilirsiniz.', 'warning');
        return false;
    }
    
    return true;
}

// Add form validation to diary form
document.addEventListener('DOMContentLoaded', function() {
    const diaryForm = document.getElementById('diaryForm');
    if (diaryForm) {
        diaryForm.addEventListener('submit', function(e) {
            if (!validateDiaryForm()) {
                e.preventDefault();
            }
        });
    }
});
