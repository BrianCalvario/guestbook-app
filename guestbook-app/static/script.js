document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('messageForm');
    const messagesList = document.getElementById('messagesList');

    function loadMessages() {
        fetch('/messages')
            .then(res => res.json())
            .then(data => {
                messagesList.innerHTML = '';
                data.forEach(msg => {
                    const li = document.createElement('li');
                    li.textContent = `${msg.name}: ${msg.message};`
                    messagesList.appendChild(li);
                });
            });
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const message = document.getElementById('message').value;

        fetch('/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, message })
        })
        .then(() => {
            form.reset();
            loadMessages();
        });
    });

    loadMessages();
});