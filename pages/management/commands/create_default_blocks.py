from django.core.management.base import BaseCommand
from pages.models import PageBlock

class Command(BaseCommand):
    help = 'Crée les blocs par défaut pour la page d\'accueil avec support médias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--with-media-examples',
            action='store_true',
            help='Inclure des exemples de blocs médias (documents et vidéos)',
        )

    def handle(self, *args, **options):
        # Bloc Hero (Section principale)
        hero_block, created = PageBlock.objects.get_or_create(
            block_type='hero',
            order=1,
            defaults={
                'title': 'Bienvenue à l\'Université d\'Excellence',
                'subtitle': 'Formez votre avenir avec nous',
                'content': '''
                <p>Notre université offre une formation d'excellence dans un environnement stimulant et innovant. 
                Rejoignez une communauté étudiante dynamique et préparez-vous aux défis de demain.</p>
                ''',
                'status': 'active',
                'link_text': 'Découvrir nos formations',
                'link_url': '#formations'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Hero créé'))

        # Bloc À propos
        about_block, created = PageBlock.objects.get_or_create(
            block_type='about',
            order=2,
            defaults={
                'title': 'À Propos de Notre Université',
                'subtitle': 'Une institution de prestige au service de l\'excellence académique',
                'content': '''
                <p>Fondée il y a plus de 50 ans, notre université s'est imposée comme un leader dans l'enseignement supérieur. 
                Nous offrons des programmes innovants dans de nombreux domaines :</p>
                <ul>
                    <li><strong>Sciences et Technologies</strong> - Formations d'avant-garde</li>
                    <li><strong>Sciences Humaines</strong> - Développement personnel et social</li>
                    <li><strong>Commerce et Gestion</strong> - Leadership et entrepreneuriat</li>
                    <li><strong>Médecine et Santé</strong> - Formation médicale d'excellence</li>
                </ul>
                <p>Nos diplômés excellent dans leurs carrières grâce à une formation complète alliant théorie et pratique.</p>
                ''',
                'status': 'active',
                'link_text': 'En savoir plus sur notre histoire',
                'link_url': '#about'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc À Propos créé'))

        # Bloc Actualités/Communiqués
        news_block, created = PageBlock.objects.get_or_create(
            block_type='news',
            order=3,
            defaults={
                'title': 'Actualités & Communiqués',
                'subtitle': 'Restez informés de la vie universitaire',
                'content': '''
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <h4>🎓 Rentrée Académique 2025</h4>
                        <p>Les inscriptions pour l'année académique 2025-2026 sont ouvertes. 
                        Découvrez nos nouveaux programmes et nos modalités d'admission.</p>
                        <p><strong>Date limite :</strong> 30 septembre 2025</p>
                    </div>
                    <div>
                        <h4>🏆 Excellence Académique</h4>
                        <p>Notre université a été classée parmi les 10 meilleures institutions 
                        d'enseignement supérieur du pays pour la troisième année consécutive.</p>
                    </div>
                </div>
                <div class="grid md:grid-cols-2 gap-6 mt-6">
                    <div>
                        <h4>🔬 Nouveau Laboratoire de Recherche</h4>
                        <p>Inauguration de notre laboratoire de recherche en intelligence artificielle, 
                        équipé des dernières technologies.</p>
                    </div>
                    <div>
                        <h4>🌍 Partenariats Internationaux</h4>
                        <p>Signature de nouveaux accords avec des universités prestigieuses 
                        en Europe et en Amérique du Nord.</p>
                    </div>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Voir tous les communiqués',
                'link_url': '#actualites'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Actualités créé'))

        # Bloc Galerie
        gallery_block, created = PageBlock.objects.get_or_create(
            block_type='gallery',
            order=4,
            defaults={
                'title': 'Notre Campus',
                'subtitle': 'Un environnement d\'apprentissage exceptionnel',
                'content': '''
                <p>Découvrez notre magnifique campus moderne, conçu pour offrir le meilleur environnement d'apprentissage :</p>
                <div class="grid md:grid-cols-4 gap-6 text-center">
                    <div>
                        <h5>🏛️ Bâtiments Modernes</h5>
                        <p>Salles de cours équipées des dernières technologies</p>
                    </div>
                    <div>
                        <h5>📚 Bibliothèque Centrale</h5>
                        <p>Plus de 100,000 ouvrages et espaces d'étude</p>
                    </div>
                    <div>
                        <h5>🏃‍♂️ Installations Sportives</h5>
                        <p>Gymnase, terrain de sport et centre de fitness</p>
                    </div>
                    <div>
                        <h5>🍽️ Restaurants</h5>
                        <p>Plusieurs options de restauration sur le campus</p>
                    </div>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Visite virtuelle du campus',
                'link_url': '#campus'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Galerie créé'))

        # Bloc Contact
        contact_block, created = PageBlock.objects.get_or_create(
            block_type='contact',
            order=5,
            defaults={
                'title': 'Contactez-Nous',
                'subtitle': 'Nous sommes là pour répondre à vos questions',
                'content': '''
                <div class="grid md:grid-cols-2 gap-8">
                    <div>
                        <h4>📍 Adresse</h4>
                        <p>123 Avenue de l'Université<br>
                        Yaoundé, Cameroun<br>
                        BP 1234</p>
                        
                        <h4>📞 Téléphone</h4>
                        <p>+237 2XX XX XX XX<br>
                        +237 6XX XX XX XX</p>
                    </div>
                    <div>
                        <h4>✉️ Email</h4>
                        <p>info@universite.cm<br>
                        admission@universite.cm<br>
                        scolarite@universite.cm</p>
                        
                        <h4>🕒 Horaires</h4>
                        <p>Lundi - Vendredi : 8h00 - 17h00<br>
                        Samedi : 8h00 - 12h00</p>
                    </div>
                </div>
                <div class="text-center mt-8">
                    <p><strong>Besoin d'informations sur nos formations ?</strong><br>
                    Notre équipe d'orientation est à votre disposition pour vous guider dans vos choix.</p>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Formulaire de contact',
                'link_url': '#contact'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Contact créé'))

        # Bloc Services
        services_block, created = PageBlock.objects.get_or_create(
            block_type='services',
            order=6,
            defaults={
                'title': 'Nos Services Étudiants',
                'subtitle': 'Un accompagnement complet pour votre réussite',
                'content': '''
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="text-center">
                        <h4>🎯 Orientation Académique</h4>
                        <p>Conseils personnalisés pour choisir votre parcours et optimiser votre réussite.</p>
                    </div>
                    <div class="text-center">
                        <h4>💼 Insertion Professionnelle</h4>
                        <p>Stages, emplois, et accompagnement vers la vie active avec notre réseau d'entreprises partenaires.</p>
                    </div>
                    <div class="text-center">
                        <h4>🏠 Vie Étudiante</h4>
                        <p>Logement, restauration, activités culturelles et sportives pour une expérience universitaire enrichissante.</p>
                    </div>
                </div>
                <div class="grid md:grid-cols-3 gap-8 mt-8">
                    <div class="text-center">
                        <h4>📖 Soutien Pédagogique</h4>
                        <p>Tutorat, cours de soutien et ressources numériques pour vous accompagner dans vos études.</p>
                    </div>
                    <div class="text-center">
                        <h4>🌐 Mobilité Internationale</h4>
                        <p>Programmes d'échange et opportunités d'études à l'étranger avec nos universités partenaires.</p>
                    </div>
                    <div class="text-center">
                        <h4>💡 Innovation & Entrepreneuriat</h4>
                        <p>Incubateur d'entreprises et accompagnement de vos projets innovants.</p>
                    </div>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Découvrir tous nos services',
                'link_url': '#services'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Services créé'))

        # Blocs médias (si demandé)
        if options['with_media_examples']:
            self.create_media_examples()

        active_count = PageBlock.objects.filter(status="active").count()
        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Création terminée ! {active_count} blocs actifs dans la base de données.'
            )
        )

        if not options['with_media_examples']:
            self.stdout.write(
                self.style.WARNING(
                    '\n💡 Pour créer des exemples avec médias, utilisez : --with-media-examples'
                )
            )

    def create_media_examples(self):
        """Créer des exemples de blocs avec médias"""
        
        # Bloc Documents
        doc_block, created = PageBlock.objects.get_or_create(
            block_type='documents',
            order=7,
            defaults={
                'title': 'Documents & Ressources',
                'subtitle': 'Accédez à tous nos documents importants',
                'content': '''
                <p>Retrouvez ici tous les documents essentiels pour votre parcours universitaire :</p>
                <ul>
                    <li><strong>Brochures de formation</strong> - Détails sur tous nos programmes</li>
                    <li><strong>Règlement intérieur</strong> - Règles et procédures de l'université</li>
                    <li><strong>Calendrier académique</strong> - Dates importantes de l'année</li>
                    <li><strong>Formulaires d'inscription</strong> - Documents à remplir</li>
                </ul>
                <p>Tous les documents sont disponibles en téléchargement gratuit.</p>
                ''',
                'status': 'active',
                'document_title': 'Brochure Générale 2025',
                'link_text': 'Accéder à tous les documents',
                'link_url': '#documents'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Documents créé'))

        # Bloc Vidéos
        video_block, created = PageBlock.objects.get_or_create(
            block_type='videos',
            order=8,
            defaults={
                'title': 'Vidéos & Présentations',
                'subtitle': 'Découvrez notre université en images',
                'content': '''
                <p>Plongez dans l'univers de notre université grâce à nos vidéos :</p>
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <h4>🎬 Visite Virtuelle</h4>
                        <p>Découvrez nos campus et installations en vidéo immersive.</p>
                    </div>
                    <div>
                        <h4>🎓 Témoignages Étudiants</h4>
                        <p>Écoutez l'expérience de nos étudiants et diplômés.</p>
                    </div>
                </div>
                <div class="grid md:grid-cols-2 gap-6 mt-6">
                    <div>
                        <h4>👨‍🏫 Conférences</h4>
                        <p>Replays de nos conférences et événements académiques.</p>
                    </div>
                    <div>
                        <h4>🔬 Recherche & Innovation</h4>
                        <p>Présentation de nos projets de recherche et innovations.</p>
                    </div>
                </div>
                ''',
                'status': 'active',
                'video_type': 'youtube',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Exemple
                'link_text': 'Voir toutes nos vidéos',
                'link_url': '#videos'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Vidéos créé'))

        self.stdout.write(self.style.SUCCESS('✓ Exemples de médias créés'))