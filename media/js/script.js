$(document).ready(function () {
    $(".search").submit(function (event) {
        event.preventDefault();
        let query = $(".search input").val().trim();

        if (query.length > 0) {
            $.ajax({
                url: "/api/search/",
                type: "GET",
                data: { q: query },
                success: function (response) {
                    let resultsDiv = $("#search-results");
                    resultsDiv.empty();

                    if (response.results.length > 0) {
                        response.results.forEach(product => {
                            resultsDiv.append(`
                                <div class="product">
                                    <img src="${product.image || '/media/default.jpg'}" alt="${product.name}">
                                    <p>${product.name} - $${product.price}</p>
                                </div>
                            `);
                        });
                    } else {
                        resultsDiv.append("<p>No products found.</p>");
                    }
                },
                error: function () {
                    alert("Error fetching search results.");
                }
            });
        }
    });
});
