// Tab Switching Logic
const navLinks = document.querySelectorAll('#sidebar-nav a');
const viewSections = document.querySelectorAll('.view-section');

navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Remove active class from all links
        navLinks.forEach(l => l.classList.remove('active'));
        // Add active class to clicked link
        link.classList.add('active');

        // Hide all views
        viewSections.forEach(view => {
            view.style.display = 'none';
            view.classList.remove('active');
        });

        // Show target view
        const targetId = link.getAttribute('data-target');
        const targetView = document.getElementById(targetId);
        if(targetView) {
            targetView.style.display = 'block';
            // slight delay to trigger CSS animation
            setTimeout(() => targetView.classList.add('active'), 10);
        }
    });
});

// Toast Notification System
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Prediction Form Submission
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get button and update state
    const btn = e.target.querySelector('button');
    const btnText = btn.querySelector('.btn-text');
    const spinner = document.getElementById('btn-spinner');
    
    btnText.style.display = 'none';
    spinner.style.display = 'block';
    btn.disabled = true;

    // Gather form data
    const payload = {
        Age: parseInt(document.getElementById('age').value),
        Gender: document.getElementById('gender').value,
        TenureMonths: parseInt(document.getElementById('tenure').value),
        ContractType: document.getElementById('contract').value,
        PaymentMethod: document.getElementById('payment').value,
        MonthlyCharges: parseFloat(document.getElementById('monthly').value),
        TotalCharges: parseFloat(document.getElementById('total').value),
        SupportCalls: parseInt(document.getElementById('support').value)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        
        // Update UI
        document.getElementById('placeholder-state').style.display = 'none';
        document.getElementById('results-content').style.display = 'block';

        // Update elements
        const riskText = document.getElementById('risk-text');
        const probText = document.getElementById('prob-text');
        const probBar = document.getElementById('prob-bar');
        const predText = document.getElementById('pred-text');
        const actionCard = document.getElementById('action-card');
        const actionText = document.getElementById('action-text');

        // Set Values
        riskText.innerText = data.risk_level;
        
        const probabilityPercent = (data.churn_probability * 100).toFixed(1);
        probText.innerText = probabilityPercent + '%';
        
        // Animate progress bar
        setTimeout(() => {
            probBar.style.width = probabilityPercent + '%';
        }, 100);

        predText.innerText = data.churn_prediction;

        // Reset classes
        riskText.className = '';
        actionCard.className = 'action-card';
        actionCard.querySelector('h4').className = '';
        probBar.style.backgroundColor = '';

        // Apply dynamic styling based on risk level
        if (data.risk_level === 'High') {
            riskText.classList.add('text-high');
            actionCard.classList.add('bg-high');
            actionCard.querySelector('h4').classList.add('text-high');
            probBar.style.backgroundColor = 'var(--danger)';
            actionText.innerText = "Assign customer success manager immediately. Schedule a check-in call and consider offering a retention discount.";
        } else if (data.risk_level === 'Medium') {
            riskText.classList.add('text-medium');
            actionCard.classList.add('bg-medium');
            actionCard.querySelector('h4').classList.add('text-medium');
            probBar.style.backgroundColor = 'var(--warning)';
            actionText.innerText = "Monitor account health. Send an automated check-in email to gather feedback on their experience.";
        } else {
            riskText.classList.add('text-low');
            actionCard.classList.add('bg-low');
            actionCard.querySelector('h4').classList.add('text-low');
            probBar.style.backgroundColor = 'var(--success)';
            actionText.innerText = "Account is healthy. Consider upselling premium features or asking for a referral/testimonial.";
        }

        showToast("Analysis Complete");

    } catch (error) {
        showToast("Error predicting churn: " + error.message);
        console.error(error);
    } finally {
        btnText.style.display = 'block';
        spinner.style.display = 'none';
        btn.disabled = false;
    }
});
