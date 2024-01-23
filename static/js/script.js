const input = document.getElementById("city");
const clearInputBtn = document.getElementById("clear-search-bar");
const inputForm = document.querySelector("form");
const submitBtn = document.querySelector("#submit");
const stat = document.querySelector("#status");
const statusImg = document.querySelector("#status-image");
const time = document.querySelector('#time');
const sampleLocations = document.querySelectorAll('.sample-locations > div')
const weatherBackground = document.querySelector('.weather-background');
let timeofday;

window.addEventListener('load', () => {
    if (parseInt(time.textContent.split(":")[0]) > 17) {
        timeofday = "night"
        weatherBackground.classList.add('night');
        sampleLocations.forEach(location => {
            location.classList.add('night');
        })
    }
    else {
        timeofday = "day"
        weatherBackground.classList.remove('night');
        sampleLocations.forEach(location => {
            location.classList.remove('night');
        })
    }
    if (stat.textContent.includes('cloud')) {
        statusImg.src = `../static/assets/cloudy-${timeofday}.svg`
    }
    else if (stat.textContent.includes('clear')) {
        statusImg.src = `../static/assets/clear-${timeofday}.svg`
    }
    else if (stat.textContent.includes('rain')) {
        statusImg.src = `../static/assets/rain-${timeofday}.svg`
    }
    else if (stat.textContent.includes('thunder')) {
        statusImg.src = `../static/assets/thunder-${timeofday}.svg`
    }
    else if (stat.textContent.includes('snow')) {
        statusImg.src = `../static/assets/snow-${timeofday}.svg`
    }
})

clearInputBtn.addEventListener("click", () => {
    clearInputBtn.classList.remove("show");
});

input.addEventListener("input", () => {
    input.value.trim() == ""
        ? clearInputBtn.classList.remove("show")
        : clearInputBtn.classList.add("show");
});

const sampleCityDivs = document.querySelectorAll('.sample-locations > div');
sampleCityDivs.forEach(city => {
    city.addEventListener('click', () => {
        input.value = city.querySelector('.city').textContent;
        inputForm?.requestSubmit();
    })
})
