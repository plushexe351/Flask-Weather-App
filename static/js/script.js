const input = document.getElementById("city");
const clearInputBtn = document.getElementById("clear-search-bar");
const inputForm = document.querySelector("form");
const submitBtn = document.querySelector("#submit");
const stat = document.querySelector("#status");
const statusImg = document.querySelector("#status-image");


console.log(statusImg?.classList[1])

window.addEventListener('load', () => {

    let statusimg = stat.textContent.includes('cloud') ? "fa-cloud" : "fa-x"
    console.log(statusimg)
    statusImg.classList[1] = statusimg
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

const sampleCities = document.querySelectorAll('.sample-locations .city');
sampleCities.forEach(city => {
    city.value = city.textContent;
})