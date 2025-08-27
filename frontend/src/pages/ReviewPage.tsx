import React, { useState, useEffect } from "react";

const ReviewPage: React.FC = () => {
  const [data, setData] = useState<any>(() => {
    const saved = localStorage.getItem("receiptData");
    return saved ? JSON.parse(saved) : null;
  });
  const [modalOpen, setModalOpen] = useState(false);
  const [editItem, setEditItem] = useState<any>(null);
  const [newCategory, setNewCategory] = useState("");
  const [newTerm, setNewTerm] = useState("");
  const [allCategories, setAllCategories] = useState<string[]>([]);

  // Fetch all categories from backend for the dropdown
  useEffect(() => {
    const fetchCategories = async () => {
      const res = await fetch("/api/categories");
      const result = await res.json();
      if (result.categories) {
        setAllCategories(result.categories.map((cat: any) => cat.name));
      }
    };
    fetchCategories();
  }, []);

  if (!data) {
    return (
      <div className="max-w-xl mx-auto mt-10 p-6 border border-gray-200 rounded-lg bg-white shadow">
        <h2 className="text-2xl font-bold mb-2 text-gray-800">No Data Available</h2>
        <p className="text-gray-600">Please upload a receipt first.</p>
      </div>
    );
  }

  const handleEditClick = (category: string, item: any) => {
    setEditItem({ ...item, oldCategory: category });
    setNewCategory(category);
    setNewTerm(item.name);
    setModalOpen(true);
  };

  const handleModalClose = () => {
    setModalOpen(false);
    setEditItem(null);
    setNewCategory("");
    setNewTerm("");
  };

  const handleSave = async () => {
    await fetch("/api/update-term", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        oldCategory: editItem.oldCategory,
        oldTerm: editItem.name,
        newCategory,
        newTerm,
      }),
    });
    // Re-categorize the receipt data locally
    setData((prev: any) => {
      if (!prev) return prev;
      // Remove the item from the old category
      const oldCatItems = prev.categories[editItem.oldCategory].items.filter((i: any) => i.name !== editItem.name);
      // Add the item to the new category (or create it if not present)
      const newCatItems = prev.categories[newCategory]?.items ? [...prev.categories[newCategory].items] : [];
      // If the term already exists in the new category, update it; else add it
      const existingIdx = newCatItems.findIndex((i: any) => i.name === newTerm);
      const updatedItem = { ...editItem, name: newTerm };
      if (existingIdx !== -1) {
        newCatItems[existingIdx] = updatedItem;
      } else {
        newCatItems.push(updatedItem);
      }
      // Rebuild categories
      const newCategories = { ...prev.categories };
      newCategories[editItem.oldCategory] = {
        ...newCategories[editItem.oldCategory],
        items: oldCatItems,
        total_price: oldCatItems.reduce((sum: number, i: any) => sum + i.price, 0)
      };
      newCategories[newCategory] = {
        ...newCategories[newCategory],
        items: newCatItems,
        total_price: newCatItems.reduce((sum: number, i: any) => sum + i.price, 0)
      };
      return { ...prev, categories: newCategories };
    });
    handleModalClose();
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border border-gray-200 rounded-lg bg-white shadow">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Review Parsed Receipt</h2>
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-700 mb-1">Store: <span className="font-normal">{data.store}</span></h3>
        <p className="text-gray-600">Total Items: <span className="font-semibold">{Object.values(data.categories).reduce((acc: number, cat: any) => acc + cat.items.length, 0)}</span></p>
        <p className="text-gray-600">Total Price: <span className="font-semibold">${Object.values(data.categories).reduce((acc: number, cat: any) => acc + cat.total_price, 0).toFixed(2)}</span></p>
      </div>
      <div className="mb-6">
        <h3 className="text-xl font-semibold text-gray-800 mb-2">Category Totals</h3>
        <ul className="space-y-2">
          {Object.entries(data.categories).map(([category, categoryData]: [string, any]) => {
            const overallTotal = Object.values(data.categories).reduce(
              (acc: number, cat: any) => acc + cat.total_price,
              0
            );
            const percent =
              overallTotal > 0
          ? ((categoryData.total_price / overallTotal) * 100).toFixed(1)
          : "0.0";
            return (
              <li key={category} className="flex items-center justify-between bg-gray-50 rounded px-3 py-2">
          <a
            href={`#${category}`}
            className="font-medium text-blue-600 hover:underline focus:outline-none"
          >
            {category}
          </a>
          <span className="flex items-center space-x-2">
            <span className="font-semibold text-gray-800">
              ${categoryData.total_price.toFixed(2)}
            </span>
            <button
              className="px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300 focus:outline-none"
              onClick={() => navigator.clipboard.writeText(categoryData.total_price.toFixed(2))}
              title="Copy total to clipboard"
              type="button"
            >
              Copy
            </button>
            <span className="text-gray-600">({percent}%)</span>
            <button
              className="px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300 focus:outline-none"
              onClick={() => navigator.clipboard.writeText(percent + "%")}
              title="Copy percentage to clipboard"
              type="button"
            >
              Copy %
            </button>
          </span>
              </li>
            );
          })}
        </ul>
      </div>
      <div>
        <h3 className="text-xl font-semibold text-gray-800 mb-2">Categories</h3>
        {Object.entries(data.categories).map(([category, categoryData]: [string, any]) => (
          <div key={category} className="mb-5 p-4 bg-gray-50 rounded" id={category}>
            <table className="w-full table-auto">
              <thead>
                <tr>
                  <th className="text-left text-xl font-semibold text-gray-700 py-3">{category}</th>
                  <th className="text-right font-semibold text-gray-700 p-3"  onClick={() => navigator.clipboard.writeText(categoryData.total_price.toFixed(2))}>
                    ${categoryData.total_price.toFixed(2)}
                  </th>
                </tr>
              </thead>
              <tbody>
                {categoryData.items.length === 0 ? (
                  <tr>
                    <td colSpan={2} className="text-gray-400 italic">No items</td>
                  </tr>
                ) : (
                  categoryData.items.map((item: any, idx: number) => (
                    <tr
                      key={idx}
                      className={`group ${idx % 2 === 0 ? 'bg-gray-100' : 'bg-gray-200'}`}
                    >
                      <td className="text-gray-700 flex items-center py-3 px-2">
                        {item.name}
                        <button
                          className="ml-2 p-1 text-xs rounded hover:bg-blue-100 focus:outline-none invisible group-hover:visible"
                          onClick={() => handleEditClick(category, item)}
                          type="button"
                          aria-label="Edit Category"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536M9 13l6.536-6.536a2 2 0 112.828 2.828L11.828 15.828a2 2 0 01-1.414.586H7v-3a2 2 0 01.586-1.414z" />
                          </svg>
                        </button>
                      </td>
                      <td className="text-right text-gray-600 py-3 px-2">${item.price.toFixed(2)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ))}
      {/* Modal for editing category/term */}
      {modalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Edit Item Category</h3>
            <label className="block mb-2 font-medium">Category</label>
            <select
              className="w-full mb-4 p-2 border rounded"
              value={newCategory}
              onChange={e => setNewCategory(e.target.value)}
            >
              {allCategories.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
            <label className="block mb-2 font-medium">Term (text for database)</label>
            <input
              className="w-full mb-4 p-2 border rounded"
              value={newTerm}
              onChange={e => setNewTerm(e.target.value)}
            />
            <div className="flex justify-end space-x-2">
              <button
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                onClick={handleModalClose}
                type="button"
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                onClick={handleSave}
                type="button"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  );
};

export default ReviewPage;
