#!/bin/bash

echo "🔧 Correction rapide - Template videos.html manquant"
echo "=================================================="

# Créer le dossier si nécessaire
mkdir -p templates/pages/blocks/

# Créer le template videos.html
cat > templates/pages/blocks/videos.html << 'EOF'
<!-- templates/pages/blocks/videos.html -->
<div class="py-16 lg:py-24 bg-black text-white">
    <div class="container mx-auto px-4">
        <div class="text-center mb-16">
            <h2 class="text-4xl lg:text-5xl font-bold mb-6">{{ block.title }}</h2>
            {% if block.subtitle %}
                <p class="text-xl text-gray-300 max-w-3xl mx-auto">{{ block.subtitle }}</p>
            {% endif %}
        </div>
        
        <div class="max-w-6xl mx-auto">
            <!-- Contenu textuel -->
            {% if block.content %}
                <div class="prose prose-lg prose-invert max-w-none mb-12 text-center">
                    {{ block.content|safe }}
                </div>
            {% endif %}
            
            <!-- Lecteur vidéo -->
            <div class="relative mb-8">
                {% if block.video_file %}
                    <!-- Vidéo locale -->
                    <div class="relative rounded-2xl overflow-hidden shadow-2xl">
                        <video 
                            class="w-full h-auto max-h-96 lg:max-h-[500px]" 
                            controls 
                            preload="metadata"
                            {% if block.video_thumbnail %}poster="{{ block.video_thumbnail.url }}"{% endif %}>
                            <source src="{{ block.video_file.url }}" type="video/mp4">
                            Votre navigateur ne supporte pas la lecture vidéo.
                        </video>
                    </div>
                    
                {% elif block.video_url %}
                    <!-- Vidéo YouTube/Vimeo -->
                    <div class="relative rounded-2xl overflow-hidden shadow-2xl">
                        <div class="aspect-w-16 aspect-h-9">
                            <iframe 
                                src="{{ block.get_video_embed_url }}"
                                class="w-full h-96 lg:h-[500px]"
                                frameborder="0"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowfullscreen>
                            </iframe>
                        </div>
                    </div>
                    
                {% elif block.video_embed_code %}
                    <!-- Code d'intégration personnalisé -->
                    <div class="relative rounded-2xl overflow-hidden shadow-2xl">
                        {{ block.video_embed_code|safe }}
                    </div>
                    
                {% elif block.image %}
                    <!-- Image de remplacement si pas de vidéo -->
                    <div class="relative rounded-2xl overflow-hidden shadow-2xl">
                        <img src="{{ block.image.url }}" 
                             class="w-full h-96 lg:h-[500px] object-cover" 
                             alt="{{ block.title }}">
                        <div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                            <div class="text-center">
                                <svg class="w-16 h-16 mx-auto mb-4 text-white" fill="currentColor" viewBox="0 0 24 24">
                                    <path d="M8 5v14l11-7z"/>
                                </svg>
                                <p class="text-xl font-semibold">Vidéo bientôt disponible</p>
                            </div>
                        </div>
                    </div>
                {% endif %}
            </div>
            
            <!-- Lien additionnel -->
            {% if block.link_url %}
                <div class="text-center">
                    <a href="{{ block.link_url }}" 
                       class="inline-flex items-center bg-red-600 text-white font-semibold px-8 py-4 rounded-full hover:bg-red-700 transform hover:scale-105 transition-all duration-300 shadow-lg">
                        {{ block.link_text|default:"Voir plus de vidéos" }}
                        <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H15M9 10V9a2 2 0 012-2h2a2 2 0 012 2v1.01"></path>
                        </svg>
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
EOF

echo "✅ Template videos.html créé avec succès !"
echo ""
echo "🔧 Si d'autres templates sont manquants, créez-les :"

# Créer aussi les autres templates s'ils manquent
for template in documents testimonials stats team; do
    if [ ! -f "templates/pages/blocks/${template}.html" ]; then
        echo "📝 Création de ${template}.html..."
        cp templates/pages/blocks/videos.html templates/pages/blocks/${template}.html
        # Adapter le contenu pour chaque type
        case $template in
            "documents")
                sed -i 's/bg-black text-white/bg-gray-50/' templates/pages/blocks/${template}.html
                sed -i 's/prose-invert/prose-gray/' templates/pages/blocks/${template}.html
                ;;
            "testimonials")
                sed -i 's/bg-black text-white/bg-blue-50/' templates/pages/blocks/${template}.html
                sed -i 's/prose-invert/prose-blue/' templates/pages/blocks/${template}.html
                ;;
            *)
                sed -i 's/bg-black text-white/bg-white/' templates/pages/blocks/${template}.html
                sed -i 's/prose-invert/prose-gray/' templates/pages/blocks/${template}.html
                ;;
        esac
        echo "✅ ${template}.html créé"
    else
        echo "✅ ${template}.html existe déjà"
    fi
done

echo ""
echo "🚀 Problème résolu ! Relancez le serveur :"
echo "python manage.py runserver"