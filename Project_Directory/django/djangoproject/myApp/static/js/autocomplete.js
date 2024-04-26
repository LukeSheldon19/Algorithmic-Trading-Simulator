document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    
    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value;

        if (searchTerm.length > 0) {
            fetch(`/autocomplete/?term=${searchTerm}`) // Update with your URL
                .then(response => response.json())
                .then(data => {
                    let dataList = document.getElementById('tickerList');
                    dataList.innerHTML = '';

                    data.forEach((ticker) => {
                        let option = document.createElement('option');
                        option.value = ticker;
                        dataList.appendChild(option);
                    });
                })
                .catch(error => console.error('Error:', error));
        }
    });
});