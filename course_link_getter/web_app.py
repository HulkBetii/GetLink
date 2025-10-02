#!/usr/bin/env python3
"""
Course Link Getter - Web UI Version

A simple web-based interface for browsing course links.
"""

import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from core.store import CatalogStore


class CourseWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the web interface."""
    
    def __init__(self, *args, **kwargs):
        self.store = CatalogStore()
        self.store.load_from_json("assets/catalog.sample.json")
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path.startswith('/api/courses'):
            self.serve_courses_api()
        elif self.path.startswith('/api/categories'):
            self.serve_categories_api()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main HTML page."""
        html = self.get_html_template()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_courses_api(self):
        """Serve courses data as JSON."""
        # Parse query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        
        category = params.get('category', [None])[0]
        subcategory = params.get('subcategory', [None])[0]
        text = params.get('text', [None])[0]
        
        # Filter courses
        courses = self.store.filter(
            category=category,
            subcategory=subcategory,
            text=text
        )
        
        # Convert to JSON
        courses_data = [course.model_dump() for course in courses]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(courses_data).encode())
    
    def serve_categories_api(self):
        """Serve categories data as JSON."""
        categories = self.store.list_categories()
        categories_data = [category.model_dump() for category in categories]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(categories_data).encode())
    
    def get_html_template(self):
        """Get the HTML template for the web interface."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Link Getter</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .filters {
            padding: 20px;
            background: #ecf0f1;
            border-bottom: 1px solid #bdc3c7;
        }
        .filter-group {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 10px;
        }
        .filter-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .filter-group select, .filter-group input {
            padding: 8px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            font-size: 14px;
        }
        .results {
            padding: 20px;
        }
        .course-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }
        .course-table th, .course-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }
        .course-table th {
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }
        .course-table tr:hover {
            background-color: #f8f9fa;
        }
        .course-link {
            color: #3498db;
            text-decoration: none;
        }
        .course-link:hover {
            text-decoration: underline;
        }
        .tags {
            font-size: 12px;
            color: #7f8c8d;
        }
        .status {
            margin-top: 10px;
            padding: 10px;
            background: #d5dbdb;
            border-radius: 4px;
        }
        .btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 4px;
            cursor: pointer;
            margin-right: 10px;
        }
        .btn:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Course Link Getter</h1>
            <p>Browse and access course links through hierarchical categories</p>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label for="search">Search:</label>
                <input type="text" id="search" placeholder="Search courses..." onkeyup="filterCourses()">
            </div>
            
            <div class="filter-group">
                <label for="category">Category:</label>
                <select id="category" onchange="updateSubcategories(); filterCourses()">
                    <option value="">All Categories</option>
                </select>
            </div>
            
            <div class="filter-group">
                <label for="subcategory">Subcategory:</label>
                <select id="subcategory" onchange="filterCourses()">
                    <option value="">All Subcategories</option>
                </select>
            </div>
            
            <div class="filter-group">
                <button class="btn" onclick="showAllCourses()">Show All</button>
                <button class="btn" onclick="copyAllLinks()">Copy All Links</button>
                <button class="btn" onclick="exportCSV()">Export CSV</button>
            </div>
        </div>
        
        <div class="results">
            <div class="status" id="status">Loading courses...</div>
            <table class="course-table" id="courseTable">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Category</th>
                        <th>Subcategory</th>
                        <th>Provider</th>
                        <th>Tags</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody id="courseTableBody">
                </tbody>
            </table>
        </div>
    </div>

    <script>
        let allCourses = [];
        let categories = [];
        
        // Load data on page load
        window.onload = function() {
            loadCategories();
            loadCourses();
        };
        
        async function loadCategories() {
            try {
                const response = await fetch('/api/categories');
                categories = await response.json();
                
                const categorySelect = document.getElementById('category');
                categories.forEach(cat => {
                    const option = document.createElement('option');
                    option.value = cat.name;
                    option.textContent = cat.name;
                    categorySelect.appendChild(option);
                });
            } catch (error) {
                console.error('Error loading categories:', error);
            }
        }
        
        async function loadCourses() {
            try {
                const response = await fetch('/api/courses');
                allCourses = await response.json();
                displayCourses(allCourses);
                updateStatus(`Loaded ${allCourses.length} courses`);
            } catch (error) {
                console.error('Error loading courses:', error);
                updateStatus('Error loading courses');
            }
        }
        
        async function filterCourses() {
            const search = document.getElementById('search').value;
            const category = document.getElementById('category').value;
            const subcategory = document.getElementById('subcategory').value;
            
            let url = '/api/courses?';
            if (category) url += `category=${encodeURIComponent(category)}&`;
            if (subcategory) url += `subcategory=${encodeURIComponent(subcategory)}&`;
            if (search) url += `text=${encodeURIComponent(search)}&`;
            
            try {
                const response = await fetch(url);
                const courses = await response.json();
                displayCourses(courses);
                updateStatus(`Showing ${courses.length} courses`);
            } catch (error) {
                console.error('Error filtering courses:', error);
                updateStatus('Error filtering courses');
            }
        }
        
        function displayCourses(courses) {
            const tbody = document.getElementById('courseTableBody');
            tbody.innerHTML = '';
            
            courses.forEach(course => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${course.title}</td>
                    <td>${course.category}</td>
                    <td>${course.subcategory}</td>
                    <td>${course.provider}</td>
                    <td class="tags">${course.tags.join(', ')}</td>
                    <td><a href="${course.link}" target="_blank" class="course-link">Open Link</a></td>
                `;
                tbody.appendChild(row);
            });
        }
        
        function updateSubcategories() {
            const categorySelect = document.getElementById('category');
            const subcategorySelect = document.getElementById('subcategory');
            
            subcategorySelect.innerHTML = '<option value="">All Subcategories</option>';
            
            const selectedCategory = categorySelect.value;
            if (selectedCategory) {
                const category = categories.find(cat => cat.name === selectedCategory);
                if (category) {
                    category.subcategories.forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub;
                        option.textContent = sub;
                        subcategorySelect.appendChild(option);
                    });
                }
            }
        }
        
        function showAllCourses() {
            document.getElementById('search').value = '';
            document.getElementById('category').value = '';
            document.getElementById('subcategory').value = '';
            displayCourses(allCourses);
            updateStatus(`Showing all ${allCourses.length} courses`);
        }
        
        function copyAllLinks() {
            const visibleCourses = Array.from(document.querySelectorAll('#courseTableBody tr'))
                .map(row => {
                    const linkCell = row.querySelector('.course-link');
                    return linkCell ? linkCell.href : null;
                })
                .filter(link => link);
            
            const linksText = visibleCourses.join('\\n');
            navigator.clipboard.writeText(linksText).then(() => {
                updateStatus(`Copied ${visibleCourses.length} links to clipboard`);
            }).catch(err => {
                updateStatus('Failed to copy links to clipboard');
            });
        }
        
        function exportCSV() {
            const visibleCourses = Array.from(document.querySelectorAll('#courseTableBody tr'))
                .map(row => {
                    const cells = row.querySelectorAll('td');
                    if (cells.length >= 5) {
                        return {
                            title: cells[0].textContent,
                            category: cells[1].textContent,
                            subcategory: cells[2].textContent,
                            provider: cells[3].textContent,
                            tags: cells[4].textContent,
                            link: cells[5].querySelector('.course-link')?.href || ''
                        };
                    }
                    return null;
                })
                .filter(course => course);
            
            const csvContent = [
                'Title,Category,Subcategory,Provider,Tags,Link',
                ...visibleCourses.map(course => 
                    `"${course.title}","${course.category}","${course.subcategory}","${course.provider}","${course.tags}","${course.link}"`
                )
            ].join('\\n');
            
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `courses_${new Date().toISOString().slice(0,10)}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);
            
            updateStatus(`Exported ${visibleCourses.length} courses to CSV`);
        }
        
        function updateStatus(message) {
            document.getElementById('status').textContent = message;
        }
    </script>
</body>
</html>
        """


def main():
    """Start the web server."""
    # Try different ports if 8080 is busy
    ports_to_try = [8080, 8081, 8082, 3000, 5000]
    httpd = None
    
    for port in ports_to_try:
        try:
            server_address = ('', port)
            httpd = HTTPServer(server_address, CourseWebHandler)
            print(f"🌐 Starting Course Link Getter Web Server...")
            print(f"📱 Open your browser and go to: http://localhost:{port}")
            print(f"🛑 Press Ctrl+C to stop the server")
            break
        except OSError as e:
            if e.errno == 48:  # Address already in use
                print(f"⚠️  Port {port} is busy, trying next port...")
                continue
            else:
                raise
    
    if httpd is None:
        print("❌ Could not find an available port. Please try again later.")
        return
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped.")
        httpd.shutdown()


if __name__ == "__main__":
    main()
