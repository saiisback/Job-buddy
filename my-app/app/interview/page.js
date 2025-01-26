"use client"
import { useEffect, useState } from 'react';
import { fetchQuestions } from '@/utils/api';
import { speak, recognizeSpeech } from '@/utils/voiceUtils';
import FaceDetection from './components/FaceDetection';

const InterviewPage = () => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestion, setCurrentQuestion] = useState(0);

    useEffect(() => {
        const getQuestions = async () => {
            const q = await fetchQuestions('Software Developer');
            setQuestions(q);
        };
        getQuestions();
    }, []);

    const askQuestion = () => {
        if (questions[currentQuestion]) {
            speak(questions[currentQuestion]); // Speak the question
        }
    };

    const handleAnswer = async () => {
        const answer = await recognizeSpeech(); // Recognize user's speech
        console.log('User Answer:', answer);
        // Move to the next question
        setCurrentQuestion((prev) => prev + 1);
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold">AI Mock Interview</h1>
            <div className="mt-6">
                <FaceDetection />
                <div className="mt-4">
                    <p className="text-lg font-medium">
                        Question: {questions[currentQuestion] || 'Loading...'}
                    </p>
                    <button
                        onClick={askQuestion}
                        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
                    >
                        Ask Question
                    </button>
                    <button
                        onClick={handleAnswer}
                        className="mt-4 px-4 py-2 bg-green-500 text-white rounded"
                    >
                        Answer
                    </button>
                </div>
            </div>
        </div>
    );
};

export default InterviewPage;