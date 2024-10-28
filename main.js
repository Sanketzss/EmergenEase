const sosForm = document.getElementById('sosForm');

sosForm.addEventListener('submit', (event) => {
    event.preventDefault();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            document.getElementById('locationInput').value = `Lat: ${position.coords.latitude}, Long: ${position.coords.longitude}`;
            sosForm.submit();
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});
