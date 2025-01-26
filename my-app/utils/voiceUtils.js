// Convert text to speech
export const speak = (text) => {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);
    synth.speak(utterance);
};

// Recognize user speech (returns promise with transcribed text)
export const recognizeSpeech = () => {
    return new Promise((resolve) => {
        const recognition = new window.webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.onresult = (event) => resolve(event.results[0][0].transcript);
        recognition.start();
    });
};