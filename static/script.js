document
    .getElementById("predictionForm")
    .addEventListener("submit", async function (event) {

        event.preventDefault();

        // Get values from the form
        const crop = document.getElementById("crop").value;
        const area = document.getElementById("area").value;
        const rainfall = document.getElementById("rainfall").value;
        const temperature = document.getElementById("temperature").value;
        const fertilizer = document.getElementById("fertilizer").value;
        const irrigation = document.getElementById("irrigation").value;
        const soil_ph = document.getElementById("soil_ph").value;


        // Create data object
        const data = {
            crop: crop,
            area: area,
            rainfall: rainfall,
            temperature: temperature,
            fertilizer: fertilizer,
            irrigation: irrigation,
            soil_ph: soil_ph
        };


        try {

            // Send data to Flask
            const response = await fetch("/predict", {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            });


            // Get response from Flask
            const result = await response.json();


            // Display prediction
            if (result.success) {

                document.getElementById("predictionValue").innerText =
                    result.prediction;

            } else {

                alert("Error: " + result.error);

            }

        } catch (error) {

            alert("Unable to connect to server.");

            console.error(error);

        }

    });