document.addEventListener("DOMContentLoaded", function() {
    var map = L.map("map").setView([31.5204, 74.3587], 10);  // Default location: Lahore

    // Load OpenStreetMap tiles
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    function fetchProductLocations() {
        fetch("/dashboard/api/vehicle-locations/")
        .then(response => response.json())
        .then(data => {
            data.products.forEach(product => {
                L.marker([product.latitude, product.longitude])
                    .addTo(map)
                    .bindPopup(`
                        <b>Product:</b> ${product.product_name}<br>
                        <b>Status:</b> ${product.product_status}<br>
                        <b>Delivery Date:</b> ${product.delivery_date}
                    `);
            });

            // Update dashboard cards
            if (data.products.length > 0) {
                let product = data.products[0];
                document.getElementById("product-name").innerText = product.product_name;
                document.getElementById("product-status").innerText = product.product_status;
                document.getElementById("delivery-date").innerText = product.delivery_date;
            }
        })
        .catch(error => console.error("Error fetching product locations:", error));
    }

    fetchProductLocations();
});
