import React, { useState } from "react";

const AdminPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleLowercaseTerms = async () => {
    setLoading(true);
    setMessage("");
    try {
      const res = await fetch("/api/admin/lowercase-terms", { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setMessage("All terms have been lowercased.");
      } else {
        setMessage(data.error || "Unknown error");
      }
    } catch (e) {
      setMessage("Request failed");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border border-gray-200 rounded-lg bg-white shadow">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Admin Tools</h2>
      <button
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 mb-4"
        onClick={handleLowercaseTerms}
        disabled={loading}
      >
        {loading ? "Processing..." : "Lowercase All Terms"}
      </button>
      {message && <div className="mt-2 text-green-700">{message}</div>}
    </div>
  );
};

export default AdminPage;
