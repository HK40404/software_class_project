// Initial Ratings
const ratings = {

}

// Total Stars
const starsTotal = 5;

// Run Get Ratings when DOM loads
document.addEventListener('DOMContentLoaded', getRatings);

// Form Elements    
const productSelect = document.getElementById('product-select');
const ratingControl = document.getElementById('rating-control');

// Initial Product
let product;

// Product select change
productSelect.addEventListener('change', (e) => {
    product = e.target.value;
    // Enable rating control
    ratingControl.disabled = false;
    ratingControl.value = ratings[product];
});

// Rating Control change
ratingControl.addEventListener('blur', (e) => {
    const rating = e.target.value;

    // Make sure rating 5 or under
    if(rating > 5) {
        alert('Please rate 1 - 5');
        return;
    }

    // Change rating
    ratings[product] = rating;

    getRatings();
});

// Get ratings
function getRatings() {
    for(let rating in ratings) {
        // Get Percentage
        const starPercentage = (ratings[rating] / starsTotal) * 100;

        // Round to nearest ten
        const starPercentageRounded = `${Math.round(starPercentage / 10) * 10 }%`;
                
        // Set width of stars-inner to percentage
        document.querySelector(`.${rating} .stars-inner`).style.width = starPercentageRounded;

        // Add Number Rating
        document.querySelector(`.${rating} .number-rating`).innerHTML = ratings[rating];
    }
}