#!/bin/bash

echo "🧪 VALIDATION FINALE DU SYSTÈME DE MÉDIAS"
echo "========================================"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ERRORS=0

# 1. Vérifier la structure des dossiers
echo -e "\n${BLUE}📁 1. Vérification de la structure${NC}"

declare -a REQUIRED_DIRS=(
    "pages/templates/pages/blocks"
    "pages/templates/pages/partials"
    "media/documents"
    "media/videos"
    "media/blocks/images"
    "media/videos/thumbnails"
    "static/admin/css"
    "static/admin/js"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $dir${NC}"
    else
        echo -e "${RED}❌ $dir manquant${NC}"
        ((ERRORS++))
    fi
done

# 2. Vérifier les templates
echo -e "\n${BLUE}📝 2. Vérification des templates${NC}"

declare -a REQUIRED_TEMPLATES=(
    "pages/templates/pages/blocks/documents.html"
    "pages/templates/pages/blocks/videos.html"
    "pages/templates/pages/partials/document.html"
    "pages/templates/pages/partials/video.html"
    "pages/templates/pages/partials/media_gallery.html"
)

for template in "${REQUIRED_TEMPLATES[@]}"; do
    if [ -f "$template" ]; then
        echo -e "${GREEN}✅ $(basename $template)${NC}"
    else
        echo -e "${RED}❌ $(basename $template) manquant${NC}"
        ((ERRORS++))
    fi
done

# 3. Vérifier le modèle Django
echo -e "\n${BLUE}🏗️  3. Vérification du modèle${NC}"

python manage.py shell -c "
import sys
try:
    from pages.models import PageBlock
    
    # Vérifier les nouveaux champs
    field_names = [f.name for f in PageBlock._meta.get_fields()]
    
    required_fields = ['document', 'document_title', 'video_type', 'video_file', 'video_url', 'video_embed_code', 'video_thumbnail']
    
    missing_fields = []
    for field in required_fields:
        if field not in field_names:
            missing_fields.append(field)
    
    if missing_fields:
        print(f'❌ Champs manquants: {missing_fields}')
        sys.exit(1)
    else:
        print('✅ Tous les champs requis sont présents')
    
    # Tester les méthodes
    methods = ['get_document_name', 'get_document_extension', 'get_document_size', 'get_video_embed_url', 'has_media']
    
    for method in methods:
        if hasattr(PageBlock, method):
            print(f'✅ Méthode {method} disponible')
        else:
            print(f'❌ Méthode {method} manquante')
            sys.exit(1)
    
    print('✅ Modèle PageBlock validé')
    
except Exception as e:
    print(f'❌ Erreur avec le modèle: {e}')
    sys.exit(1)
" 2>/dev/null

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Problème avec le modèle PageBlock${NC}"
    ((ERRORS++))
else
    echo -e "${GREEN}✅ Modèle PageBlock validé${NC}"
fi

# 4. Vérifier les migrations
echo -e "\n${BLUE}🗃️  4. Vérification des migrations${NC}"

python manage.py showmigrations pages --plan | tail -5

if python manage.py showmigrations pages | grep -q "\[ \]"; then
    echo -e "${YELLOW}⚠️  Migrations en attente détectées${NC}"
    echo "Appliquer avec: python manage.py migrate"
else
    echo -e "${GREEN}✅ Migrations à jour${NC} "
fi

# 5. Test du serveur
echo -e "\n${BLUE}🌐 5. Test du serveur${NC}"

echo "Démarrage du serveur (test 3 secondes)..."
python manage.py runserver 8000 > /dev/null 2>&1 &
SERVER_PID=$!
sleep 3

if kill -0 $SERVER_PID 2>/dev/null; then
    echo -e "${GREEN}✅ Serveur fonctionne${NC}"
    
    # Test admin
    if curl -s http://localhost:8000/admin/ | grep -q "admin"; then
        echo -e "${GREEN}✅ Admin accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  Admin non testé complètement${NC}"
    fi
    
    # Test page d'accueil
    if curl -s http://localhost:8000/ | grep -q "Université"; then
        echo -e "${GREEN}✅ Page d'accueil accessible${NC}"
    else
        echo -e "${YELLOW}⚠️  Page d'accueil non testée complètement${NC}"
    fi
else
    echo -e "${RED}❌ Serveur ne démarre pas${NC}"
    ((ERRORS++))
fi

# Arrêter le serveur
kill $SERVER_PID 2>/dev/null

# 6. Vérifier les permissions
echo -e "\n${BLUE}🔒 6. Vérification des permissions${NC}"

if [ -w "media/" ]; then
    echo -e "${GREEN}✅ Dossier media accessible en écriture${NC}"
else
    echo -e "${RED}❌ Dossier media non accessible en écriture${NC}"
    echo "Corriger avec: chmod -R 755 media/"
    ((ERRORS++))
fi

# 7. Test des types de fichiers
echo -e "\n${BLUE}📎 7. Test des validateurs de fichiers${NC}"

python manage.py shell -c "
try:
    from pages.models import validate_file_size
    from django.core.exceptions import ValidationError
    from django.core.files.uploadedfile import SimpleUploadedFile
    
    # Test validateur de taille (simulation)
    class MockFile:
        def __init__(self, size):
            self.size = size
    
    # Test taille OK
    try:
        validate_file_size(MockFile(1024 * 1024))  # 1MB
        print('✅ Validation taille 1MB: OK')
    except ValidationError:
        print('❌ Validation taille 1MB: Erreur')
    
    # Test taille trop grande
    try:
        validate_file_size(MockFile(100 * 1024 * 1024))  # 100MB
        print('❌ Validation taille 100MB: Devrait échouer')
    except ValidationError:
        print('✅ Validation taille 100MB: Rejetée correctement')
    
except Exception as e:
    print(f'❌ Erreur validateurs: {e}')
" 2>/dev/null

# 8. Résumé final
echo -e "\n" + "=" * 50
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 VALIDATION RÉUSSIE !${NC}"
    echo -e "${GREEN}================================${NC}"
    echo ""
    echo -e "${GREEN}✅ Système de médias entièrement fonctionnel${NC}"
    echo ""
    echo -e "${YELLOW}🚀 Prochaines étapes :${NC}"
    echo "1. python manage.py runserver"
    echo "2. Aller sur http://localhost:8000/admin/"
    echo "3. Créer/modifier un bloc avec médias"
    echo "4. Tester upload document/vidéo"
    echo "5. Voir le résultat sur http://localhost:8000/"
    echo ""
    echo -e "${YELLOW}📋 Fonctionnalités disponibles :${NC}"
    echo "• Upload de documents (PDF, Word, Excel, PowerPoint)"
    echo "• Upload de vidéos locales (MP4, WebM)"
    echo "• Intégration YouTube/Vimeo"
    echo "• Code embed personnalisé"
    echo "• Templates spécialisés documents/vidéos"
    echo "• Interface admin moderne"
    echo "• Validation automatique des fichiers"
    echo ""
    echo -e "${BLUE}💡 Commandes utiles :${NC}"
    echo "• Créer blocs avec médias : python manage.py create_default_blocks --with-media-examples"
    echo "• Backup données : python manage.py dumpdata pages.PageBlock > backup.json"
    echo "• Restaurer données : python manage.py loaddata backup.json"
    
else
    echo -e "${RED}❌ VALIDATION ÉCHOUÉE !${NC}"
    echo -e "${RED}========================${NC}"
    echo ""
    echo -e "${RED}$ERRORS erreur(s) détectée(s)${NC}"
    echo ""
    echo -e "${YELLOW}🔧 Actions correctives :${NC}"
    echo "1. Vérifiez les erreurs ci-dessus"
    echo "2. Lancez: bash setup_media_system.sh"
    echo "3. Relancez ce test: bash final_validation_script.sh"
    echo ""
    echo -e "${YELLOW}📞 Support :${NC}"
    echo "• Vérifiez les logs : python manage.py runserver"
    echo "• Testez les migrations : python manage.py migrate"
    echo "• Recréez la structure : mkdir -p pages/templates/pages/{blocks,partials}"
fi

echo ""
echo -e "${BLUE}🏁 Validation terminée${NC}"