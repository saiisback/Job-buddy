import React, { useEffect, useRef } from 'react';
import * as faceapi from 'face-api.js';

const FaceDetection = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    useEffect(() => {
        const loadModels = async () => {
            try {
                // Load models directly in the component
                await Promise.all([
                    faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
                    faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
                    faceapi.nets.faceExpressionNet.loadFromUri('/models'),
                ]);
                console.log('Face-api models loaded successfully');
            } catch (error) {
                console.error('Error loading face-api models:', error);
            }
        };

        const startVideo = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                videoRef.current.srcObject = stream;
            } catch (error) {
                console.error('Error starting video stream:', error);
            }
        };

        const detectFace = async () => {
            if (!videoRef.current || !canvasRef.current) return;

            const detections = await faceapi
                .detectAllFaces(videoRef.current, new faceapi.TinyFaceDetectorOptions())
                .withFaceLandmarks()
                .withFaceExpressions();

            // Clear and update canvas
            const canvas = canvasRef.current;
            const displaySize = {
                width: videoRef.current.videoWidth,
                height: videoRef.current.videoHeight,
            };
            faceapi.matchDimensions(canvas, displaySize);
            const resizedDetections = faceapi.resizeResults(detections, displaySize);

            // Draw detections
            canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
            faceapi.draw.drawDetections(canvas, resizedDetections);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
        };

        const init = async () => {
            await loadModels(); // Load models in the component
            startVideo();

            // Start detecting faces at intervals
            const interval = setInterval(detectFace, 100); // Adjust interval as needed
            return () => clearInterval(interval); // Cleanup
        };

        init();
    }, []);

    return (
        <div className="relative w-full h-auto">
            <video ref={videoRef} autoPlay muted className="w-full h-auto"></video>
            <canvas ref={canvasRef} className="absolute top-0 left-0 w-full h-full"></canvas>
        </div>
    );
};

export default FaceDetection;