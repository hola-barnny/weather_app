// Toggle Dark Mode
const toggleButton = document.getElementById('toggle-dark-mode');
const body = document.body;
const container = document.querySelector('.container');

toggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    container.classList.toggle('dark-mode');
    saveDarkModePreference();
});

// Function to save the user's dark mode preference in localStorage
function saveDarkModePreference() {
    const isDarkMode = body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
}

// Check and apply dark mode preference on page load
document.addEventListener('DOMContentLoaded', () => {
    const darkModePreference = localStorage.getItem('darkMode');
    if (darkModePreference === 'enabled') {
        body.classList.add('dark-mode');
        container.classList.add('dark-mode');
    }
});

// Smoothly handle form submission without page reload
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const cityInput = form.querySelector('input[name="city"]');
    const errorDiv = document.querySelector('.error');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const cityName = cityInput.value.trim();
        
        if (cityName) {
            errorDiv.textContent = '';
            fetchWeatherData(cityName);
        } else {
            errorDiv.textContent = "Please enter a city name.";
        }
    });

    // Function to fetch weather data from the backend
    function fetchWeatherData(city) {
        fetch('/forecast', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ city: city })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                errorDiv.textContent = data.error;
            } else {
                updateWeatherUI(data);
            }
        })
        .catch(error => {
            errorDiv.textContent = "Error fetching data. Please try again.";
        });
    }

    // Function to update UI with weather data
    function updateWeatherUI(data) {
        const weatherContainer = document.querySelector('.weather-container');
        weatherContainer.innerHTML = `
            <h2>${data.weather.temperature}°C - ${data.weather.description}</h2>
            <p>Humidity: ${data.weather.humidity}%</p>
            <img src="http://openweathermap.org/img/wn/${data.weather.icon}@2x.png" alt="Weather Icon">
            <p>Wind Speed: ${data.weather.wind_speed} km/h</p>
            <p>Pressure: ${data.weather.pressure} hPa</p>
        `;
    }
});

// Dark Mode Styles with a smooth transition effect
const darkModeStyles = `
    .dark-mode {
        background-color: #2c3e50;
        color: #ecf0f1;
        transition: background-color 0.3s, color 0.3s;
    }
    
    .dark-mode button {
        background-color: #34495e;
        color: #ecf0f1;
        border: 1px solid #ecf0f1;
        transition: background-color 0.3s, color 0.3s;
    }

    .dark-mode .error {
        color: #e74c3c;
    }

    .dark-mode input,
    .dark-mode select {
        background-color: #34495e;
        color: #ecf0f1;
        border: 1px solid #7f8c8d;
    }

    .dark-mode .weather-container {
        background-color: #34495e;
        padding: 20px;
        border-radius: 8px;
    }

    .dark-mode .weather-container h2,
    .dark-mode .weather-container p {
        color: #ecf0f1;
    }

    .dark-mode a {
        color: #ecf0f1;
        text-decoration: underline;
    }

    .dark-mode a:hover {
        color: #f39c12;
    }
`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = darkModeStyles;
document.head.appendChild(styleSheet);
