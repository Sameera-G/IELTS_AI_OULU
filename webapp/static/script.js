// static/script.js

document.addEventListener("DOMContentLoaded", function() {
    const stopwatch = document.getElementById('stopwatch');
    const startStopButton = document.getElementById('startStopButton');
    const resetButton = document.getElementById('resetButton');
    const descriptionLabel = document.getElementById('descriptionLabel');
    const listenButton = document.getElementById('listenButton');
    let timer;
    let elapsedTime = 0;

    function startStopwatch() {
        if (!timer) {
            timer = setInterval(updateStopwatch, 1000);
            startStopButton.textContent = 'Pause';
        } else {
            clearInterval(timer);
            timer = null;
            startStopButton.textContent = 'Continue';
        }
    }

    function updateStopwatch() {
        elapsedTime++;
        const hours = Math.floor(elapsedTime / 3600);
        const minutes = Math.floor((elapsedTime % 3600) / 60);
        const seconds = elapsedTime % 60;
        stopwatch.textContent = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    function resetStopwatch() {
        clearInterval(timer);
        timer = null;
        elapsedTime = 0;
        stopwatch.textContent = '00:00:00';
        startStopButton.textContent = 'Start';
    }

    function loadDescriptionFromFile(filename) {
        fetch(filename)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Description file not found.');
                }
                return response.text();
            })
            .then(data => {
                descriptionLabel.textContent = data;
                descriptionLabel.style.wordWrap = 'break-word';
            })
            .catch(error => {
                console.error(error);
            });
    }

    function speakDescription() {
        const text = descriptionLabel.textContent;
        // You can implement text-to-speech functionality here if needed
        console.log('Speaking:', text);
    }

    startStopwatch(); // Start the stopwatch automatically
    startStopButton.addEventListener('click', startStopwatch);
    resetButton.addEventListener('click', resetStopwatch);
    listenButton.addEventListener('click', speakDescription);

    // Load description from file on page load
    loadDescriptionFromFile('/static/paragraphs/main_description.txt');
});
