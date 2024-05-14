document.addEventListener('DOMContentLoaded', function () {
    var addProductForm = document.getElementById('addProductForm');
    var productContainer = document.getElementById('productContainer');

    // Evento de envío del formulario
    if (addProductForm) {
        addProductForm.addEventListener('submit', function(event) {
            event.preventDefault();
            // Obtener valores del formulario
            var productName = document.getElementById('productName').value;
            var productQuantity = document.getElementById('productQuantity').value;
            var productCost = document.getElementById('productCost').value; // Obtiene el costo
            var productPrice = document.getElementById('productPrice').value; // Obtiene el precio

            // Agregar el nuevo producto al array de productos existente
            var products = JSON.parse(localStorage.getItem('products')) || [];
            products.push({
                name: productName,
                quantity: productQuantity,
                cost: productCost, // Guardar el costo
                price: productPrice // Guardar el precio
            });
            localStorage.setItem('products', JSON.stringify(products));

            // Redirigir a la página de productos
            window.location.href = 'productos.html';
        });
    }

    // Cargar los productos
    if (productContainer) {
        loadProducts();
    }
});

// Función para cargar los productos
function loadProducts() {
    var products = JSON.parse(localStorage.getItem('products')) || [];
    var container = document.getElementById('productContainer');
    container.innerHTML = ''; // Limpia el contenedor antes de cargar

    // Iterar sobre los productos y mostrarlos en el DOM
    products.forEach(function(product, index) {
        var productBox = document.createElement('div');
        productBox.className = 'productBox';
        productBox.innerHTML = `
            <div class="product-detail">${product.name}</div>
            <div class="product-detail">Cantidad: ${product.quantity}</div>
            <div class="product-detail">Costo: $${product.cost}</div>
            <div class="product-detail">Precio: $${product.price}</div>
            <div class="product-icons">
                <button onclick="incrementar(${index})"><img src="images/add.png" alt="Agregar" class="icono"></button>
                <button onclick="decrementar(${index})"><img src="images/menos.png" alt="Quitar" class="icono"></button>
                <button onclick="eliminar(${index})"><img src="images/borrar.png" alt="Eliminar" class="icono"></button>
            </div>
        `;
        container.appendChild(productBox);
    });
}

    
// Las funciones incrementar, decrementar, incrementarStart, decrementarStart y stopChange siguen aquí...


// Añade las funciones incrementarStart, decrementarStart y stopChange aquí
let intervalId = null;

function incrementarStart(index) {
    stopChange(); // Detener cualquier operación anterior
    intervalId = setInterval(() => incrementar(index), 100);
}

function decrementarStart(index) {
    stopChange(); // Detener cualquier operación anterior
    intervalId = setInterval(() => decrementar(index), 100);
}

function stopChange() {
    clearInterval(intervalId);
}

function incrementar(index) {
    var products = JSON.parse(localStorage.getItem('products')) || [];
    if (products[index]) {
        products[index].quantity++;
        localStorage.setItem('products', JSON.stringify(products));
        loadProducts(); // Refresca la lista de productos
    }
}

function decrementar(index) {
    var products = JSON.parse(localStorage.getItem('products')) || [];
    if (products[index] && products[index].quantity > 1) {
        products[index].quantity--;
        localStorage.setItem('products', JSON.stringify(products));
        loadProducts(); // Refresca la lista de productos
    }
}

function eliminar(index) {
    var products = JSON.parse(localStorage.getItem('products')) || [];
    products.splice(index, 1); // Elimina el producto del array
    localStorage.setItem('products', JSON.stringify(products));
    loadProducts(); // Refresca la lista de productos
}

// Carga los productos cuando estemos en la página de productos
if (window.location.pathname.includes('productos.html')) {
    document.addEventListener('DOMContentLoaded', loadProducts);
}
