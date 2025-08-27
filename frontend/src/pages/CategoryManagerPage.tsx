import React, { useEffect, useState } from "react";

const CategoryManagerPage: React.FC = () => {
  const [categories, setCategories] = useState<any[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("");
  const [newCategory, setNewCategory] = useState("");
  const [newTerm, setNewTerm] = useState("");
  const [termToMove, setTermToMove] = useState<string>("");
  const [moveToCategory, setMoveToCategory] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editCategoryName, setEditCategoryName] = useState("");
  const [editCategoryIdx, setEditCategoryIdx] = useState<number | null>(null);
  const [addTermModalOpen, setAddTermModalOpen] = useState(false);
  const [addTermValue, setAddTermValue] = useState("");
  const [addTermCategoryIdx, setAddTermCategoryIdx] = useState<number | null>(null);
  const [showAddCategoryModal, setShowAddCategoryModal] = useState(false);

  // Fetch categories and terms from backend
  const fetchCategories = async () => {
    setLoading(true);
    const res = await fetch("/api/categories");
    const data = await res.json();
    setCategories(data.categories);
    setLoading(false);
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  // Create new category
  const handleCreateCategory = async () => {
    if (!newCategory) return;
    await fetch("/api/create-category", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: newCategory }),
    });
    setNewCategory("");
    fetchCategories();
  };

  // Add new term to selected category
  const handleAddTerm = async () => {
    if (!selectedCategory || !newTerm) return;
    await fetch("/api/add-term", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category: selectedCategory, term: newTerm }),
    });
    setNewTerm("");
    fetchCategories();
  };

  // Move term to another category
  const handleMoveTerm = async () => {
    if (!termToMove || !moveToCategory) return;
    await fetch("/api/recategorize-term", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ term: termToMove, newCategory: moveToCategory }),
    });
    setTermToMove("");
    setMoveToCategory("");
    fetchCategories();
  };


  // Open edit modal for a category
  const openEditModal = (idx: number) => {
    setEditCategoryIdx(idx);
    setEditCategoryName(categories[idx].name);
    setEditModalOpen(true);
  };

  // Open add term modal for a category
  const openAddTermModal = (idx: number) => {
    setAddTermCategoryIdx(idx);
    setAddTermValue("");
    setAddTermModalOpen(true);
  };

  const handleAddTermToCategory = async () => {
    if (addTermCategoryIdx === null || !addTermValue) return;
    await fetch("/api/add-term", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category: categories[addTermCategoryIdx].name, term: addTermValue }),
    });
    setAddTermModalOpen(false);
    setAddTermValue("");
    fetchCategories();
  };

  const handleEditCategorySave = async () => {
    if (editCategoryIdx === null) return;
    // TODO: Implement backend endpoint for renaming category
    await fetch("/api/rename-category", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        oldName: categories[editCategoryIdx].name,
        newName: editCategoryName,
      }),
    });
    setEditModalOpen(false);
    fetchCategories();
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 border border-gray-200 rounded-lg bg-white shadow">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">Category Manager</h2>
      <div className="mb-8">
        <h3 className="text-lg font-semibold mb-2">All Categories</h3>
        {loading ? (
          <div>Loading...</div>
        ) : (
          <ul className="space-y-2">
            {categories
              .filter((cat: any) => cat.name.toLowerCase() !== "other")
              .slice() // copy array to avoid mutating state
              .sort((a: any, b: any) => a.name.localeCompare(b.name))
              .map((cat: any, idx: number, arr: any[]) => (
                <li key={cat.name} className="bg-gray-50 rounded p-3 flex items-center justify-between">
                  <span className="font-semibold text-gray-800">{cat.name}</span>
                  <div className="flex gap-2">
                    <button
                      className="px-3 py-1 bg-green-100 text-green-800 border border-green-400 rounded hover:bg-green-200"
                      onClick={() => openAddTermModal(categories.findIndex((c: any) => c.name === cat.name))}
                    >
                      +
                    </button>
                    <button
                      className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                      onClick={() => openEditModal(categories.findIndex((c: any) => c.name === cat.name))}
                    >
                      Edit
                    </button>
                  </div>
                </li>
              ))}
            {/* Add Category Button */}
            <li className="flex justify-center">
              <button
                className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 mt-2"
                onClick={() => setShowAddCategoryModal(true)}
              >
                + Add New Category
              </button>
            </li>
          </ul>
        )}

        {/* Add Term Modal */}
        {addTermModalOpen && addTermCategoryIdx !== null && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
            <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold mb-4">Add Term to {categories[addTermCategoryIdx].name}</h3>
              <input
                className="w-full mb-4 p-2 border rounded"
                placeholder="New term"
                value={addTermValue}
                onChange={e => setAddTermValue(e.target.value)}
              />
              <div className="flex justify-end space-x-2">
                <button
                  className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                  onClick={() => setAddTermModalOpen(false)}
                  type="button"
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  onClick={handleAddTermToCategory}
                  type="button"
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Add Category Modal */}
        {showAddCategoryModal && (
          <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
            <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold mb-4">Add New Category</h3>
              <input
                className="w-full mb-4 p-2 border rounded"
                placeholder="Category name"
                value={newCategory}
                onChange={e => setNewCategory(e.target.value)}
              />
              <div className="flex justify-end space-x-2">
                <button
                  className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                  onClick={() => setShowAddCategoryModal(false)}
                  type="button"
                >
                  Cancel
                </button>
                <button
                  className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  onClick={async () => { await handleCreateCategory(); setShowAddCategoryModal(false); }}
                  type="button"
                >
                  Add
                </button>
              </div>
            </div>
          </div>
        )}
      </div>


      {/* Edit Category Modal */}
      {editModalOpen && editCategoryIdx !== null && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-40 z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold mb-4">Edit Category</h3>
            <label className="block mb-2 font-medium">Category Name</label>
            <input
              className="w-full mb-4 p-2 border rounded"
              value={editCategoryName}
              onChange={e => setEditCategoryName(e.target.value)}
            />
            <label className="block mb-2 font-medium">Terms</label>
            <ul className="mb-4 space-y-1">
              {categories[editCategoryIdx].terms.map((term: string) => (
                <li key={term} className="bg-gray-100 rounded px-3 py-1 text-gray-700 inline-block mr-2 mb-2">
                  {term}
                </li>
              ))}
            </ul>
            <div className="flex justify-end space-x-2">
              <button
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                onClick={() => setEditModalOpen(false)}
                type="button"
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                onClick={handleEditCategorySave}
                type="button"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CategoryManagerPage;