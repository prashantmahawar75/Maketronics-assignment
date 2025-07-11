#  Maketronic's Smart Data Display - Tech Products Hub

A modern, responsive web application for displaying and managing tech products with real-time data fetching and interactive filtering capabilities.


##  Features

### Frontend Features
- **Responsive Design**: Modern, mobile-first design with gradient backgrounds and smooth animations
- **Real-time Search**: Instant product filtering by name, description, or category
- **Category Filtering**: Filter products by smartphone, laptop, headphones, gaming, and accessories
- **Interactive UI**: Hover effects, smooth transitions, and engaging user experience
- **Statistics Dashboard**: Live product count and filtering statistics
- **Refresh Functionality**: Manual data refresh with loading indicators

### Backend Features
- **RESTful API**: Clean, documented API endpoints for all operations
- **Web Scraping**: Automated product data collection from multiple sources
- **Data Caching**: In-memory caching for improved performance
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Error Handling**: Comprehensive error handling and logging
- **Health Monitoring**: Health check endpoints for system monitoring

##  Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox/grid
- **JavaScript** - Vanilla JS for interactivity
- **Responsive Design** - Mobile-first approach

### Backend
- **Python 3.8+** - Server-side language
- **Flask** - Web framework
- **BeautifulSoup4** - Web scraping
- **Requests** - HTTP client
- **Flask-CORS** - Cross-origin support

##  Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Internet connection (for web scraping)

##  Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/prashantmahawar75/Maketronics-assignment
   cd Maketronics-assignment
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional)
   ```bash
   # Create .env file for additional configuration
   touch .env
   ```

##  Usage

### Running the Application

1. **Start the Flask backend**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **Open the frontend**
   - Open `index.html` in your browser, or
   - Visit `http://localhost:5000` to see the API documentation

### Using the Interface

1. **Search Products**: Use the search bar to find products by name, description, or category
2. **Filter by Category**: Click category buttons to filter products
3. **Refresh Data**: Click the refresh button to update product data
4. **View Details**: Click "View Product" to visit the product page

##  API Documentation

### Base URL
```
http://localhost:5000/api
```

### Endpoints

#### Get All Products
```http
GET /api/products
```

**Query Parameters:**
- `search` - Search term for products
- `category` - Filter by category (smartphone, laptop, etc.)
- `limit` - Limit number of results
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter

**Example:**
```bash
curl "http://localhost:5000/api/products?search=laptop&category=laptop"
```

#### Get Single Product
```http
GET /api/products/{id}
```

#### Refresh Product Data
```http
POST /api/refresh
```

#### Get Categories
```http
GET /api/categories
```

#### Get Statistics
```http
GET /api/stats
```

#### Health Check
```http
GET /api/health
```

### Response Format

All API responses follow this structure:
```json
{
  "success": true,
  "data": [...],
  "total": 20,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

##  Project Structure

```
Maketronics-assignment/
├── app.py                 # Flask backend application
├── index.html            # Frontend HTML (from paste.txt)
├── requirements.txt      # Python dependencies

```


### Customization

1. **Add New Product Sources**: Edit the `sources` list in `scrape_tech_products()`
2. **Modify Categories**: Update the category filters in both frontend and backend
3. **Change Styling**: Customize CSS in the `<style>` section of `index.html`
4. **Add New Endpoints**: Extend the Flask app with additional routes


##  Security Notes

- **Web Scraping**: Respect robots.txt and rate limits
- **CORS**: Configure CORS properly for production
- **Input Validation**: Validate all user inputs
- **Rate Limiting**: Implement rate limiting for production use

##  Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

1. **Using Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Using Docker** (create Dockerfile)
   ```dockerfile
   FROM python:3.9-slim
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
   ```

3. **Environment Setup**
   - Set `FLASK_ENV=production`
   - Configure proper CORS origins
   - Set up proper logging
   - Use a production database if needed

##  Performance

- **Caching**: Products are cached in memory for faster access
- **Async Operations**: Non-blocking operations where possible
- **Rate Limiting**: Built-in delays for web scraping
- **Error Handling**: Graceful degradation with fallback data

##  Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **Import Errors**
   ```bash
   # Ensure virtual environment is activated
   source venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **CORS Issues**
   - Check Flask-CORS configuration
   - Ensure frontend origin is allowed


**Live link**: https://prashantmahawar75.github.io/Maketronics-assignment/

**Screen-Shot**: 

<img width="1919" height="885" alt="image" src="https://github.com/user-attachments/assets/92f7a9b5-bdf7-4e9a-b66a-1bbd9b9869c9" />

<img width="1919" height="863" alt="image" src="https://github.com/user-attachments/assets/6deeb8c2-6a14-4cab-8ac9-26c50b6eec06" />

<img width="1919" height="871" alt="image" src="https://github.com/user-attachments/assets/ba125d84-87e0-45ac-9c1f-4f7a7e9420b7" />


