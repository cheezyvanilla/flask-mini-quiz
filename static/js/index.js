const daysIndo = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
const daysMap = {
    "Sunday": "Minggu",
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu"
}
document.addEventListener("DOMContentLoaded", () => {
    const today = new Date();
    const dayName = daysIndo[today.getDay()];
    const options = { day: 'numeric', month: 'long', year: 'numeric' };
    const dateStr = today.toLocaleDateString('id-ID', options);
    document.getElementById("current-date").textContent = `Hari ini: ${dayName}, ${dateStr}`;
});

function getWeather() {
    const city = document.getElementById("city").value;
    if (!city) return alert("Masukkan nama kota!");

    fetch(`/api/weather?city=${city}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) return alert(data.error);
            document.getElementById("forecast-table").style.display = "table";
            const tbody = document.querySelector("#forecast-table tbody");
            tbody.innerHTML = "";

            data.forecast.forEach(day => {
                const row = `<tr>
                    <td>${`${daysMap[day.day]}, ${day.date}`}</td>
                    <td>${day.day_weather}</td>
                    <td>${day.night_weather}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(err => console.error(err));
}
