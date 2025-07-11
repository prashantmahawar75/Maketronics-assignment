from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import time
import random
from urllib.parse import urljoin, urlparse
import logging

app = Flask(__name__)
CORS(app)  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

products_cache = []
last_updated = None

FALLBACK_DATA = [
    {
        "id": 1,
        "title": "iPhone 15 Pro Max",
        "description": "Latest flagship smartphone with titanium design, A17 Pro chip, and advanced camera system.",
        "price": "AED 1,59,900",
        "category": "smartphone",
        "link": "https://www.apple.com/iphone-15-pro/",
        "source": "Apple Store"
    },
    {
        "id": 2,
        "title": "Samsung Galaxy S24 Ultra",
        "description": "Premium Android smartphone with S Pen, 200MP camera, and AI-powered features.",
        "price": "AED 1,29,999",
        "category": "smartphone",
        "link": "https://www.samsung.com/in/smartphones/galaxy-s24-ultra/",
        "source": "Samsung"
    },
    {
        "id": 3,
        "title": "MacBook Pro 16\" M3 Max",
        "description": "Professional laptop with M3 Max chip, 18-hour battery life, and stunning Liquid Retina XDR display.",
        "price": "AED 3,99,900",
        "category": "laptop",
        "link": "https://www.apple.com/macbook-pro/",
        "source": "Apple Store"
    },
    {
        "id": 4,
        "title": "Dell XPS 13 Plus",
        "description": "Ultrabook with 13th Gen Intel Core processors, premium build quality, and edge-to-edge display.",
        "price": "AED 1,54,990",
        "category": "laptop",
        "link": "https://www.dell.com/en-in/shop/laptops/xps-13-plus/spd/xps-13-9320-laptop",
        "source": "Dell"
    },
    {
        "id": 5,
        "title": "Sony WH-1000XM5",
        "description": "Industry-leading noise canceling headphones with 30-hour battery life and crystal-clear calls.",
        "price": "AED 29,990",
        "category": "headphones",
        "link": "https://www.sony.co.in/headphones/wh-1000xm5",
        "source": "Sony"
    },
    {
        "id": 6,
        "title": "AirPods Pro (2nd Gen)",
        "description": "Wireless earbuds with active noise cancellation, spatial audio, and adaptive transparency.",
        "price": "AED 26,900",
        "category": "headphones",
        "link": "https://www.apple.com/airpods-pro/",
        "source": "Apple Store"
    },
    {
        "id": 7,
        "title": "NVIDIA RTX 4090",
        "description": "Ultimate gaming graphics card with 24GB GDDR6X memory and ray tracing capabilities.",
        "price": "AED 1,54,000",
        "category": "gaming",
        "link": "https://www.nvidia.com/en-in/geforce/graphics-cards/40-series/rtx-4090/",
        "source": "NVIDIA"
    },
    {
        "id": 8,
        "title": "PlayStation 5",
        "description": "Next-gen gaming console with ultra-high speed SSD, ray tracing, and 4K gaming support.",
        "price": "AED 54,990",
        "category": "gaming",
        "link": "https://www.playstation.com/en-in/ps5/",
        "source": "PlayStation"
    },
    {
        "id": 9,
        "title": "iPad Pro 12.9\" M2",
        "description": "Professional tablet with M2 chip, Liquid Retina XDR display, and Apple Pencil support.",
        "price": "AED 1,12,900",
        "category": "accessories",
        "link": "https://www.apple.com/ipad-pro/",
        "source": "Apple Store"
    },
    {
        "id": 10,
        "title": "Microsoft Surface Pro 9",
        "description": "2-in-1 laptop tablet with 12th Gen Intel Core processors and all-day battery life.",
        "price": "AED 1,13,999",
        "category": "laptop",
        "link": "https://www.microsoft.com/en-in/surface/devices/surface-pro-9",
        "source": "Microsoft"
    },
    {
        "id": 11,
        "title": "Google Pixel 8 Pro",
        "description": "AI-powered smartphone with advanced computational photography and 7 years of updates.",
        "price": "AED 1,06,999",
        "category": "smartphone",
        "link": "https://store.google.com/product/pixel_8_pro",
        "source": "Google Store"
    },
    {
        "id": 12,
        "title": "OnePlus 12",
        "description": "Flagship killer with Snapdragon 8 Gen 3, 120W fast charging, and Hasselblad camera.",
        "price": "AED 64,999",
        "category": "smartphone",
        "link": "https://www.oneplus.in/12",
        "source": "OnePlus"
    },
    {
        "id": 13,
        "title": "ASUS ROG Zephyrus G16",
        "description": "Gaming laptop with RTX 4070, AMD Ryzen 9 processor, and 240Hz display.",
        "price": "AED 1,89,990",
        "category": "gaming",
        "link": "https://rog.asus.com/laptops/13-14-inch/rog-zephyrus-g16-2024/",
        "source": "ASUS"
    },
    {
        "id": 14,
        "title": "Bose QuietComfort 45",
        "description": "Premium noise-cancelling headphones with 24-hour battery and balanced sound signature.",
        "price": "AED 32,900",
        "category": "headphones",
        "link": "https://www.bose.in/products/headphones/over-ear-headphones/quietcomfort-45-headphones",
        "source": "Bose"
    },
    {
        "id": 15,
        "title": "Logitech MX Master 3S",
        "description": "Advanced wireless mouse with ultra-precise scroll wheel and multi-device connectivity.",
        "price": "AED 8,995",
        "category": "accessories",
        "link": "https://www.logitech.com/en-in/products/mice/mx-master-3s.html",
        "source": "Logitech"
    },
    {
        "id": 16,
        "title": "Samsung 32\" Odyssey G7",
        "description": "1000R curved gaming monitor with 240Hz refresh rate and 1ms response time.",
        "price": "AED 54,999",
        "category": "gaming",
        "link": "https://www.samsung.com/in/monitors/gaming/odyssey-g7-32-inch-lc32g75tqswxxl/",
        "source": "Samsung"
    },
    {
        "id": 17,
        "title": "Apple Magic Keyboard",
        "description": "Wireless keyboard with scissor mechanism, numeric keypad, and rechargeable battery.",
        "price": "AED 19,900",
        "category": "accessories",
        "link": "https://www.apple.com/in/shop/product/MK2C3HN/A/magic-keyboard-with-numeric-keypad",
        "source": "Apple Store"
    },
    {
        "id": 18,
        "title": "ThinkPad X1 Carbon Gen 11",
        "description": "Business ultrabook with 13th Gen Intel Core, carbon fiber construction, and military-grade durability.",
        "price": "AED 1,89,000",
        "category": "laptop",
        "link": "https://www.lenovo.com/in/en/laptops/thinkpad/thinkpad-x1/X1-Carbon-Gen-11/p/21HMCTO1WWIN",
        "source": "Lenovo"
    },
    {
        "id": 19,
        "title": "Razer DeathAdder V3",
        "description": "Ergonomic gaming mouse with 30K DPI sensor, 90-hour battery life, and ultra-lightweight design.",
        "price": "AED 8,999",
        "category": "gaming",
        "link": "https://www.razer.com/gaming-mice/razer-deathadder-v3",
        "source": "Razer"
    },
    {
        "id": 20,
        "title": "JBL Flip 6",
        "description": "Portable Bluetooth speaker with powerful sound, 12-hour playtime, and IP67 waterproof rating.",
        "price": "AED 11,999",
        "category": "accessories",
        "link": "https://in.jbl.com/bluetooth-speakers/JBL+FLIP+6.html",
        "source": "JBL"
    }
]

def safe_request(url, timeout=10):
    """Make a safe HTTP request with error handling"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed for {url}: {e}")
        return None

def extract_price(text):
    """Extract price from text using regex"""
    price_patterns = [
        r'AED [\d,]+',
        r'Rs\.?\s*[\d,]+',
        r'\$[\d,]+',
        r'USD\s*[\d,]+',
        r'INR\s*[\d,]+'
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return "Price not available"

def scrape_tech_products():
    """Enhanced scraping function with real web scraping capability"""
    scraped_products = []
    
    sources = [
        {
            'url': 'https://www.flipkart.com/search?q=smartphone',
            'type': 'flipkart',
            'category': 'smartphone'
        },
        {
            'url': 'https://www.amazon.in/s?k=laptop',
            'type': 'amazon',
            'category': 'laptop'
        }
    ]
    
    try:
        for source in sources:
            response = safe_request(source['url'])
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                if source['type'] == 'flipkart':
                    products = soup.find_all('div', {'data-id': True})[:5]  # Limit to 5 per source
                    for i, product in enumerate(products):
                        try:
                            title = product.find('a', class_='IRpwTa')
                            price = product.find('div', class_='_30jeq3')
                            if title and price:
                                scraped_products.append({
                                    'id': len(scraped_products) + 1,
                                    'title': title.text.strip()[:50] + '...',
                                    'description': f"Popular {source['category']} from Flipkart",
                                    'price': price.text.strip(),
                                    'category': source['category'],
                                    'link': 'https://www.flipkart.com' + title.get('href', ''),
                                    'source': 'Flipkart',
                                    'scraped_at': datetime.now().isoformat()
                                })
                        except:
                            continue
                
                time.sleep(2)
        
        if len(scraped_products) < 10:
            logger.warning("Insufficient scraped data, using fallback data")
            scraped_products.extend(FALLBACK_DATA[:15])
        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        scraped_products = FALLBACK_DATA
    
    return scraped_products[:20]  

def initialize_products():
    """Initialize products cache with fresh data"""
    global products_cache, last_updated
    
    logger.info("Initializing products cache...")
    products_cache = scrape_tech_products()
    last_updated = datetime.now()
    logger.info(f"Loaded {len(products_cache)} products")

def filter_products(products, search=None, category=None, min_price=None, max_price=None):
    """Filter products based on search criteria"""
    filtered = products.copy()
    
    if search:
        search_lower = search.lower()
        filtered = [p for p in filtered if (
            search_lower in p['title'].lower() or
            search_lower in p['description'].lower() or
            search_lower in p['category'].lower()
        )]
    
    if category and category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    
    # if min_price or max_price:
    #     pass
    
    return filtered

@app.route('/')
def index():
    """Serve the main HTML page"""
    try:
        with open('index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Smart Data Display API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .api-doc { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 5px; }
                .endpoint { color: #2c3e50; font-weight: bold; }
                .method { color: #e74c3c; }
            </style>
        </head>
        <body>
            <h1>🚀 Smart Data Display API</h1>
            <p>Backend API for the Tech Products Hub</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="api-doc">
                <span class="method">GET</span> <span class="endpoint">/api/products</span>
                <p>Get all products with optional filtering</p>
                <p>Parameters: search, category, min_price, max_price</p>
            </div>
            
            <div class="api-doc">
                <span class="method">GET</span> <span class="endpoint">/api/products/{id}</span>
                <p>Get a specific product by ID</p>
            </div>
            
            <div class="api-doc">
                <span class="method">POST</span> <span class="endpoint">/api/refresh</span>
                <p>Refresh product data from sources</p>
            </div>
            
            <div class="api-doc">
                <span class="method">GET</span> <span class="endpoint">/api/categories</span>
                <p>Get all available categories</p>
            </div>
            
            <div class="api-doc">
                <span class="method">GET</span> <span class="endpoint">/api/stats</span>
                <p>Get statistics about the product database</p>
            </div>
            
            <h2>Example Usage:</h2>
#             <pre>
# curl http://localhost:5000/api/products
# curl http://localhost:5000/api/products?search=laptop&category=laptop
# curl -X POST http://localhost:5000/api/refresh
#             </pre>
            
#             <p><strong>Note:</strong> This API supports CORS for frontend integration.</p>
        </body>
        </html>
        """

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    try:
        
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        limit = request.args.get('limit', type=int)
        
        filtered_products = filter_products(
            products_cache, 
            search=search if search else None,
            category=category if category else None,
            min_price=min_price,
            max_price=max_price
        )
        
        if limit:
            filtered_products = filtered_products[:limit]
        
        return jsonify({
            'success': True,
            'data': filtered_products,
            'total': len(filtered_products),
            'filters': {
                'search': search,
                'category': category,
                'min_price': min_price,
                'max_price': max_price
            },
            'last_updated': last_updated.isoformat() if last_updated else None,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_products: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        product = next((p for p in products_cache if p['id'] == product_id), None)
        
        if product:
            return jsonify({
                'success': True,
                'data': product,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404
    
    except Exception as e:
        logger.error(f"Error in get_product: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh', methods=['POST'])
def refresh_products():
    """Refresh product data from sources"""
    try:
        logger.info("Refreshing product data...")
        initialize_products()
        
        return jsonify({
            'success': True,
            'message': 'Product data refreshed successfully',
            'total_products': len(products_cache),
            'last_updated': last_updated.isoformat(),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in refresh_products: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    try:
        categories = list(set(product['category'] for product in products_cache))
        categories.sort()
        
        return jsonify({
            'success': True,
            'data': categories,
            'total': len(categories),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_categories: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about the product database"""
    try:
        categories = {}
        price_ranges = {
            'under_10k': 0,
            '10k_50k': 0,
            '50k_100k': 0,
            'above_100k': 0
        }
        
        for product in products_cache:
           
            category = product['category']
            categories[category] = categories.get(category, 0) + 1

            price_text = product['price']
            if '₹' in price_text:
                price_match = re.search(r'₹([\d,]+)', price_text)
                if price_match:
                    price_num = int(price_match.group(1).replace(',', ''))
                    if price_num < 10000:
                        price_ranges['under_10k'] += 1
                    elif price_num < 50000:
                        price_ranges['10k_50k'] += 1
                    elif price_num < 100000:
                        price_ranges['50k_100k'] += 1
                    else:
                        price_ranges['above_100k'] += 1
        
        return jsonify({
            'success': True,
            'data': {
                'total_products': len(products_cache),
                'categories': categories,
                'price_ranges': price_ranges,
                'last_updated': last_updated.isoformat() if last_updated else None
            },
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"Error in get_stats: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'products_loaded': len(products_cache),
        'last_updated': last_updated.isoformat() if last_updated else None,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    
    initialize_products()
    
    # for runnig  the app
    app.run(debug=True, host='0.0.0.0', port=5000)