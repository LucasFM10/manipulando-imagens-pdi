document.getElementById('imageInput').addEventListener('change', function(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var imgElement = document.createElement("img");
        imgElement.src = reader.result;
        imgElement.id = 'uploadedImage';  // Adicione um ID para facilitar a manipulação
        document.getElementById('displayArea').innerHTML = '';  // Clear previous images
        document.getElementById('displayArea').appendChild(imgElement);  // Append new image
    };
    reader.readAsDataURL(event.target.files[0]);
});

// Botão para aplicar o filtro negativo
document.getElementById('negativeBtn').addEventListener('click', function() {
    var imgData = document.getElementById('uploadedImage').src;
    $.ajax({
        type: 'POST',
        url: applyNegativeUrl,
        data: {
            'image_data': imgData,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            $('#uploadedImage').attr('src', response.new_image_src);
        },
        error: function(xhr, status, error) {
            console.error("There was an error with the AJAX request.");
        }
    });
});

// Botão para aplicar o filtro de média aritmética
document.getElementById('averageBtn').addEventListener('click', function() {
    var imgData = document.getElementById('uploadedImage').src;
    $.ajax({
        type: 'POST',
        url: applyAverageUrl,
        data: {
            'image_data': imgData,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            $('#uploadedImage').attr('src', response.new_image_src);
        },
        error: function(xhr, status, error) {
            console.error("There was an error with the AJAX request.");
        }
    });
});

