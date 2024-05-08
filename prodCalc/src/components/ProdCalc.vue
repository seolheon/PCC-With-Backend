<template>
  <el-container>
    <el-header class="calc-header">
      <div class="h-wrapper">
        <h1>Product Cost Calc</h1>
      </div>

      <el-button type="primary" :icon="ShoppingCart" @click="openCart" /> 
      <el-dialog v-model="cartVisible" title="Cart" width="500" center>

        <el-table v-show="cartItems.length" :data="cartItems" border>
          <el-table-column prop="name" label="Product Name"></el-table-column>
          <el-table-column prop="quantity" label="Quantity"></el-table-column>
          <el-table-column prop="cost" label="Cost"></el-table-column>
        </el-table>

        <div v-show="cartItems.length" class="total-cost">
          Total Cost: {{ totalCost }}
        </div>

        <div v-show="!cartItems.length" class="empty-cart">
          Cart is empty
        </div>

        <template #footer>
          <div class="dialog-footer">
            <el-button @click="closeCart">Cancel</el-button>
            <el-button v-show="cartItems.length" type="primary" @click="closeCart">
              Order
            </el-button>
          </div>
        </template>
      </el-dialog>

    </el-header>

    <el-main class="card">

      <section class="dropdown-section">
        <div class="dropdown-wrapper">
            <el-dropdown @command="handleCategoryChange">
          <span class="dropdown-link">
            <label v-if="!selectedCategory" class="c-label">Choose category</label>
            <label v-else class="c-label">{{selectedCategory}}</label>
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu class="dropdown-menu">
              <el-dropdown-item v-if="!categories.length" disabled=true class="c-label">No categories available</el-dropdown-item>
              <el-dropdown-item v-else v-for="(category, index) in categories" :key="index" :command="category.name">{{ category.name }}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      
        <div v-if="selectedCategory" class="dropdown-wrapper">
          <el-dropdown @command="selectedProduct = $event">
            <span class="dropdown-link">
              <label v-if="!selectedProduct" class="c-label">Choose product</label>
              <label v-else class="c-label">{{selectedProduct.name}}</label>
              <el-icon class="el-icon--right"><arrow-down /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu class="dropdown-menu">
                <el-dropdown-item v-if="!products.length" disabled=true class="c-label">No products available</el-dropdown-item>
                <el-dropdown-item v-else v-for="product in products" :key="product.name" :command="product">{{ product.name }}</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>  
      </div>
    </section>
          
      <section class="product-details" v-if="selectedProduct">
        <div class="image-wrapper">
          <img class="product-image" :src="selectedProduct.image"/>
        </div>
        <div class="description-wrapper">

          <div class="name-wrapper"> 
            <label>Name: </label>
            <label class="name">{{ selectedProduct.name }}</label>
          </div>

          <div class="cost-wrapper"> 
            <label >Cost: </label>
            <label class="cost">{{ selectedProduct.cost }}</label>
          </div>

          <div class="quantity-wrapper"> 
            <label>Quantity</label>
            <input v-model.number="quantity" class="quantity-input" @change="handleQuantityChange(quantity)"/>
          </div>

          <el-button type="primary" @click="addToCart">Add to cart</el-button>
        </div>
      </section>

    </el-main>
    <el-footer></el-footer>

  </el-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ArrowDown, ShoppingCart } from '@element-plus/icons-vue';

const selectedCategory = ref('');
const selectedProduct = ref(null);
const categories = ref([]);
const products = ref([]);
const cartItems = ref([]);
const totalCost = ref(0);
const cartVisible = ref(false);
const quantity = ref(1);

const loadCategories = async () => {
  try {
    const url = '/api/categories';
    const response = await axios.get(url);
    categories.value = response.data; 
  } catch (error) {
    console.error('Error loading categories:', error);
  }
};

const loadProducts = async (categoryName) => {
  try {
    const url = `/api/products/${categoryName}/`;
    const response = await axios.get(url);
    products.value = response.data; 
  } catch (error) {
    console.error('Error loading products:', error);
  }
};

const addToCart = () => {
  if (selectedProduct.value && quantity.value) {
    const existingItem = cartItems.value.find(item => item.name === selectedProduct.value.name);
    const cost = calculateCost(selectedProduct.value.cost, quantity.value); 
    if (existingItem) {
      existingItem.quantity += quantity.value;
      existingItem.cost += cost;
    } else {
      cartItems.value.push({ name: selectedProduct.value.name, quantity: quantity.value, cost: cost });
    }
    totalCost.value += cost;
  } else {
    ElMessage.error('Please select a product and enter quantity');
  }
};

const calculateCost = (cost, quantity) => {
  return cost * quantity; 
};

const handleQuantityChange = (value) => {
  if (value <= 0) {
    quantity.value = 1;
  }
};

const openCart = () => {
  console.log('Opening cart...');
  cartVisible.value = true;
};

const closeCart = () => {
  console.log('Closing cart...');
  cartVisible.value = false;
};

const handleCategoryChange = (category) => {
  selectedCategory.value = category;
  selectedProduct.value = null;
};

onMounted(async () => {
  await loadCategories(); 
});

watch(selectedCategory, async (newValue) => {
  if (newValue) {
    await loadProducts(newValue); 
  }
});
</script>

<style scoped>

.calc-header {
  background-color: #303030;
  min-width: 100vh;
  display: flex;
  justify-content: space-between;
  place-items: center;
  border-radius: 10px 10px 0px 0px;
}

.h-wrapper {
  color: #909090;
  font: 18px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

.card {
  background-color: #303030;
  border-radius: 0px 0px 10px 10px;
}

.dropdown-section {
  display: flex;
  justify-content: center;
  place-items: center;
  gap: 100px;
}

.dropdown-wrapper {
  background-color: #202020;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  place-items: center;
  gap: 20px;
  padding: 10px 10px;
}

.c-label {
  color: #909090;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

.product-details {
  display: flex;
  justify-content: center;
  place-items: center;
  gap: 50px;
  margin: 30px 0px 50px 0px;
}

.description-wrapper {
  display: flex;
  flex-direction: column;
  gap: 10px;
  color: #909090;
  width: 200px;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

.name-wrapper, .cost-wrapper {
  display: flex;
  justify-content: space-between;
  place-items: center;
}

.name, .cost {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin-left: 100px;
}

.quantity-wrapper {
  margin-bottom: 15px;
  display: flex;
  justify-content: space-between;
  place-items: center;
}

.quantity-input {
  background-color: #202020;
  border-radius: 10px;
  color: #909090;
  padding-left: 10px;
  border: none;
  max-width: 40px;
}

.product-image {
  max-width: 130px;
}


.dropdown-link {
  cursor: pointer;
  color: #909090;
  background-color: #202020;
  display: flex;
  align-items: center;
  border:none;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

.dropdown-link :hover {
  cursor: pointer;
}

.el-dropdown:focus-visible {
  border:none;
  outline: none;
  box-shadow: none;
}

.dropdown-link:focus-visible {
  border:none;
  outline: none;
  box-shadow: none;
}

.dropdown-menu{
  cursor: pointer;
  background-color: #202020;
  display: flex;
  flex-direction: column;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #303030;
  color: #fff;
}

:deep(.el-dialog) {
  background-color: #404040;
  border-radius: 15px;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-dialog .el-table) {
  background-color: #404040;
  border: none;
  --el-table-border-color: #808080; 
  font: 600 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-table .el-table__cell) {
  color: #909090;
  background-color: #404040;
  border: none;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-dialog) {
  background-color: #404040;
  border-radius: 15px;
  font: 400 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-dialog .el-dialog__title) {
  color: #959595;
  font: 600 24px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover>td.el-table__cell) {
  background-color: #282828;
}

.total-cost {
  justify-content: right;
  display: flex;
  margin-top: 20px;
  color: #fff;
  font: 400 16px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

.empty-cart {
  justify-content: center;
  display: flex;
  margin: 30px 0px;
  color: #fff;
  font: 400 24px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-button) {
  background-color: #606060;
  border-color: #454545;
  color: #000;
  outline: none;
  font: 600 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-button--primary) {
  background-color: #71d1b1;
  border-color: #549982;
  color: #000;
  outline: none;
  font: 600 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}

:deep(.el-button:active) {
  background-color: #2b2a2a;
  border-color: #454545;
  color: #000;
  outline: none;
  font: 600 14px Montserrat Alternates, -apple-system, Roboto, Helvetica, sans-serif;
}
</style>
