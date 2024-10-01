import React, { useState, useEffect } from 'react';

const ImageUploader = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [generation, setGeneration] = useState(0);
  const [processedImage, setProcessedImage] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [timerActive, setTimerActive] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    setImage(file);
    const previewURL = URL.createObjectURL(file);
    setImagePreview(previewURL);
  };

  const fetchProcessedImage = async () => {
    const formData = new FormData();
    formData.append('image', image);

    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    const reader = response.body.getReader();
    const { done, value } = await reader.read();
    if (done) {
      setIsProcessing(false);
      setTimerActive(false);
      return;
    }
    const blob = new Blob([value], { type: 'image/png' });
    const imageObjectURL = URL.createObjectURL(blob);
    setProcessedImage(imageObjectURL);
    setGeneration((prev) => prev + 1);
  };

  const handleStart = () => {
    if (!image) return;

    setIsProcessing(true);
    setTimerActive(true);
  };

  const handleStop = () => {
    setTimerActive(false);
    setIsProcessing(false);
  };

  useEffect(() => {
    if (timerActive) {
      const timer = setTimeout(() => {
        fetchProcessedImage();
      }, 0);

      return () => clearTimeout(timer);
    }
  }, [timerActive, generation]);

  return (
    <div className="container mx-auto p-5">
      <div className="mb-5 text-center">
        <input type="file" onChange={handleImageUpload} className="mb-3" />
        <button
          onClick={handleStart}
          disabled={isProcessing}
          className={`bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-700 mr-4 ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isProcessing ? 'Procesando...' : 'Iniciar Algoritmo Genético'}
        </button>
        <button
          onClick={handleStop}
          disabled={!isProcessing}
          className={`bg-red-500 text-white py-2 px-4 rounded hover:bg-red-700 ${!isProcessing ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          Parar Proceso
        </button>
      </div>

      <div className="flex justify-around mt-5">        
        <div className="w-1/2 flex flex-col items-center">
          <h3 className="text-lg font-semibold mb-2">Imagen Original</h3>
          {imagePreview && (
            <img
              src={imagePreview}
              alt="Original"
              className="border-2 border-gray-300 rounded-lg max-w-full"
            />
          )}
        </div>
        <div className="w-1/2 flex flex-col items-center">
          <h3 className="text-lg font-semibold mb-2">Imagen Procesada (Generación: {generation})</h3>
          {processedImage && (
            <img
              src={processedImage}
              alt="Processed"
              className="border-2 border-gray-300 rounded-lg max-w-full"
            />
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageUploader;
