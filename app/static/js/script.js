// Toggle Dark Mode
const toggleButton = document.getElementById('toggle-dark-mode');
const body = document.body;
const container = document.querySelector('.container');

toggleButton.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    container.classList.toggle('dark-mode');
});

// Smoothly handle form submission without page reload
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const cityInput = form.querySelector('input[name="city"]');
    const errorDiv = document.querySelector('.error');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent page reload on form submission
        const cityName = cityInput.value.trim();
        
        if (cityName) {
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
        // Update weather display with received data (you can enhance this part)
        const weatherContainer = document.querySelector('.weather-container');
        weatherContainer.innerHTML = `
            <h2>${data.weather.temperature}°C - ${data.weather.description}</h2>
            <p>Humidity: ${data.weather.humidity}%</p>
            <img src="http://openweathermap.org/img/wn/${data.weather.icon}@2x.png" alt="Weather Icon">
        `;
    }
});

// Code for Dark Mode toggle
const darkModeStyles = `
    .dark-mode {
        background-color: #2c3e50;
        color: #ecf0f1;
    }
    
    .dark-mode button {
        background-color: #34495e;
        color: #ecf0f1;
    }

    .dark-mode .error {
        color: #e74c3c;
    }
`;

const styleSheet = document.createElement("style");
styleSheet.type = "text/css";
styleSheet.innerText = darkModeStyles;
document.head.appendChild(styleSheet);
