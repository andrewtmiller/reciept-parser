// src/pages/UploadPage.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post("/receipts/parse", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      console.log(response.data)

      // Save data to localStorage (or context later)
      localStorage.setItem("receiptData", JSON.stringify(response.data));
      navigate("/review");
    } catch (err) {
      console.error(err);
      setError("Failed to parse receipt. Please try again.");
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-4 border rounded">
      <h2 className="text-2xl font-semibold mb-4">Upload a Receipt</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".html"
          onChange={handleFileChange}
          className="mb-4"
        />
        <br />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Upload
        </button>
      </form>
      {error && <p className="text-red-600 mt-3">{error}</p>}
    </div>
  );
};

export default UploadPage;
