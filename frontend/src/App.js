import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentView, setCurrentView] = useState('list'); // 'list' or 'add-product'
  
  //Notification State
  const [notification, setNotification] = useState({show: false, message: '', type: 'success' });
  // Form States
  const [newProductName, setNewProductName] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('1'); // Defaults to Category ID 1

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await fetch('http://localhost:8000/products');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const fetchCategories = async () => {
    try{
      const response = await fetch('http://localhost:8000/categories');
      const data = await response.json();
      setCategories(data);
      {/*}
      if (data.length > 0) {
        setSelectedCategory(data[0].id.toString());
      }
      */}
    } catch (error) {
      console.error("Error fetching categories: ", error);
    }
  };

  const showToast = (message, type = 'success') => {
    setNotification({ show: true, message, type });
    setTimeout(() => {
      setNotification({show: false, message: '', type: 'success'});
    }, 4000);
  };

  const handleToggle = async (productId) => {
    try {
      const response = await fetch(`http://localhost:8000/products/${productId}/toggle`, {
        method: 'PATCH',
      });
      if (response.ok) {
        setProducts(products.map(p => 
          p.id === productId ? { ...p, is_ordered: !p.is_ordered } : p
        ));
      }
    } catch (error) {
      console.error("Error toggling product:", error);
    }
  };

  // Form submission handler
  const handleAddProductSubmit = async (e) => {
    e.preventDefault();
    if (!newProductName.trim()) return;

    try {
      const response = await fetch('http://localhost:8000/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: newProductName,
          category_id: parseInt(selectedCategory)
        })
      });

      if (response.ok) {
        showToast(`"${newProductName}" successfully added!`);
        setNewProductName(''); // Clear input
        fetchProducts();       // Refresh state list
        setCurrentView('list'); // Go back to main view
      } else {
        showToast("Failed to save product.", "error");
      }
    } catch (error) {
      console.error("Error adding product:", error);
    }
  };

  return (
    <div className="app-layout">
      {/* Notification Banner */}
      <div className={`toast-notification ${notification.show ? 'show' : ''} ${notification.type}`}>
        {notification.type === 'success' ? '✅' : '❌'} {notification.message}
      </div>
      {/* Upper Left Menu Button */}
      <button className="menu-btn" onClick={() => setIsMenuOpen(!isMenuOpen)}>
        ☰ Menu
      </button>

      {/* Slide-out Sidebar Menu */}
      <div className={`sidebar ${isMenuOpen ? 'open' : ''}`}>
        <button className="close-btn" onClick={() => setIsMenuOpen(false)}>×</button>
        <h2>Navigation</h2>
        <ul>
          <li onClick={() => { setCurrentView('list'); setIsMenuOpen(false); }}>🛒 Shopping List</li>
          <li onClick={() => { setCurrentView('add-product'); setIsMenuOpen(false); fetchCategories()}}>➕ Add New Product</li>
        </ul>
      </div>

      {/* Overlay to close menu when clicking outside */}
      {isMenuOpen && <div className="overlay" onClick={() => setIsMenuOpen(false)}></div>}

      {/* Main Content Area */}
      <div className="main-content">
        {currentView === 'list' ? (
          <div className="card">
            <h1>Grocery Shopping List 🛒</h1>
            <h3>All Products</h3>
            <ul className="product-list">
              {products.map(product => (
                <li key={product.id} className="product-item">
                  <span className="toggle-icon" onClick={() => handleToggle(product.id)}>
                    {product.is_ordered ? '✅' : '➕'}
                  </span>
                  <span className={product.is_ordered ? 'ordered-text' : ''}>
                    {product.name}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <div className="card">
            <h1>Add New Product 🆕</h1>
            <form onSubmit={handleAddProductSubmit} className="product-form">
              <div className="form-group">
                <label>Product Name:</label>
                <input 
                  type="text" 
                  value={newProductName} 
                  onChange={(e) => setNewProductName(e.target.value)} 
                  placeholder="e.g. Milk, Bread, Bananas"
                  required
                />
              </div>

              <div className="form-group">
                <label>Category:</label>
                <select 
                  value={selectedCategory} 
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                {/* Dynamically mapping database categories */}
                {categories.map(category => (
                  <option key={category.id} value={category.id}>
                    {category.category_name}
                  </option>
                ))}
                </select>
              </div>

              <button type="submit" className="submit-btn">Save Product</button>
              <button type="button" className="cancel-btn" onClick={() => setCurrentView('list')}>Cancel</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;