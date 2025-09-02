import { Link, useLocation } from "react-router-dom";

const navItems = [
  { name: "Upload Receipt", path: "/upload" },
  { name: "Review Receipts", path: "/review" },
  { name: "Manage Categories", path: "/categories" },
];

export default function NavBar() {
  const location = useLocation();
  return (
    <nav className="bg-gray-800 text-white px-4 py-2 flex gap-4 items-center">
      <span className="font-bold text-lg">Receipt Handler</span>
      {navItems.map((item) => (
        <Link
          key={item.path}
          to={item.path}
          className={`px-3 py-1 rounded hover:bg-gray-700 transition-colors ${
            location.pathname === item.path ? "bg-gray-700" : ""
          }`}
        >
          {item.name}
        </Link>
      ))}
    </nav>
  );
}
