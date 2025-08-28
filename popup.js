// document.addEventListener('DOMContentLoaded', () => {
//     const askButton = document.getElementById('askButton');
//     const questionInput = document.getElementById('questionInput');
//     const answerDiv = document.getElementById('answer');
//     const errorDiv = document.getElementById('error');
//     const loader = document.getElementById('loader');

//     askButton.addEventListener('click', () => {
//         // Reset UI
//         answerDiv.style.display = 'none';
//         errorDiv.style.display = 'none';
//         loader.style.display = 'block';

//         chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
//             const url = tabs[0].url;
//             const videoId = extractVideoId(url);
//             const question = questionInput.value;

//             if (!videoId) {
//                 showError("This doesn't seem to be a YouTube video page.");
//                 return;
//             }
//             if (!question.trim()) {
//                 showError("Please enter a question.");
//                 return;
//             }

//             fetchFromBackend(videoId, question);
//         });
//     });

//     function extractVideoId(url) {
//         const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
//         const match = url.match(regExp);
//         return (match && match[2].length === 11) ? match[2] : null;
//     }

//     async function fetchFromBackend(videoId, question) {
//         try {
//             const response = await fetch('http://127.0.0.1:5000/ask', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ video_id: videoId, question: question }),
//             });

//             // We now read the JSON response regardless of whether it's an error or not
//             const data = await response.json();

//             // If the response was not OK, we use the 'error' field from the JSON
//             if (!response.ok) {
//                 // Throw an error with the specific message from the server
//                 throw new Error(data.error || `HTTP error! Status: ${response.status}`);
//             }

//             showAnswer(data.answer);

//         } catch (error) {
//             console.error('Error:', error);
//             // The showError function will now display the detailed error message
//             showError(error.message);
//         }
//     }

//     function showAnswer(answerText) {
//         loader.style.display = 'none';
//         answerDiv.textContent = answerText;
//         answerDiv.style.display = 'block';
//     }

//     function showError(errorMessage) {
//         loader.style.display = 'none';
//         errorDiv.textContent = errorMessage;
//         errorDiv.style.display = 'block';
//     }
// });
document.addEventListener('DOMContentLoaded', () => {
    const askButton = document.getElementById('askButton');
    const questionInput = document.getElementById('questionInput');
    const answerDiv = document.getElementById('answer');
    const errorDiv = document.getElementById('error');
    const loader = document.getElementById('loader');

    askButton.addEventListener('click', () => {
        answerDiv.style.display = 'none';
        errorDiv.style.display = 'none';
        loader.style.display = 'block';

        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            const url = tabs[0].url;
            const videoId = extractVideoId(url);
            const question = questionInput.value;

            // // --- THIS IS THE NEW LINE FOR TESTING ---
            // // It will immediately show the video ID it found.
            // showError(`Testing - Video ID found: ${videoId}`); 
            // // --- REMOVE THIS LINE AFTER TESTING ---

            if (!videoId) {
                showError("This doesn't seem to be a YouTube video page.");
                return;
            }
            if (!question.trim()) {
                showError("Please enter a question.");
                return;
            }

            fetchFromBackend(videoId, question);
        });
    });

    function extractVideoId(url) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        return (match && match[2].length === 11) ? match[2] : null;
    }

    async function fetchFromBackend(videoId, question) {
        try {
            const response = await fetch('http://127.0.0.1:5000/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_id: videoId, question: question }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || `HTTP error! Status: ${response.status}`);
            }

            showAnswer(data.answer);

        } catch (error) {
            console.error('Error:', error);
            showError(error.message);
        }
    }

    function showAnswer(answerText) {
        loader.style.display = 'none';
        answerDiv.textContent = answerText;
        answerDiv.style.display = 'block';
    }

    function showError(errorMessage) {
        loader.style.display = 'none';
        errorDiv.textContent = errorMessage;
        errorDiv.style.display = 'block';
    }
});