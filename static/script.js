document.addEventListener('DOMContentLoaded', function() {
    const summaryForm = document.querySelector('form[action^="/generate_summary/"]');
    const detailedAttributesForm = document.querySelector('form[action^="/generate_detailed_attributes/"]');
    const addProductsForm = document.getElementById('addProductsForm');

    function handleFormSubmit(form, successUrl, processingText) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.classList.add('btn-generating');

            let seconds = 0;
            const updateButtonText = () => {
                seconds++;
                submitButton.textContent = `🔄 ${processingText}... ${seconds} 🔄`;
            };

            const timer = setInterval(updateButtonText, 1000);

            fetch(this.action, {
                method: 'POST',
                body: new FormData(this),
            })
            .then(response => {
                clearInterval(timer);
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json();
                }
            })
            .then(data => {
                if (data && !data.success) {
                    alert('Error: ' + data.error);
                    resetButton(submitButton);
                }
            })
            .catch(error => {
                clearInterval(timer);
                console.error('Error:', error);
                alert('An error occurred while processing.');
                resetButton(submitButton);
            });
        });
    }

    function resetButton(button) {
        button.textContent = button.dataset.originalText;
        button.disabled = false;
        button.classList.remove('btn-generating');
    }

    if (summaryForm) {
        const summaryButton = summaryForm.querySelector('button[type="submit"]');
        summaryButton.dataset.originalText = summaryButton.textContent;
        handleFormSubmit(summaryForm, '/product/', 'Generating');
    }

    if (detailedAttributesForm) {
        const detailedAttributesButton = detailedAttributesForm.querySelector('button[type="submit"]');
        detailedAttributesButton.dataset.originalText = detailedAttributesButton.textContent;
        handleFormSubmit(detailedAttributesForm, '/product/', 'Generating');
    }

    if (addProductsForm) {
        const addProductsButton = addProductsForm.querySelector('button[type="submit"]');
        addProductsButton.dataset.originalText = addProductsButton.textContent;
        handleFormSubmit(addProductsForm, '/products', 'Processing');
    }
});