import React, { useState, useEffect } from 'react';
import './App.css';

function App(){
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetchProducts();
  }, []);


  const fetchProducts = async () => {
    try{
      const response = await fetch('http://localhost:8000/products');
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error("Error fetching products:", error);
    }
  };

  const handleToogle = async (productId) => {
    try{
      const response = await fetch(`http://localhost:8000/products/${productId}/toggle`, {
        method: 'PATCH',
      });

      if(response.ok){
        setProducts(products.map(p =>
          p.id === productId ? {...p, is_ordered: !p.is_ordered } : p
        ));
      }

    } catch (error) {
        console.error("Error toggling product: ", error);
      }
  };

  return (
    <div className="app-container">
      <h1>Grocery Shopping List</h1>
      <div className="list-section">
        <h3>All Products</h3>
        <ul className="product-list">
          {products.map(product => (
            <li key={product.id} className="product-item">
              <span
                className="toggle-icon"
                onClick={() => handleToogle(product.id)}
                style={{ cursor: 'pointer', marginRight: '15px', fontSize: '1.2rem' }}
              >
                {product.is_ordered ? '✅' : '➕'}
              </span>
              <span className={product.is_ordered ? 'ordered-text' : ''}>
                {product.name}
              </span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
export default App;