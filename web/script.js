// Tab navigation and enquiry form handling
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('.tab');
  const tabContents = document.querySelectorAll('.tabcontent');
  tabs.forEach(btn => btn.addEventListener('click', () => {
    tabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(tc => tc.classList.remove('active'));
    btn.classList.add('active');
    const id = btn.dataset.tab;
    document.getElementById(id).classList.add('active');
    window.scrollTo({top:0,behavior:'smooth'});
  }));

  // Form submission
  const form = document.getElementById('enquiry-form');
  const status = document.getElementById('form-status');
  form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    status.textContent = 'Sending...';
    const data = {
      name: form.name.value,
      email: form.email.value,
      phone: form.phone.value,
      message: form.message.value
    };

    try{
      const res = await fetch('/api/send', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(data)
      });
      if(res.ok){
        status.textContent = 'Thank you — your enquiry was sent.';
        form.reset();
      } else {
        const payload = await res.json();
        status.textContent = payload.error || 'Failed to send enquiry.';
      }
    }catch(err){
      console.error(err);
      status.textContent = 'Network error — please email directly.';
    }
  });
});