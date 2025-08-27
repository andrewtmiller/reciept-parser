import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [htmlText, setHtmlText] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setHtmlText(""); // Clear textarea if file is selected
      setError(null);
    }
  };

  const handleTextareaChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setHtmlText(e.target.value);
    setFile(null); // Clear file if textarea is used
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file && !htmlText.trim()) {
      setError("Please select a file or paste HTML.");
      return;
    }

    const formData = new FormData();
    if (file) {
      formData.append("file", file);
    } else if (htmlText.trim()) {
      const blob = new Blob([htmlText], { type: "text/html" });
      formData.append("file", new File([blob], "pasted.html", { type: "text/html" }));
    }

    try {
      const response = await api.post("/receipts/parse", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      if (response.data && response.data.categories) {
        Object.keys(response.data.categories).forEach((cat) => {
          const category = response.data.categories[cat];
          if (!category || !Array.isArray(category.items) || category.items.length === 0) {
            delete response.data.categories[cat];
          }
        });
      }

      localStorage.setItem("receiptData", JSON.stringify(response.data));
      navigate("/review");
    } catch (err) {
      console.error(err);
      setError("Failed to parse receipt. Please try again.");
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-4 border border-gray-200 rounded">
      <h2 className="text-2xl font-semibold mb-4">Upload a Receipt</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".html"
          onChange={handleFileChange}
          className="mb-4"
          disabled={!!htmlText}
        />
        <div className="my-4 text-center text-gray-500">or</div>
        <textarea
          value={htmlText}
          onChange={handleTextareaChange}
          placeholder="Paste HTML here..."
          rows={8}
          className="w-full border border-gray-300 rounded p-2 mb-4"
          disabled={!!file}
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
