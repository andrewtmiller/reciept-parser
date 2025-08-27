import React, { useState } from "react";

const ReviewPage: React.FC = () => {
  const [data, setData] = useState<any>(() => {
    const saved = localStorage.getItem("receiptData");
    return saved ? JSON.parse(saved) : null;
  });

  if (!data) {
    return (
      <div className="max-w-xl mx-auto mt-10 p-6 border border-gray-200 rounded-lg bg-white shadow">
        <h2 className="text-2xl font-bold mb-2 text-gray-800">No Data Available</h2>
        <p className="text-gray-600">Please upload a receipt first.</p>
      </div>
    );
  }

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
          // <div key={category} className="mb-5 p-4 bg-gray-50 rounded">
          //   <h4 className="text-lg font-semibold text-gray-700 mb-2">{category}: <span class="text-sm">${categoryData.total_price.toFixed(2)}</span></h4>
          //   <ul className="list-disc list-inside space-y-1">
          //     {categoryData.items.length === 0 ? (
          //       <li className="text-gray-400 italic">No items</li>
          //     ) : (
          //       categoryData.items.map((item: any, idx: number) => (
          //         <li key={idx} className="text-gray-700">
          //           <span className="font-medium">{item.name}</span> — <span className="text-gray-600">${item.price.toFixed(2)}</span>
          //         </li>
          //       ))
          //     )}
          //   </ul>
          //   <div className="mt-2 text-sm text-gray-600 font-semibold">Total: ${categoryData.total_price.toFixed(2)}</div>
          // </div>
          <div key={category} className="mb-5 p-4 bg-gray-50 rounded" id={category}>
            <h4 className="text-left text-xl font-semibold text-gray-700">{category}</h4>
            <table className="w-full table-auto">
              <thead>
                <tr>
                  {/* <th></th> */}
                  <th className="text-left text-xl font-semibold text-gray-700"></th>
                    <th className="text-right font-semibold text-gray-700">
                    ${categoryData.total_price.toFixed(2)}
                    <button
                      className="ml-2 px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300 focus:outline-none"
                      onClick={() => navigator.clipboard.writeText(categoryData.total_price.toFixed(2))}
                      title="Copy total to clipboard"
                      type="button"
                    >
                      Copy
                    </button>
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
                    <tr key={idx}>
                        {/* <td>
                        <span role="img" aria-label="edit" className="cursor-pointer">✏️</span>
                        </td> */}
                      <td className="text-gray-700">{item.name}</td>
                      <td className="text-right text-gray-600">${item.price.toFixed(2)}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReviewPage;
