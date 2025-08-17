# pages/management/commands/create_academic_blocks.py
from django.core.management.base import BaseCommand
from pages.models import PageBlock

class Command(BaseCommand):
    help = 'Crée les blocs académiques publics pour afficher les filières et informations'

    def handle(self, *args, **options):
        
        # Bloc Filières publiques
        filieres_block, created = PageBlock.objects.get_or_create(
            block_type='academic_filieres',
            order=3,
            defaults={
                'title': 'Nos Filières de Formation',
                'subtitle': 'Découvrez tous nos programmes d\'excellence',
                'content': '''
                <p class="text-xl text-gray-600 mb-12 max-w-3xl mx-auto">
                    Notre institut propose des formations d'excellence dans plusieurs domaines, 
                    adaptées aux besoins du marché du travail moderne.
                </p>
                ''',
                'status': 'active',
                'link_text': 'Voir toutes les filières',
                'link_url': '/academique/filieres/'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Filières publiques créé'))

        # Bloc Admission/Inscription
        admission_block, created = PageBlock.objects.get_or_create(
            block_type='academic_admission',
            order=4,
            defaults={
                'title': 'Admission & Inscription',
                'subtitle': 'Rejoignez notre communauté étudiante',
                'content': '''
                <div class="grid md:grid-cols-2 gap-12">
                    <div>
                        <h4 class="text-2xl font-bold text-gray-900 mb-4">📋 Processus d'admission</h4>
                        <div class="space-y-4">
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-100 text-blue-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">1</span>
                                <div>
                                    <h5 class="font-semibold">Dossier de candidature</h5>
                                    <p class="text-gray-600">Soumettez votre dossier complet avec les pièces requises</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-100 text-blue-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">2</span>
                                <div>
                                    <h5 class="font-semibold">Examen d'entrée</h5>
                                    <p class="text-gray-600">Passez l'examen dans votre domaine de spécialisation</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-100 text-blue-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">3</span>
                                <div>
                                    <h5 class="font-semibold">Entretien</h5>
                                    <p class="text-gray-600">Entretien avec notre commission d'admission</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <h4 class="text-2xl font-bold text-gray-900 mb-4">📅 Calendrier 2025</h4>
                        <div class="bg-blue-50 rounded-xl p-6">
                            <div class="space-y-3">
                                <div class="flex justify-between">
                                    <span class="font-medium">Dépôt des dossiers</span>
                                    <span class="text-blue-600 font-bold">29 Août 2025</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="font-medium">Examen d'entrée</span>
                                    <span class="text-blue-600 font-bold">06 Sept 2025</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="font-medium">Résultats</span>
                                    <span class="text-blue-600 font-bold">15 Sept 2025</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="font-medium">Rentrée</span>
                                    <span class="text-blue-600 font-bold">01 Oct 2025</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Commencer mon inscription',
                'link_url': '/academique/filieres/'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Admission créé'))

        # Bloc Frais et modalités
        frais_block, created = PageBlock.objects.get_or_create(
            block_type='academic_frais',
            order=5,
            defaults={
                'title': 'Frais de Scolarité',
                'subtitle': 'Tarifs transparents et options de financement',
                'content': '''
                <div class="grid md:grid-cols-3 gap-8">
                    <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-blue-600">
                        <div class="text-center">
                            <h4 class="text-xl font-bold text-gray-900 mb-2">Frais d'inscription</h4>
                            <div class="text-3xl font-black text-blue-600 mb-4">15 000 FCFA</div>
                            <p class="text-gray-600">Frais d'étude de dossier<br>(non remboursable)</p>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-green-600">
                        <div class="text-center">
                            <h4 class="text-xl font-bold text-gray-900 mb-2">Frais de formation</h4>
                            <div class="text-3xl font-black text-green-600 mb-4">Variable</div>
                            <p class="text-gray-600">Selon la filière choisie<br>Consultez le détail</p>
                        </div>
                    </div>
                    <div class="bg-white rounded-xl shadow-lg p-8 border-t-4 border-purple-600">
                        <div class="text-center">
                            <h4 class="text-xl font-bold text-gray-900 mb-2">Modalités</h4>
                            <div class="text-lg font-bold text-purple-600 mb-4">Flexibles</div>
                            <p class="text-gray-600">Paiement en plusieurs fois<br>Bourses disponibles</p>
                        </div>
                    </div>
                </div>
                <div class="text-center mt-12">
                    <p class="text-lg text-gray-600 mb-6">
                        🏦 <strong>Paiement :</strong> Crédit du Sahel - Compte IUTESSA : 37120000A230612301
                    </p>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Voir les détails des frais',
                'link_url': '/academique/filieres/'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Frais créé'))

        # Bloc Documents requis
        documents_block, created = PageBlock.objects.get_or_create(
            block_type='academic_documents',
            order=6,
            defaults={
                'title': 'Documents Requis',
                'subtitle': 'Constitution de votre dossier de candidature',
                'content': '''
                <div class="bg-blue-50 rounded-2xl p-8 mb-8">
                    <h4 class="text-xl font-bold text-blue-900 mb-6 text-center">
                        📋 Liste complète des documents à fournir
                    </h4>
                    <div class="grid md:grid-cols-2 gap-6">
                        <div class="space-y-4">
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">1</span>
                                <span>Fiche d'inscription dûment remplie</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">2</span>
                                <span>Photocopie du diplôme du Baccalauréat ou relevé de notes</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">3</span>
                                <span>Photocopie de l'acte de naissance</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">4</span>
                                <span>Lettre de motivation adressée au promoteur</span>
                            </div>
                        </div>
                        <div class="space-y-4">
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">5</span>
                                <span>Certificat médical signé par un médecin</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">6</span>
                                <span>Photocopie du reçu de paiement (15 000 FCFA)</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">7</span>
                                <span>02 photos 4x4</span>
                            </div>
                            <div class="flex items-start space-x-3">
                                <span class="bg-blue-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-bold">8</span>
                                <span>01 enveloppe A4 à l'adresse du candidat</span>
                            </div>
                        </div>
                    </div>
                    <div class="text-center mt-8">
                        <p class="text-red-600 font-semibold">
                            ⚠️ Seuls les dossiers complets seront reçus. Les dossiers incomplets seront rejetés.
                        </p>
                    </div>
                </div>
                ''',
                'status': 'active',
                'link_text': 'Télécharger la fiche d\'inscription',
                'link_url': 'https://bit.ly/3ZsFBbg'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Bloc Documents créé'))

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Blocs académiques publics créés avec succès!')
        )