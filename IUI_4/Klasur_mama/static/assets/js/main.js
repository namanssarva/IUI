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
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Generated " + action + ": " + data[action]);
                    displayPDFLink(data.pdf_url); // Display the PDF link
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert("An error occurred while processing the file. Please try again.");
                });
        } else {
            alert("Please select a file first.");
        }
    }

    function displayPDFLink(pdfUrl) {
        var resultDiv = document.getElementById("result");
        var resultsSection = document.getElementById("results");
        resultDiv.innerHTML = `<a href="${pdfUrl}" target="_blank">Download/View Generated PDF</a>`;
        resultsSection.style.display = "block"; // Show the results section
    }
});