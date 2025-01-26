import * as faceapi from 'face-api.js';

export const loadModels = async () => {
    try {
        await Promise.all([
            faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
            faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
            faceapi.nets.faceExpressionNet.loadFromUri('/models'),
        ]);
        console.log('Models loaded successfully');
    } catch (error) {
        console.error('Error loading face-api models:', error);
    }
};