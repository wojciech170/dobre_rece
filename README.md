# Dobre Ręce

This project is part of the **PortfolioLab** program provided by **CodersLab**, where I was given static files and most templates. While I modified the templates to better fit the project, all Python code was written by me. The goal of the project is to showcase my skills in Django development, front-end integration, and project structuring.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## About the Project

**Dobre Ręce** is a Django-based web application aimed at demonstrating backend and frontend integration using Django's template system and JavaScript.

While **CodersLab** provided the static files and most of the templates, I modified those templates significantly and wrote all of the Python code for this project from scratch. The focus was on creating a flexible structure, optimizing code reuse, and improving functionality with JavaScript enhancements.

### What I Worked On

- Developed all Python code, including views, models, and form handling.
- Refactored the base template to optimize code reusability across multiple pages.
- Modified JavaScript for better functionality and user interaction.
- Implemented form handling features (with plans for more improvements).

## Features

- Modular template structure using Django template inheritance.
- Interactive form handling with JavaScript.
- Responsive design.

### Known Issues

- **Pagination**: Currently, the pagination feature isn't fully functional. This is something I'm aware of and may address in future updates.

## Technologies Used

- **Django**: Backend framework used for managing views, models, and templates.
- **JavaScript**: Modified scripts to enhance frontend functionality.
- **HTML/CSS**: For structuring and styling the UI.

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/wojciech170/dobre_rece.git
   ```

2. Create a virtual environment and activate it:
   ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
   
3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
    
5. Run the development server:
    ```bash
    python manage.py runserver
    ```
    
## Usage

After starting the server, you can access the project at http://127.0.0.1:8000/. Navigate through the different views to explore the form handling and interactive features.


