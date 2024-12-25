(function() {
  // Check if the button already exists
  if (document.getElementById('speech-to-text-button')) return;

  // Create a microphone button
  const micButton = document.createElement('button');
  micButton.id = 'speech-to-text-button';
  micButton.textContent = '🎤';
  micButton.style.position = 'absolute';
  micButton.style.right = '10px';
  micButton.style.bottom = '10px';
  micButton.style.padding = '10px';
  micButton.style.border = 'none';
  micButton.style.borderRadius = '50%';
  micButton.style.backgroundColor = '#4CAF50';
  micButton.style.color = 'white';
  micButton.style.cursor = 'pointer';
  micButton.style.zIndex = '1000';

  // Add the button to the page
  document.body.appendChild(micButton);

  // Speech recognition setup
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    alert('Speech Recognition API not supported by your browser.');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.lang = 'en-US';

  micButton.addEventListener('click', () => {
    recognition.start();
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    const textArea = document.querySelector('textarea'); // Adjust the selector if necessary
    if (textArea) {
      textArea.value = transcript;
      textArea.dispatchEvent(new Event('input', { bubbles: true }));
    }
  };

  recognition.onerror = (event) => {
    console.error('Speech recognition error:', event.error);
  };
})();
