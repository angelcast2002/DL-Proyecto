import { useState } from 'react';
import { FiUpload } from 'react-icons/fi';

const Drop = () => {
    const [videoFile, setVideoFile] = useState(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleDrop = (event) => {
        event.preventDefault();
        setIsDragging(false);
        const file = event.dataTransfer.files[0];
        if (file && file.type.startsWith('video/')) {
            setVideoFile(file);
        }
    };

    const handleDragOver = (event) => {
        event.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleUpload = async () => {
        if (videoFile) {
            // Aquí puedes añadir lógica para comprimir el video antes de enviarlo
            console.log('Enviando el video al servidor:', videoFile);
            // Simular el envío del video por medio de una API
        }
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div
                className={`border-4 border-dashed rounded-xl w-full max-w-lg p-10 transition-all duration-300 ${
                    isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
            >
                {videoFile ? (
                    <div className="text-center">
                        <p className="text-lg font-semibold mb-4">Archivo: {videoFile.name}</p>
                        <button
                            onClick={handleUpload}
                            className="bg-blue-500 text-white px-5 py-2 rounded-lg hover:bg-blue-600 transition-all"
                        >
                            Subir Video
                        </button>
                    </div>
                ) : (
                    <div className="flex flex-col items-center">
                        <FiUpload size={40} className="mb-4 text-gray-400" />
                        <p className="text-gray-500 font-semibold mb-4">
                            Arrastra y suelta un video aquí, o haz click para seleccionarlo.
                        </p>
                        <input
                            type="file"
                            accept="video/*"
                            onChange={(e) => setVideoFile(e.target.files[0])}
                            className="hidden"
                            id="videoInput"
                        />
                        <label
                            htmlFor="videoInput"
                            className="cursor-pointer bg-blue-500 text-white px-5 py-2 rounded-lg hover:bg-blue-600 transition-all"
                        >
                            Seleccionar Video
                        </label>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Drop;
