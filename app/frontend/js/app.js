// Initialize the Telegram Web App SDK
window.Telegram.WebApp.ready();
window.Telegram.WebApp.expand(); // Expand the app to occupy more space

// Fetch the user data from Telegram Web App
const user = window.Telegram.WebApp.initDataUnsafe?.user;

// Update UI with user data
// if (user) {
//     const username = user.username ? `@${user.username}` : '@Guest';
//     document.getElementById('user-username').textContent = username;

//     if (user.photo_url) {
//         document.getElementById('user-avatar').src = user.photo_url;
//     }
// }

// Send the user data to the backend
if (user && user.id) {
    fetch('https://b6eb-46-246-28-252.ngrok-free.app/users/telegram-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: user.id,
            username: user.username,
            first_name: user.first_name,
            last_name: user.last_name,
            language_code: user.language_code,
            is_premium: user.is_premium,
            added_to_attachment_menu: user.added_to_attachment_menu,
            allows_write_to_pm: user.allows_write_to_pm,
            photo_url: user.photo_url
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(`Fetch successful: ${JSON.stringify(data)}`);
    })
    .catch(error => {
        console.error(`Fetch error: ${error.message}`);
    });
}