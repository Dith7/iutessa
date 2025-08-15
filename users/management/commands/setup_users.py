from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.signals import create_default_groups

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialise les données utilisateurs de base'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-admin',
            action='store_true',
            help='Crée un utilisateur administrateur par défaut',
        )

    def handle(self, *args, **options):
        self.stdout.write('Initialisation des données utilisateurs...')

        # Créer les groupes par défaut
        self.stdout.write('Création des groupes par défaut...')
        create_default_groups()
        self.stdout.write(
            self.style.SUCCESS('Groupes créés avec succès')
        )

        # Créer un admin par défaut si demandé
        if options['create_admin']:
            self.create_default_admin()

        self.stdout.write(
            self.style.SUCCESS('Initialisation terminée avec succès!')
        )

    def create_default_admin(self):
        """Crée un utilisateur administrateur par défaut"""
        admin_username = 'admin'
        
        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.WARNING(f'L\'utilisateur {admin_username} existe déjà')
            )
            return

        admin_user = User.objects.create_user(
            username=admin_username,
            email='admin@universite.fr',
            password='admin123',
            first_name='Administrateur',
            last_name='Système',
            role='ADMIN',
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Utilisateur administrateur créé: {admin_username} / admin123'
            )
        )

        # Créer quelques utilisateurs de test
        self.create_test_users()

    def create_test_users(self):
        """Crée des utilisateurs de test"""
        test_users = [
            {
                'username': 'etudiant1',
                'email': 'etudiant1@universite.fr',
                'password': 'etudiant123',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'role': 'ETUDIANT'
            },
            {
                'username': 'etudiant2',
                'email': 'etudiant2@universite.fr',
                'password': 'etudiant123',
                'first_name': 'Marie',
                'last_name': 'Martin',
                'role': 'ETUDIANT'
            },
            {
                'username': 'visiteur1',
                'email': 'visiteur1@universite.fr',
                'password': 'visiteur123',
                'first_name': 'Pierre',
                'last_name': 'Visiteur',
                'role': 'VISITEUR'
            }
        ]

        for user_data in test_users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(
                    f'Utilisateur de test créé: {user_data["username"]}'
                )