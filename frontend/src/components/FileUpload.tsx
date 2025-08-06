import React, { useRef } from 'react';

interface FileUploadProps {
    onFileSelect: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect }) => {
    const inputRef = useRef<HTMLInputElement>(null);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            onFileSelect(file);
        }
    };

    const handleButtonClick = () => {
        inputRef.current?.click();
    };

    return (
        <div>
            <button type="button" onClick={handleButtonClick}>
            Upload File
            </button>
            <input
            type="file"
            ref={inputRef}
            style={{ display: 'none' }}
            onChange={handleFileChange}
            accept="text/html"
            />
        </div>
    );
};

export default FileUpload;