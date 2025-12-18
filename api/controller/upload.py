import os
from fastapi import UploadFile, HTTPException, Request

# Configuration pour Render
# Render fournit RENDER_EXTERNAL_URL, sinon on utilise BASE_URL ou localhost
def get_base_url() -> str:
    """Récupère l'URL de base du serveur"""
    # Render fournit cette variable d'environnement
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url:
        return render_url.rstrip('/')
    
    # Sinon utiliser BASE_URL si défini
    base_url = os.getenv("BASE_URL")
    if base_url:
        return base_url.rstrip('/')
    
    # Par défaut pour le développement local
    return "http://localhost:8000"

UPLOAD_DIR = "uploads/produits"

# Créer le répertoire d'upload s'il n'existe pas
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def upload_image_to_render(file: UploadFile, filename: str, request: Request = None) -> str:
    """
    Upload une image sur le serveur Render (stockage local)
    
    Args:
        file: Le fichier à uploader
        filename: Le nom du fichier sur le serveur
        request: Objet Request FastAPI pour construire l'URL (optionnel)
        
    Returns:
        L'URL publique de l'image uploadée
    """
    try:
        # Lire le contenu du fichier
        file_content = await file.read()
        
        # Chemin complet du fichier local
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Écrire le fichier sur le disque
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Construire l'URL publique
        # Priorité : request.base_url > RENDER_EXTERNAL_URL > BASE_URL > localhost
        if request:
            # Utiliser l'URL de la requête (fonctionne automatiquement sur Render)
            base_url = str(request.base_url).rstrip('/')
        else:
            # Fallback sur les variables d'environnement
            base_url = get_base_url()
        
        # Retourner l'URL publique (servie par FastAPI StaticFiles)
        # Le chemin commence par /uploads car c'est monté dans main.py
        image_url = f"{base_url}/uploads/produits/{filename}"
        return image_url
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'upload: {str(e)}"
        )
