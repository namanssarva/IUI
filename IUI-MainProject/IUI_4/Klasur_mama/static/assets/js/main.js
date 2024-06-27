// static/assets/js/scripts.js
document.addEventListener('DOMContentLoaded', (event) => {
    var uploadBtn = document.getElementById("uploadBtn");

    uploadBtn.onclick = function() {
        document.getElementById("uploadModal").style.display = "flex";
    };

    var closeModal = document.getElementsByClassName("close")[0];
    closeModal.onclick = function() {
        document.getElementById("uploadModal").style.display = "none";
    };

    window.onclick = function(event) {
        if (event.target == document.getElementById("uploadModal")) {
            document.getElementById("uploadModal").style.display = "none";
        }
    };

    var fileInput = document.getElementById("fileInput");

    document.getElementById("generateQuiz").addEventListener("click", function() {
        handleFileUpload("quiz");
    });

    document.getElementById("generateFlashcard").addEventListener("click", function() {
        handleFileUpload("flashcard");
    });

    document.getElementById("generateSummary").addEventListener("click", function() {
        handleFileUpload("summary");
    });

    function handleFileUpload(action) {
        var file = fileInput.files[0];
        if (file) {
            var formData = new FormData();
            formData.append('file', file);

            fetch(`/process/${file.name.split('.')[0]}/`, {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Generated " + action + ": " + data[action]);
                    // You can add code here to display the result on the page
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        } else {
            alert("Please select a file first.");
        }
    }
});