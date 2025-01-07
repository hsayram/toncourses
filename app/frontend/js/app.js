// Initialize the Telegram Web App SDK without init() method
Telegram.WebApp.ready();
Telegram.WebApp.expand();

// Debug: Log initDataUnsafe to check the user object
console.log("initDataUnsafe:", Telegram.WebApp.initDataUnsafe);

// Получаем данные о пользователе
const user = Telegram.WebApp.initDataUnsafe.user;
console.log(user);

// Добавляем небольшую задержку для того, чтобы гарантировать, что данные о пользователе загрузятся
setTimeout(() => {
    // Проверяем, есть ли данные о пользователе и отображаем имя
    if (user && user.first_name) {
        document.getElementById("user-name").innerText = `Hello, ${user.first_name}!`;
    } else {
        document.getElementById("user-name").innerText = "User data not found.";
    }

    // Send the user data to the backend
    if (user && user.id) {
        fetch('https://2674-91-132-92-160.ngrok-free.app/users/telegram-login', {  // Replace localhost with actual URL if needed
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
}, 1000); // Задержка 1 секунда