import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  //Authentication States
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState('login')
  const [authUsername, setAuthUsername] = useState('');
  const [authPassword, setAuthPassword] = useState('');

  //Application States
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [currentView, setCurrentView] = useState('list'); // 'list'--'add-product'--'add-category'--'delete-product'--'detele-category'
  const [notification, setNotification] = useState({show: false, message: '', type: 'success' });
  
  // Form States
  const [newProductName, setNewProductName] = useState('');
  const [newCategoryName, setNewCategoryName] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('1'); // Defaults to Category ID 1
  const [productToDelete, setProductToDelete] = useState('');
  const [categoryToDelete, setCategoryToDelete] = useState('');
  
  useEffect(() => {
    if (user)
    fetchProducts();
  }, [user]);

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    const endpoint = authMode === 'login' ? 'login' : 'register';
    try{
      const response = await fetch(`http://localhost:8000/auth/${endpoint}`, {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({username: authUsername, password: authPassword})
      });
      const data = await response.json();

      if(response.ok){
        if(authMode === 'login'){
          setUser({token: data.token, username: data.username, role: data.role});
          showToast(`Welcome back, ${data.username}!`);
          setCurrentView('list');
        } else {
          showToast("Registration successful! Please log in.");
          setAuthMode('login');
        }
        setAuthPassword('');
      } else {
        showToast(data.detail || "Authentication failed.", "error");
      }
    } catch (error){
      showToast("Network error occurres", "error");
    }
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentView('list');
    showToast("Logged out successfully");
  };


  //Helper filter: lists only products that match the currently selected category
  const filteredProductsToDelete = products.filter(
    p => p.category_id === parseInt(selectedCategory)
  );

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
        showToast(`${newProductName} successfully added!`);
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


  const handleAddCategorySubmit = async (e) => {
    e.preventDefault();
    if (!newCategoryName.trim()) return;

    try{
      const response = await fetch('http://localhost:8000/categories', {
        method: 'POST',
        headers: {'Content-type' : 'application/json'},
        body: JSON.stringify({
          category_name : newCategoryName
        })
      });

      if (response.ok){
        showToast(`${newCategoryName} successfully added!`);
        setNewCategoryName('');
        fetchCategories();
        setCurrentView('list');
      } else {
        showToast(`Failed to add category ${newCategoryName}.`, "error");
      }
    } catch (error) {
      console.error("Error adding category", "error")
    }
  }


  const handleDeleteProductSubmit = async (e) => {
    e.preventDefault();
    if (!productToDelete){
      showToast("No product selected to delete.", "error")
      return;
    }
    if (!window.confirm(`Are you sure to delete "${productToDelete}"?`)) return;

    try{
      const response = await fetch(`http://localhost:8000/products/${encodeURIComponent(productToDelete)}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      if (response.ok){
        showToast(data.message);
        fetchProducts();
        setCurrentView('list');
      } else {
        showToast(data.detail || "Failed to delete product.", "error");
      }
    } catch (error) {
      console.error("Error deleting product", error);
      showToast("Network error occured.", "error");
    }
  };


  const handleDeleteCategorySubmit = async (e) => {
    e.preventDefault();
    if (!categoryToDelete){
      showToast("No category selected to delete.", "error")
      return;
    }
    if (!window.confirm(`Are you sure to delete "${categoryToDelete}"?`)) return;
    
    try{
      const response = await fetch(`http://localhost:8000/categories/${encodeURIComponent(categoryToDelete)}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      if (response.ok){
        showToast(data.message);
        fetchCategories();
        setCurrentView('list');
      } else {
        showToast(data.detail || "Failed to remove the category.", "error");
      }
    } catch (error) {
      console.error("Error deleting category", error);
      showToast("Network error occured.", "error");
    }
  };
  if (!user){
    return (
    <div className="app-layout" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '10vh'}}>
      <div className="card" style={{maxWidth: '400px', width: '100%'}}>
        <h1>{authMode === 'login' ? 'Login' : 'Register'}</h1>
        <form onSubmit={handleAuthSubmit} className="product-form">
          <div className="form-group">
            <label>Username</label>
            <input type="text" value={authUsername} onChange={(e) => setAuthUsername(e.target.value)} required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" value={authPassword} onChange={(e) => setAuthPassword(e.target.value)} required />
          </div>
          <button type="submit" className="submit-btn">
            {authMode === 'login' ? 'Sign In' : 'Sign Up'}
          </button>
          <p style={{ textAlign: 'center', marginTop: '15px', cursor: 'pointer', color: '#007bff'}}
            onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}>
              {authMode === 'login' ? "Don't have an account? Register." : "Already have an account? Login."}
            </p>
        </form>
      </div>
    </div> 
    )
  }
  return (
    <div className="app-layout">
      {/* Notification Banner */}
      <div className={`toast-notification ${notification.show ? 'show' : ''} ${notification.type}`}>
        {notification.type === 'success' ? '' : '❌'} {notification.message}
      </div>
      {/* Upper Left Menu Button */}
      <button className="menu-btn" onClick={() => setIsMenuOpen(!isMenuOpen)}>
        ☰ Menu
      </button>

      {/* Slide-out Sidebar Menu */}
      <div className={`sidebar ${isMenuOpen ? 'open' : ''}`}>
        <button className="close-btn" onClick={() => setIsMenuOpen(false)}>×</button>
        <h2>Hello, {user.username} <span style={{ fontSize: '12px', display: 'block', color: '#aaa'}}>({user.role})</span></h2>
        <ul>
          <li onClick={() => { setCurrentView('list'); setIsMenuOpen(false); }}>🛒 Shopping List</li>
          {user.role === 'admin' && (
            <>
              <li onClick={() => { setCurrentView('add-product'); setIsMenuOpen(false); fetchCategories()}}>➕ Add New Product</li>
              <li onClick={() => { setCurrentView('add-category'); setIsMenuOpen(false)}}>➕ Add New Category</li>
              <li onClick={() => { setCurrentView('delete-product'); setIsMenuOpen(false); fetchCategories();}}>Remove a Product</li>
              <li onClick={() => { setCurrentView('delete-category'); setIsMenuOpen(false); fetchCategories();}}>Remove a Category</li>
            </>
          )}
          <li onClick={handleLogout} style={{ color: '#e55353', marginTop: '20px', borderTop: '1px solid #444', paddingTop: '10px'}}>Logout</li>
        </ul>
      </div>

      {/* Overlay to close menu when clicking outside */}
      {isMenuOpen && <div className="overlay" onClick={() => setIsMenuOpen(false)}></div>}

      {/* Main Content Area */}
      <div className="main-content">
        {(() => {
          if (currentView !== 'list' && user.role !== 'admin'){
            return <div className="card"><h1>Access Denied</h1><p>Guests only have access to the Shopping List page.</p></div>;
          }
          switch (currentView) {
            case 'list':
              return (
                <div className="card">
                  <h1>Grocery Shopping List</h1>
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
              );
            case 'add-product':
              return (
                <div className="card">
                  <h1>Add New Product</h1>
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
                        onChange={(e) => setSelectedCategory(e.target.value)}>
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
              );
            case 'add-category':
              return (
                <div className="card">
                  <h1>Add New Category</h1>
                  <form onSubmit={handleAddCategorySubmit} className="product-form">
                    <div className="form-group">
                      <label>Category Name:</label>
                      <input
                        type="text"
                        value={newCategoryName}
                        onChange={(e) => setNewCategoryName(e.target.value)}
                        placeholder="e.g. Meat, Frozen, Snacks"
                        required
                      />
                    </div>

                    <button type="submit" className="submit-btn">Save Category</button>
                    <button type="button" className="cancel-btn" onClick={() => setCurrentView('list')}>Cancel</button>
                  </form>
                </div>
              );

            case 'delete-product':
              return (
                <div className="card">
                  <h1>Remove a Product 🗑️</h1>
                  <form onSubmit={handleDeleteProductSubmit} className="product-form">
                    
                    {/* Dropdown 1: Select Category Filter */}
                    <div className="form-group">
                      <label>Filter by Category:</label>
                      <select value={selectedCategory} onChange={(e) => {
                        setSelectedCategory(e.target.value);
                        setProductToDelete('');
                        }}>
                        {categories.map(category => (
                          <option key={category.id} value={category.id}>{category.category_name}</option>
                        ))}
                      </select>
                    </div>

                    {/* Dropdown 2: Dynamic matching products dropdown */}
                    <div className="form-group">
                      <label>Select Product to Delete:</label>
                      <select 
                        value={productToDelete} 
                        onChange={(e) => setProductToDelete(e.target.value)}
                        disabled={filteredProductsToDelete.length === 0}
                      >
                        {filteredProductsToDelete.length === 0 ? (
                          <option value="">-- No products in this category --</option>
                        ) : (
                          <>
                            <option value="">--Choose a product --</option>
                            {filteredProductsToDelete.map(product => (
                              <option key={product.id} value={product.name}>{product.name}</option>
                            ))}
                          </>
                        )}
                      </select>
                    </div>

                    <button 
                      type="submit" 
                      className="submit-btn" 
                      style={{ backgroundColor: '#e55353' }}
                      disabled={!productToDelete}
                    >
                      Delete Selected Product
                    </button>
                    <button type="button" className="cancel-btn" onClick={() => setCurrentView('list')}>Cancel</button>
                  </form>
                </div>
              );

              case 'delete-category':
              return (
                <div className="card">
                  <h1>Remove a Category 🗑️</h1>
                  <form onSubmit={handleDeleteCategorySubmit} className="product-form">
                    
                    {/* Dropdown 1: Select Category Filter */}
                    <div className="form-group">
                      <label>Choose Category:</label>
                      <select value={categoryToDelete} onChange={(e) => setCategoryToDelete(e.target.value)}>
                        {categories.map(category => (
                          <option key={category.id} value={category.category_name}>{category.category_name}</option>
                        ))}
                      </select>
                    </div>

                    <button 
                      type="submit" 
                      className="submit-btn" 
                      style={{ backgroundColor: '#e55353' }}
                      disabled={!categoryToDelete}
                    >
                      Delete Selected Category
                    </button>
                    <button type="button" className="cancel-btn" onClick={() => setCurrentView('list')}>Cancel</button>
                  </form>
                </div>
              );

              default:
                return <div>Page not found.</div>;
          }
        })()}
      </div>
    </div>
  );
}

export default App;