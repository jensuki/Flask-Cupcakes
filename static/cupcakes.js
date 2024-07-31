$(document).ready(() => {
    // Base URL for API requests
    const BASE_URL = "http://localhost:5000/api";

    // Function to fetch and display all cupcakes
    async function fetchCupcakes() {
        // Send GET request to fetch cupcakes data
        const response = await axios.get(`${BASE_URL}/cupcakes`);
        // Extract cupcakes data from the response
        const cupcakes = response.data.cupcakes;
        // Clear the existing list of cupcakes
        $('#cupcakes-list').empty();

        // Iterate over each cupcake and create HTML for each one
        cupcakes.forEach(cupcake => {
            $('#cupcakes-list').append(`
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm cupcake-card" data-cupcake-id="${cupcake.id}">
                        <a href="/cupcake/${cupcake.id}">
                            <img src="${cupcake.image}" class="card-img-top" alt="${cupcake.flavor}">
                        </a>
                        <div class="card-body">
                            <h5 class="card-title">${cupcake.flavor}</h5>
                            <p class="card-text">
                                <strong>Size:</strong> ${cupcake.size}<br>
                                <strong>Rating:</strong> ${cupcake.rating}
                            </p>
                            <button class="btn btn-danger delete-button">Remove</button>
                        </div>
                    </div>
                </div>
            `);
        });
    }

    // Handle form submission to create a new cupcake
    $('#new-cupcake-form').submit(async (event) => {
        // Prevent the default form submission behavior
        event.preventDefault();

        // Collect form data into an object
        const data = {
            flavor: $('#flavor').val(), // Get flavor value from the form
            size: $('input[name="size"]:checked').val(), // Get selected size value
            rating: parseFloat($('#rating').val()), // Convert rating value to float
            image: $('#image').val() || null // Get image URL, default to null if empty
        };

        // Send POST request to create a new cupcake
        await axios.post(`${BASE_URL}/cupcakes`, data);
        // Refresh the list of cupcakes
        fetchCupcakes();
        // Reset the form fields
        $('#new-cupcake-form').trigger('reset');
    });

    // Handle clicking delete button to remove a cupcake
    $('#cupcakes-list').on('click', '.delete-button', async function () {
        // Get the ID of the cupcake to be deleted from the data attribute
        const cupcakeId = $(this).closest('.cupcake-card').data('cupcake-id');
        // Send DELETE request to remove the cupcake
        await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
        // Remove the cupcake card from the DOM
        $(this).closest('.cupcake-card').remove();
    });

    // Initial fetch to populate cupcakes on page load
    fetchCupcakes();
});
