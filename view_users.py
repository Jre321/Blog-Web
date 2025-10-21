#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask_blog import create_app, db
from flask_blog.models import User

def view_users():
    """Muestra todos los usuarios registrados."""
    app = create_app()
    
    with app.app_context():
        try:
            users = User.query.all()
            
            if not users:
                print("No hay usuarios registrados en la base de datos.")
                return
            
            print("USUARIOS REGISTRADOS:")
            print("=" * 60)
            
            for user in users:
                print(f"ID: {user.id}")
                print(f"Username: {user.username}")
                print(f"Email: {user.email}")
                print(f"Password Hash: {user.password_hash[:50]}...")
                print(f"Posts: {len(user.posts)}")
                print("-" * 40)
                
        except Exception as e:
            print(f"Error al acceder a la base de datos: {e}")
            print("Asegúrate de que PostgreSQL esté ejecutándose y la base de datos esté configurada.")

if __name__ == "__main__":
    view_users()
